#include "benchmarker.h"
#include <vector>
#include <random>
#include <fmt/core.h>
#include <cstdint>
#include <span>

#if defined(__aarch64__) || defined(__ARM_NEON) || defined(__ARM_NEON__)
#include "utf16neon.h"
#endif
bool is_valid_utf16_ff(const std::span<uint16_t> code_units) {
    // Transition table: indexed by high byte, maps current state to next state
    // 0 = Initial, 1 = LowSurrogate, 2 = Invalid (sticky)
    static constexpr uint8_t transition_table[3][256] = {
        // State 0 (Initial)
        {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x00-0x0F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x10-0x1F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x20-0x2F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x30-0x3F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x40-0x4F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x50-0x5F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x60-0x6F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x70-0x7F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x80-0x8F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x90-0x9F
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xA0-0xAF
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xB0-0xBF
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xC0-0xCF
            0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, // 0xD0-0xDF
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xE0-0xEF
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  // 0xF0-0xFF
        },
        // State 1 (LowSurrogate)
        {
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x00-0x0F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x10-0x1F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x20-0x2F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x30-0x3F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x40-0x4F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x50-0x5F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x60-0x6F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x70-0x7F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x80-0x8F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x90-0x9F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xA0-0xAF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xB0-0xBF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xC0-0xCF
            2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, // 0xD0-0xDF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xE0-0xEF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2  // 0xF0-0xFF
        },
        // State 255 (Invalid, sticky)
        {
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x00-0x0F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x10-0x1F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x20-0x2F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x30-0x3F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x40-0x4F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x50-0x5F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x60-0x6F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x70-0x7F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x80-0x8F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0x90-0x9F
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xA0-0xAF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xB0-0xBF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xC0-0xCF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xD0-0xDF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0xE0-0xEF
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2  // 0xF0-0xFF
        }
    };

    uint8_t state = 0; // Start in Initial state
    for (size_t i = 0; i < code_units.size(); ++i) {
        uint8_t high_byte = code_units[i] >> 8;
        state = transition_table[state][high_byte];
    }
    return state == 0; // Valid only if we end in Initial state
}

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
                  event_aggregate agg) {
  fmt::print("{:<50} : ", name);
  fmt::print(" {:5.2f} ns ", agg.fastest_elapsed_ns()/num_values);
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

    std::vector<uint16_t> valid_utf16(num_values, 0x0041); // 'A' repeated

    // Mixed random (déjà présent)
    std::vector<uint16_t> mixed_utf16;
    mixed_utf16.reserve(num_values);
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, 1);
    size_t i = 0;
    while (i < num_values) {
        int kind = dist(rng);
        if (kind == 0 && i + 1 < num_values) {
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

    // Mixed alterné (alternance stricte)
    std::vector<uint16_t> mixed_utf16_alternate;
    mixed_utf16_alternate.reserve(num_values);
    size_t j = 0;
    bool add_pair = true;
    while (j < num_values) {
        if (add_pair && j + 1 < num_values) {
            mixed_utf16_alternate.push_back(0xD800 + ((j/2) % 0x400)); // high surrogate
            mixed_utf16_alternate.push_back(0xDC00 + ((j/2) % 0x400)); // low surrogate
            j += 2;
        } else {
            mixed_utf16_alternate.push_back(0x0041 + (j % 0x1000));
            j++;
        }
        add_pair = !add_pair;
    }
    

    for (int i = 0; i < 4; ++i) {
        fmt::print("Run {}\n", i + 1);

        auto valid_agg = bench([&valid_utf16]() {
            volatile bool ok = is_valid_utf16(std::span<uint16_t>(valid_utf16));
            (void)ok;
        });
        pretty_print("is_valid_utf16 (valid)", num_values, valid_agg);

        auto valid_ff_agg = bench([&valid_utf16]() {
            volatile bool ok = is_valid_utf16_ff(std::span<uint16_t>(valid_utf16));
            (void)ok;
        });
        pretty_print("is_valid_utf16_ff (valid)", num_values, valid_ff_agg);

        auto mixed_agg = bench([&mixed_utf16]() {
            volatile bool ok = is_valid_utf16(std::span<uint16_t>(mixed_utf16));
            (void)ok;
        });
        pretty_print("is_valid_utf16 (mixed, random)", num_values, mixed_agg);

        auto mixed_ff_agg = bench([&mixed_utf16]() {
            volatile bool ok = is_valid_utf16_ff(std::span<uint16_t>(mixed_utf16));
            (void)ok;
        });
        pretty_print("is_valid_utf16_ff (mixed, random)", num_values, mixed_ff_agg);

        auto mixed_alt_agg = bench([&mixed_utf16_alternate]() {
            volatile bool ok = is_valid_utf16(std::span<uint16_t>(mixed_utf16_alternate));
            (void)ok;
        });
        pretty_print("is_valid_utf16 (mixed, alternate)", num_values, mixed_alt_agg);

        auto mixed_alt_ff_agg = bench([&mixed_utf16_alternate]() {
            volatile bool ok = is_valid_utf16_ff(std::span<uint16_t>(mixed_utf16_alternate));
            (void)ok;
        });
        pretty_print("is_valid_utf16_ff (mixed, alternate)", num_values, mixed_alt_ff_agg);
#if defined(__aarch64__) || defined(__ARM_NEON) || defined(__ARM_NEON__)
        std::vector<uint16_t> output_utf16;
        output_utf16.reserve(num_values);

        auto mixed_simd_agg = bench([&mixed_utf16,&output_utf16]() {
            utf16fix_neon_64bits(reinterpret_cast<const char16_t*>(mixed_utf16.data()), num_values, reinterpret_cast<char16_t*>(output_utf16.data()));
        });
        pretty_print("fix mixed_simd_agg (mixed, random)", num_values, mixed_simd_agg);
#endif
    }
    return 0;
}
