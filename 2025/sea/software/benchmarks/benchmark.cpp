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

#include "curlbench.h"
#include "shufflebench.h"

void pretty_print(const std::string& name,
                  event_aggregate agg) {
  fmt::print("{:<50} : ", name);
  fmt::print(" {:5.2f} s ", agg.fastest_elapsed_ns()/1000'000'000.0);
  if (collector.has_events()) {
    fmt::print(" {:5.2f} GHz ", agg.fastest_cycles() / agg.fastest_elapsed_ns());
    fmt::print(" {:5.2f} Mc ", agg.fastest_cycles()/ 1000'000.0);
    fmt::print(" {:5.2f} Mi ", agg.fastest_instructions()/ 1000'000.0);
    fmt::print(" {:5.2f} i/c ", agg.fastest_instructions() / agg.fastest_cycles());
  }
  fmt::print("\n");
}

int main(int argc, char **argv) {
  for (size_t i = 0; i < 4; i++) {

    fmt::print("Run {}\n", i + 1);

    std::vector<int> values(100'000'000);
    pretty_print("shuffle_100M",
                 bench([&values]() {
                  shuffle(values);
                 }));
    values.resize(10'000'000);
    pretty_print("shuffle_10M",
                 bench([&values]() {
                  shuffle(values);
                 }));
    values.resize(1'000'000);
    pretty_print("shuffle_1M",
                 bench([&values]() {
                  shuffle(values);
                 }));
    pretty_print("load_rss_feed",
                 bench([]() {load_rss_feed();
                 }));
                }
}
