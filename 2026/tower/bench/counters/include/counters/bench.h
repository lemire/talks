#ifndef COUNTERS_BENCH_H_
#define COUNTERS_BENCH_H_
#include "counters/event_counter.h"
#include <stdexcept>
#include <utility>

#if defined(__GNUC__) || defined(__clang__)
#define COUNTERS_FLATTEN __attribute__((flatten, always_inline)) inline
#elif defined(_MSC_VER)
#define COUNTERS_FLATTEN __forceinline
#else
#define COUNTERS_FLATTEN 
#endif

namespace counters {

/// Parameters to control benchmarking behavior.
///
/// The benchmark performs two levels of repetition:
/// - Outer iterations (``min_repeat`` / ``max_repeat``): the main warm-up and
///   measurement loop. We run the outer loop `N` times to collect multiple
///   samples and compute averages / best / worst results.
/// - Inner iterations (abstracted by ``inner_max_repeat`` /
///   ``min_time_per_inner_ns``): when a single call to the tested function is
///   too fast to measure reliably, the implementation runs the callable `M`
///   times in a tight inner loop and measures that block. All recorded counters
///   are then divided by `M` to produce per-call results. This keeps the API
///   semantics identical: users receive metrics "as if" the callable ran once,
///   while benefiting from more stable timing for very short functions.
///
/// All fields have sensible defaults; override only those you need.
struct bench_parameter {
  /// Minimum number of outer iterations (warmup + measurement).
  ///
  /// The outer loop count `N` controls how many independent samples are
  /// collected. If the warm-up period (after `min_repeat` iterations) is too
  /// short the outer loop may be increased (up to `max_repeat`).
  size_t min_repeat = 10;

  /// Minimum total warm-up time in nanoseconds.
  /// If the total warm-up time (after `min_repeat` iterations) is less than
  /// this value the number of iterations is increased (up to `max_repeat`).
  size_t min_time_ns = 400000000; // 0.4 s

