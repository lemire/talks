#include "benchmarker.h"
#include <vector>
#include <random>
#include <fmt/core.h>

void pretty_print(const std::string& name, size_t num_values, event_aggregate agg) {
  fmt::print("{:<20} : ", name);
  fmt::print(" {:5.2f} ns ", agg.fastest_elapsed_ns() / num_values);
  if (collector.has_events()) {
    fmt::print(" {:5.2f} GHz ", agg.fastest_cycles() / agg.fastest_elapsed_ns());
    fmt::print(" {:5.2f} c ", agg.fastest_cycles()/ num_values);
    fmt::print(" {:5.2f} i ", agg.fastest_instructions()/ num_values);
    fmt::print(" {:5.2f} i/c ", agg.fastest_instructions() / agg.fastest_cycles());
  }
  fmt::print("\n");
}

uint64_t scalar(uint32_t *x, uint32_t *y, size_t length) {
  uint64_t sum = 0;
  for (size_t i = 0; i < length; i++)
    sum += (uint64_t)x[i] * y[i];
  return sum;
}

uint64_t scalar4(uint32_t *x, uint32_t *y, size_t length) {
  uint64_t sum = 0;
  size_t i = 0;
  if (length > 3)
    for (; i < length - 3; i += 4)
      sum += (uint64_t)x[i] * y[i] + (uint64_t)x[i + 1] * y[i + 1] +
             (uint64_t)x[i + 2] * y[i + 2] + (uint64_t)x[i + 3] * y[i + 3];
  for (; i < length; i++)
    sum += (uint64_t)x[i] * y[i];
  return sum;
}


int main() {
    constexpr size_t num_values = 1'000'000;
    std::vector<uint32_t> x(num_values), y(num_values);
    std::mt19937 rng(42);
    std::uniform_int_distribution<uint32_t> dist(0, 1000000);
    for (size_t i = 0; i < num_values; ++i) {
        x[i] = dist(rng);
        y[i] = dist(rng);
    }

    for (int i = 0; i < 4; ++i) {
        fmt::print("Run {}\n", i + 1);

        auto agg_scalar = bench([&x, &y]() {
            volatile uint64_t s = scalar(const_cast<uint32_t*>(x.data()), const_cast<uint32_t*>(y.data()), x.size());
            (void)s;
        });
        pretty_print("scalar", num_values, agg_scalar);

        auto agg_scalar4 = bench([&x, &y]() {
            volatile uint64_t s = scalar4(const_cast<uint32_t*>(x.data()), const_cast<uint32_t*>(y.data()), x.size());
            (void)s;
        });
        pretty_print("scalar4", num_values, agg_scalar4);
    }
    return 0;
}