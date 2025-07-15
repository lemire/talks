#include "benchmarker.h"
#include <vector>
#include <algorithm>
#include <numeric>
#include <fmt/core.h>


__uint128_t g_lehmer64_state = UINT64_C(0x853c49e6748fea9b);

/**
 * D. H. Lehmer, Mathematical methods in large-scale computing units.
 * Proceedings of a Second Symposium on Large Scale Digital Calculating
 * Machinery;
 * Annals of the Computation Laboratory, Harvard Univ. 26 (1951), pp. 141-146.
 */
static inline uint64_t lehmer64() {
  g_lehmer64_state *= UINT64_C(0xda942042e4dd58b5);
  return (uint64_t)(g_lehmer64_state >> 64);
}


uint64_t java_random_bounded(uint64_t bound) {
  uint64_t rkey = lehmer64();
  uint64_t candidate = rkey % bound;
  while (rkey - candidate >
         UINT64_MAX - bound + 1) {
    rkey = lehmer64();
    candidate = rkey % bound;
  }
  return candidate;
}


static inline uint64_t random_bounded_nearlydivisionless64(uint64_t range) {
  __uint128_t random64bit, multiresult;
  uint64_t leftover;
  uint64_t threshold;
  random64bit = lehmer64();
  multiresult = random64bit * range;
  leftover = (uint64_t)multiresult;
  if (leftover < range) {
    threshold = -range % range;
    while (leftover < threshold) {
      random64bit = lehmer64();
      multiresult = random64bit * range;
      leftover = (uint64_t)multiresult;
    }
  }
  return multiresult >> 64; // [0, range)
}



void pretty_print(const std::string& name, size_t num_values, event_aggregate agg) {
  fmt::print("{:<40} : ", name);
  fmt::print(" {:5.2f} ns ", agg.fastest_elapsed_ns() / num_values);
  if (collector.has_events()) {
    fmt::print(" {:5.2f} GHz ", agg.fastest_cycles() / agg.fastest_elapsed_ns());
    fmt::print(" {:5.2f} c ", agg.fastest_cycles()/ num_values);
    fmt::print(" {:5.2f} i ", agg.fastest_instructions()/ num_values);
    fmt::print(" {:5.2f} i/c ", agg.fastest_instructions() / agg.fastest_cycles());
  }
  fmt::print("\n");
}

int main() {
    constexpr size_t num_values = 1'000'000;
    std::vector<uint64_t> data(num_values);
    std::iota(data.begin(), data.end(), 0);

    for (int i = 0; i < 4; ++i) {
        fmt::print("Run {}\n", i + 1);

        // Shuffle with random_bounded_nearlydivisionless64
        auto arr1 = data;
        auto bench1 = bench([&arr1]() {
            for (size_t j = arr1.size() - 1; j > 0; --j) {
                size_t k = random_bounded_nearlydivisionless64(j + 1);
                std::swap(arr1[j], arr1[k]);
            }
        });
        pretty_print("shuffle (nearlydivisionless64)", num_values, bench1);

        // Shuffle with java_random_bounded
        auto arr2 = data;
        auto bench2 = bench([&arr2]() {
            for (size_t j = arr2.size() - 1; j > 0; --j) {
                size_t k = java_random_bounded(j + 1);
                std::swap(arr2[j], arr2[k]);
            }
        });
        pretty_print("shuffle (java_random_bounded)", num_values, bench2);
    }
    return 0;
}