  /// Maximum number of outer iterations.
  /// Guards against runaway increases when trying to reach `min_time_ns`.
  size_t max_repeat = 1000000;
  /// Minimum time per inner iteration in nanoseconds.
  /// When a single call is too fast to measure reliably, the implementation
  /// runs the callable multiple times in a tight inner loop. This ensures
  /// stable timing for very short functions. If you set this value too low,
  /// the timings might be unstable or wrong.
  size_t min_time_per_inner_ns = 30000;
};

template <std::size_t M, typename Func>
COUNTERS_FLATTEN void call_ntimes(Func &&func) {
  if constexpr (M == 1) {
    func();
    return;
  }
  if constexpr (M == 10) {
    func();
    func();
    func();
    func();
    func();
    func();
    func();
    func();
    func();
    func();
    return;
  }
  if constexpr (M == 100) {
    for (size_t i = 0; i < 10; ++i)
      call_ntimes<10>(func);
    return;
  }
  if constexpr (M == 1000) {
    for (size_t i = 0; i < 10; ++i)
      call_ntimes<100>(func);
    return;
  }
  if constexpr (M == 1000) {
    for (size_t i = 0; i < 10; ++i)
      call_ntimes<100>(func);
    return;
  }
  if constexpr (M == 10000) {
    for (size_t i = 0; i < 10; ++i)
      call_ntimes<1000>(func);
    return;
  }
  throw std::runtime_error("Unsupported M in call_ntimes");
}

// Runtime dispatcher that maps some common repetition counts to
// compile-time unrolled instantiations. Allowed compile-time sizes:
// 1, 10, 100, 1000, 10000. Other values fall back to a simple loop.
template <typename Func>
inline void call_ntimes_runtime(Func &&func, size_t M) {
  switch (M) {
  case 1:
    call_ntimes<1>(std::forward<Func>(func));
    break;
  case 10:
    call_ntimes<10>(std::forward<Func>(func));
    break;
  case 100:
    call_ntimes<100>(std::forward<Func>(func));
    break;
  case 1000:
    call_ntimes<1000>(std::forward<Func>(func));
    break;
  case 10000:
    call_ntimes<1000>(std::forward<Func>(func));
    break;
  default:
    throw std::runtime_error("Unsupported M in call_ntimes_runtime");
    break;
  }
}

template <size_t M, class Function>
size_t bench_compute_repeat_impl(Function &&function, event_collector& collector,
                                            size_t min_repeat,
                                            size_t min_time_ns,
                                            size_t max_repeat) {
  auto fn = std::forward<Function>(function);
  size_t N = min_repeat;
  if (N == 0) {
    N = 1;
  }
  // Warm-up
  event_aggregate warm_aggregate{};
  for (size_t i = 0; i < N; i++) {
    collector.start();
    call_ntimes<M>(std::forward<Function>(function));
    event_count allocate_count = collector.end();
    warm_aggregate << allocate_count;
    if ((i + 1 == N) && (warm_aggregate.total_elapsed_ns() < min_time_ns) &&
        (N < max_repeat)) {
      N *= 10;
    }
  }
  return N;
}

// Compile-time specialized bench implementation for a fixed inner repeat M.
template <size_t M, class Function>
event_aggregate bench_impl(Function &&function, size_t min_repeat,
                           size_t min_time_ns, size_t max_repeat) {
  static thread_local event_collector collector;
  // Let us determine the outer repeat count N first.
  size_t N =
      bench_compute_repeat_impl<M>(std::forward<Function>(function), collector,
                                   min_repeat, min_time_ns, max_repeat);
  // Measurement
  event_aggregate aggregate{};
  for (size_t i = 0; i < N; i++) {
    collector.start();
    call_ntimes<M>(std::forward<Function>(function));
    event_count allocate_count = collector.end();
    aggregate << allocate_count;
  }
  aggregate.inner_count = M;
  return aggregate;
}

template <class Function>
event_aggregate bench(Function &&function, size_t min_repeat = 10,
                      size_t min_time_ns = 400'000'000,
                      size_t max_repeat = 1000000,
                      size_t min_time_per_inner_ns = 30000) {
  static thread_local event_collector collector;
  auto fn = std::forward<Function>(function);
  size_t N = min_repeat;
  constexpr size_t max_inner_M = 10000;
  // if function() is too fast, repeat it M times to get a measurable time.
  size_t M = 1;
  call_ntimes_runtime(fn, M); // call it once to warm up any caches, etc.
  while (M < max_inner_M) {
    collector.start();
    call_ntimes_runtime(fn, M);
    event_count allocate_count = collector.end();
    if (allocate_count.elapsed_ns() >= min_time_per_inner_ns) {
      break;
    }
    M *= 10;
    if (M >= max_inner_M) {
      M = max_inner_M;
      break;
    }
  }

  // Dispatch to compile-time specialized implementation for common M values.
  switch (M) {
  case 1:
    return bench_impl<1>(std::forward<Function>(function), min_repeat,
                         min_time_ns, max_repeat);
  case 10:
    return bench_impl<10>(std::forward<Function>(function), min_repeat,
                          min_time_ns, max_repeat);
  case 100:
    return bench_impl<100>(std::forward<Function>(function), min_repeat,
                           min_time_ns, max_repeat);
  case 1000:
    return bench_impl<1000>(std::forward<Function>(function), min_repeat,
                            min_time_ns, max_repeat);
  case 10000:
    return bench_impl<10000>(std::forward<Function>(function), min_repeat,
                             min_time_ns, max_repeat);
  default:
    // Fallback to generic runtime implementation
    throw std::runtime_error("unreachable");
    break;
  }
}

template <class Function>
event_aggregate bench(Function &&function, const bench_parameter &params) {
  return bench(std::forward<Function>(function), params.min_repeat,
               params.min_time_ns, params.max_repeat, params.min_time_per_inner_ns);
}

} // namespace counters
#endif // COUNTERS_BENCH_H_