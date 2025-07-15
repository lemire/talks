#include "benchmarker.h"
#include <algorithm>
#include <cstddef>
#include <cstdio>
#include <fmt/core.h>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <ranges>
#include <sstream>
#include <string>
#include <unordered_map>
using std::literals::string_literals::operator""s;

#include <vector>

#include <fast_float/fast_float.h>

void pretty_print(const std::string &name, size_t num_values,
                  event_aggregate agg) {
  fmt::print("{:<50} : ", name);
  fmt::print(" {:5.2f} ns ", agg.fastest_elapsed_ns() / num_values);
  if (collector.has_events()) {
    fmt::print(" {:5.2f} GHz ",
               agg.fastest_cycles() / agg.fastest_elapsed_ns());
    fmt::print(" {:5.2f} c ", agg.fastest_cycles() / num_values);
    fmt::print(" {:5.2f} i ", agg.fastest_instructions() / num_values);
    fmt::print(" {:5.2f} i/c ",
               agg.fastest_instructions() / agg.fastest_cycles());
  }
  fmt::print("\n");
}

int main(int argc, char **argv) {
  std::vector<std::string> values;
  constexpr size_t num_values = 1'000'000;
  values.reserve(num_values);
  std::mt19937_64 rng(42); // Graine fixe pour reproductibilité
  std::uniform_real_distribution<double> dist(0.0, 1.0);
  for (size_t i = 0; i < num_values; i++) {
    double rnd = dist(rng);
    values.push_back(std::to_string(rnd));
  }
  for (size_t i = 0; i < 4; i++) {

    fmt::print("Run {}\n", i + 1);

    pretty_print("fast_float", num_values, bench([&values]() {
                   for (auto &input : values) {
                     double result;
                     auto r = fast_float::from_chars(
                         input.data(), input.data() + input.size(), result);
                     if (r.ec != std::errc()) {
                       fmt::print("Error parsing float\n");
                     }
                   }
                 }));
  }
}
