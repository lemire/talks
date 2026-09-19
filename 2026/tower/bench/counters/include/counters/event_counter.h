#ifndef COUNTERS__EVENT_COUNTER_H
#define COUNTERS__EVENT_COUNTER_H

#include <cctype>
#ifndef _MSC_VER
#include <dirent.h>
#endif
#include <cinttypes>

#include <cstring>

#include <chrono>
#include <vector>

#include "linux-perf-events.h"
#ifdef __linux__
#include <libgen.h>
#endif

#if defined(__APPLE__) && defined(__aarch64__)
#include "apple_arm_events.h"
#endif

namespace counters {
struct event_count {
  std::chrono::duration<double> elapsed;
  std::vector<unsigned long long> event_counts;
  event_count() : elapsed(0), event_counts{0, 0, 0, 0, 0} {}
  event_count(const std::chrono::duration<double> _elapsed,
              const std::vector<unsigned long long> _event_counts)
      : elapsed(_elapsed), event_counts(_event_counts) {}
  event_count(const event_count &other)
      : elapsed(other.elapsed), event_counts(other.event_counts) {}

  // The types of counters (so we can read the getter more easily)
  enum event_counter_types {
    CPU_CYCLES,
    INSTRUCTIONS,
    BRANCH,
    BRANCH_MISSES,
    CACHE_MISSES
  };

  double elapsed_sec() const {
    return std::chrono::duration<double>(elapsed).count();
  }
  double elapsed_ns() const {
    return std::chrono::duration<double, std::nano>(elapsed).count();
  }
  double cycles() const {
    return static_cast<double>(event_counts[CPU_CYCLES]);
  }
  double instructions() const {
    return static_cast<double>(event_counts[INSTRUCTIONS]);
  }
  double branch_misses() const {
    return static_cast<double>(event_counts[BRANCH_MISSES]);
  }
  double branches() const { return static_cast<double>(event_counts[BRANCH]); }
  double cache_misses() const {
    return static_cast<double>(event_counts[CACHE_MISSES]);
  }

  event_count &operator=(const event_count &other) {
    this->elapsed = other.elapsed;
    this->event_counts = other.event_counts;
    return *this;
  }
  event_count operator+(const event_count &other) const {
    return event_count(elapsed + other.elapsed,
                       {
                           event_counts[0] + other.event_counts[0],
                           event_counts[1] + other.event_counts[1],
                           event_counts[2] + other.event_counts[2],
                           event_counts[3] + other.event_counts[3],
                           event_counts[4] + other.event_counts[4],
                       });
  }

  void operator+=(const event_count &other) { *this = *this + other; }
};

struct event_aggregate {
  bool has_events = false;
  int iterations = 0;
  int inner_count = 1; // Number of inner iterations
  event_count total{};
  event_count best{};
  event_count worst{};
  template <typename T> event_aggregate &operator/=(T divisor) {
    total.elapsed /= double(divisor);
    for (size_t i = 0; i < total.event_counts.size(); i++) {
      total.event_counts[i] /= double(divisor);
    }
    return *this;
  }

  event_aggregate() = default;

  void operator<<(const event_count &other) {
    if (iterations == 0 || other.elapsed < best.elapsed) {
      best = other;
    }
    if (iterations == 0 || other.elapsed > worst.elapsed) {
      worst = other;
    }
    iterations++;
    total += other;
  }

  double elapsed_sec() const { return total.elapsed_sec() / iterations / inner_count; }
  double total_elapsed_ns() const { return total.elapsed_ns(); }
  double elapsed_ns() const { return total.elapsed_ns() / iterations / inner_count; }
  double cycles() const { return total.cycles() / iterations / inner_count; }
  double branch_misses() const { return total.branch_misses() / iterations / inner_count; }
  double branches() const { return total.branches() / iterations / inner_count; }
  double instructions() const { return total.instructions() / iterations / inner_count; }
  double cache_misses() const { return total.cache_misses() / iterations / inner_count; }
  double fastest_elapsed_ns() const { return best.elapsed_ns() / inner_count; }
  double fastest_cycles() const { return best.cycles() / inner_count; }
  double fastest_instructions() const { return best.instructions() / inner_count; }
  double fastest_branch_misses() const { return best.branch_misses() / inner_count; }
  double fastest_branches() const { return best.branches() / inner_count; }
  double fastest_cache_misses() const { return best.cache_misses() / inner_count; }
  int iteration_count() const { return iterations; }
  int inner_iteration_count() const { return inner_count; }
};

struct event_collector {
  event_count count{};
  std::chrono::time_point<std::chrono::steady_clock> start_clock{};

#if defined(__linux__)
  LinuxEvents<PERF_TYPE_HARDWARE> linux_events;
  event_collector()
      : linux_events(std::vector<int>{
            PERF_COUNT_HW_CPU_CYCLES,
            PERF_COUNT_HW_INSTRUCTIONS,
            PERF_COUNT_HW_BRANCH_INSTRUCTIONS, // Retired branch instructions
            PERF_COUNT_HW_BRANCH_MISSES,
            PERF_COUNT_HW_CACHE_MISSES,
        }) {}
  bool has_events() { return linux_events.is_working(); }
#elif defined(__APPLE__) && defined(__aarch64__)
  AppleEvents apple_events;
  performance_counters diff;
  event_collector() : diff(0) { apple_events.setup_performance_counters(); }
  bool has_events() { return apple_events.setup_performance_counters(); }
#else
  event_collector() {}
  bool has_events() { return false; }
#endif

  inline void start() {
#if defined(__linux)
    linux_events.start();
#elif defined(__APPLE__) && defined(__aarch64__)
    if (has_events()) {
      diff = apple_events.get_counters();
    }
#endif
    start_clock = std::chrono::steady_clock::now();
  }
  inline event_count &end() {
    const auto end_clock = std::chrono::steady_clock::now();
#if defined(__linux)
    linux_events.end(count.event_counts);
#elif __APPLE__ && __aarch64__
    if (has_events()) {
      performance_counters end = apple_events.get_counters();
      diff = end - diff;
    }
    count.event_counts[0] = diff.cycles;
    count.event_counts[1] = diff.instructions;
    count.event_counts[2] = diff.branches;
    count.event_counts[3] = diff.missed_branches;
    count.event_counts[4] = diff.cache_misses;
#endif
    count.elapsed = end_clock - start_clock;
    return count;
  }
};

inline bool has_performance_counters() {
  return counters::event_collector().has_events();
}

} // namespace counters
#endif