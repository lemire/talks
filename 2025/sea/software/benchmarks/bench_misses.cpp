#include "benchmarker.h"
#include <vector>
#include <random>
#include <fmt/core.h>
#include <cstdint>

static inline uint64_t rng(uint64_t h) {
  h ^= h >> 33;
  h *= UINT64_C(0xff51afd7ed558ccd);
  h ^= h >> 33;
  h *= UINT64_C(0xc4ceb9fe1a85ec53);
  h ^= h >> 33;
  return h;
}

__attribute__((noinline)) void sum_random(uint64_t howmany, uint64_t *out) {
  for (uint64_t i = 0; i < howmany; ++i) {
    out[i] = rng(i);
  }
}

__attribute__((noinline)) void cond_sum_random(uint64_t howmany, uint64_t *out) {
  uint64_t j = 0;
  for (uint64_t i = 0; i < howmany; ++i) {
    uint64_t randomval = rng(i);
    if ((randomval & 1) == 1) out[j++] = randomval;
  }
}

__attribute__((noinline)) void mask_sum_random(uint64_t howmany, uint64_t *out) {
  uint64_t j = 0;
  for (uint64_t i = 0; i < howmany; ++i) {
    uint64_t randomval = rng(i);
    out[j] = randomval;
    j += (randomval & 1);
  }
}


void print_markdown_row(size_t num_values, double miss_percent) {
    fmt::print("| {} | {:.1f} |\n", num_values, miss_percent);
}

int main() {
    fmt::print("| entries | % branch misses |\n");
    fmt::print("|---------|----------------:|\n");
    for (size_t num_values = 1024; num_values <= 1'048'576; num_values *= 2) {
        std::vector<uint64_t> buffer(num_values);
        auto agg_cond = bench([&buffer]() {
            cond_sum_random(buffer.size(), buffer.data());
        });
        double branch_misses = agg_cond.branch_misses();
        double miss_percent = 100.0 * branch_misses / num_values;
        print_markdown_row(num_values, miss_percent);
    }
    return 0;
}
