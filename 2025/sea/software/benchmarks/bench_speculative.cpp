#include "benchmarker.h"
#include <vector>
#include <fmt/core.h>
#include <cstdint>
#include <span>
#include <random>


bool is_valid_utf16(const std::span<uint16_t> code_units) {
    size_t i = 0;
    while (i < code_units.size()) {
        uint16_t unit = code_units[i];
        if (unit <= 0xD7FF || unit >= 0xE000 ) {
            ++i; continue;
        }
        if (unit >= 0xD800 && unit <= 0xDBFF) {
            if (i + 1 >= code_units.size()) {
                return false; // Missing low surrogate
            }
            uint16_t next_unit = code_units[i + 1];
            if (next_unit < 0xDC00 || next_unit > 0xDFFF) {
                return false; // Invalid low surrogate
            }
            i += 2; // Valid surrogate pair
            continue;
        }
        return false;
    }
    return true;
}

void pretty_print(const std::string& name, size_t num_values,
                  event_aggregate agg, bool print_header = false) {
  if (print_header) {
    fmt::print("| size | ns/value | GHz | cycles/value | instr/value | i/c |\n");
    fmt::print("|------|---------:|-----:|-------------:|------------:|-----:|\n");
  }
  fmt::print("| {:>6} ", name);
  fmt::print("| {:9.2f} ", agg.fastest_elapsed_ns() / num_values);
  if (collector.has_events()) {
    fmt::print("| {:7.2f} ", agg.fastest_cycles() / agg.fastest_elapsed_ns());
    fmt::print("| {:13.2f} ", agg.fastest_cycles()/ num_values);
    fmt::print("| {:12.2f} ", agg.fastest_instructions()/ num_values);
    fmt::print("| {:5.2f} ", agg.fastest_instructions() / agg.fastest_cycles());
  } else {
    fmt::print("|   n/a   |     n/a      |     n/a     |  n/a |");
  }
  fmt::print("|\n");
}

std::vector<uint16_t> get(size_t max_size) {
    std::vector<uint16_t> mixed_utf16;
    mixed_utf16.reserve(max_size);

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, 1);
    size_t i = 0;
    while (i < max_size) {
        int kind = dist(rng);
        if (kind == 0 && i + 1 < max_size) {
            // Add a valid surrogate pair
            mixed_utf16.push_back(0xD800 + (rng() % 0x400)); // high surrogate
            mixed_utf16.push_back(0xDC00 + (rng() % 0x400)); // low surrogate
            i += 2;
        } else if (kind == 1) {
            // Add a lone BMP value
            mixed_utf16.push_back(0x0041 + (rng() % 0x1000));
            i++;
        }
    }
    return mixed_utf16;
}

void append_to_max_size(std::vector<uint16_t>& mixed_utf16, size_t max_size) {
    if (mixed_utf16.empty() || max_size <= mixed_utf16.size()) {
        return;
    }

    size_t initial_size = mixed_utf16.size();
    size_t repeats = max_size / initial_size;

    mixed_utf16.reserve(max_size);
    for (size_t i = 1; i < repeats; ++i) {
        mixed_utf16.insert(mixed_utf16.end(), mixed_utf16.begin(), mixed_utf16.begin() + initial_size);
    }
}
int main() {
    constexpr size_t max_size = 1 << 20; 
    bool header_printed = false;
    for (size_t size = max_size; size >= 64; size /= 2) {
        std::vector<uint16_t> mixed_utf16 = get(size);
        append_to_max_size(mixed_utf16, max_size);
        auto agg = bench([&mixed_utf16]() {
            volatile bool ok = is_valid_utf16(std::span<uint16_t>(mixed_utf16.data(), mixed_utf16.size()));
            (void)ok;
        });
        pretty_print(std::to_string(size), mixed_utf16.size(), agg, !header_printed);
        header_printed = true;
    }
    return 0;
}
