#include "benchmarker.h"
#include <algorithm>
#include <numeric>
#include <cstddef>
#include <cstdio>
#include <fmt/core.h>
#include <span>

namespace array_ops {
// Unrolled by 4: successive differences from src to dst
template <typename T>
__attribute__((noinline))
constexpr void successive_differences_to_unrolled(std::span<const T> src, std::span<T> dst) {
    if (src.size() == 0 || dst.size() == 0) return;
    size_t n = std::min(src.size(), dst.size());
    if (n == 0) return;
    dst[0] = src[0];
    size_t i = 1;
    // Unroll by 4
    for (; i + 3 < n; i += 4) {
        dst[i]   = src[i]   - src[i-1];
        dst[i+1] = src[i+1] - src[i];
        dst[i+2] = src[i+2] - src[i+1];
        dst[i+3] = src[i+3] - src[i+2];
    }
    for (; i < n; ++i) {
        dst[i] = src[i] - src[i-1];
    }
}

// Unrolled by 4: prefix sum from src to dst
template <typename T>
__attribute__((noinline))
constexpr void prefix_sum_to_unrolled(std::span<const T> src, std::span<T> dst) {
    if (src.size() == 0 || dst.size() == 0) return;
    size_t n = std::min(src.size(), dst.size());
    if (n == 0) return;
    dst[0] = src[0];
    size_t i = 1;
    // Unroll by 4
    for (; i + 3 < n; i += 4) {
        dst[i]   = dst[i-1]   + src[i];
        dst[i+1] = dst[i]     + src[i+1];
        dst[i+2] = dst[i+1]   + src[i+2];
        dst[i+3] = dst[i+2]   + src[i+3];
    }
    for (; i < n; ++i) {
        dst[i] = dst[i-1] + src[i];
    }
}
// Computes successive differences from src to dst
// Example: src = [1, 3, 6, 8] -> dst = [1, 2, 3, 2]
template <typename T>
__attribute__((noinline)) 
constexpr void successive_differences_to(std::span<const T> src, std::span<T> dst) {
    if (src.size() == 0 || dst.size() == 0) return;
    size_t n = std::min(src.size(), dst.size());
    if (n == 0) return;
    dst[0] = src[0];
    for (size_t i = 1; i < n; ++i) {
        dst[i] = src[i] - src[i - 1];
    }
}

// Computes prefix sum from src to dst
// Example: src = [1, 2, 3, 2] -> dst = [1, 3, 6, 8]
template <typename T>
__attribute__((noinline)) 
constexpr void prefix_sum_to(std::span<const T> src, std::span<T> dst) {
    if (src.size() == 0 || dst.size() == 0) return;
    size_t n = std::min(src.size(), dst.size());
    if (n == 0) return;
    dst[0] = src[0];
    for (size_t i = 1; i < n; ++i) {
        dst[i] = dst[i - 1] + src[i];
    }
}
// Computes successive differences of the array in-place
// Example: [1, 3, 6, 8] -> [1, 2, 3, 2]
template <typename T>
__attribute__((noinline)) 
constexpr void successive_differences(std::span<T> arr) {
    if (arr.size() <= 1) return;
    for (size_t i = arr.size() - 1; i > 0; --i) {
        arr[i] = arr[i] - arr[i - 1];
    }
}

// Computes prefix sum of the array in-place
// Example: [1, 2, 3, 2] -> [1, 3, 6, 8]
template <typename T>
__attribute__((noinline)) 
constexpr void prefix_sum(std::span<T> arr) {
    if (arr.size() <= 1) return;
    for (size_t i = 1; i < arr.size(); ++i) {
        arr[i] = arr[i] + arr[i - 1];
    }
}
} // namespace array_ops



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
    constexpr size_t num_values = 1'000'000;
    std::vector<int> values(num_values);

    std::iota(values.begin(), values.end(), 1); // Fill with 1, 2, ..., num_values

    for (size_t i = 0; i < 4; i++) {
        fmt::print("Run {}\n", i + 1);

        // In-place successive differences
        auto diff_agg = bench([&values]() {
            auto arr = values;
            array_ops::successive_differences(std::span<int>(arr));
        });
        pretty_print("successive_differences (in-place)", num_values, diff_agg);

        // In-place prefix sum
        auto prefix_agg = bench([&values]() {
            auto arr = values;
            array_ops::prefix_sum(std::span<int>(arr));
        });
        pretty_print("prefix_sum (in-place)", num_values, prefix_agg);
        std::vector<int> dst(values.size());

        // Out-of-place successive differences
        auto diff_dst_agg = bench([&values, &dst]() {
            array_ops::successive_differences_to(std::span<const int>(values), std::span<int>(dst));
        });
        pretty_print("successive_differences (dst)", num_values, diff_dst_agg);

        // Out-of-place prefix sum
        auto prefix_dst_agg = bench([&values, &dst]() {
            array_ops::prefix_sum_to(std::span<const int>(values), std::span<int>(dst));
        });
        pretty_print("prefix_sum (dst)", num_values, prefix_dst_agg);
        // Out-of-place successive differences
        auto diff_dst_agg_u = bench([&values, &dst]() {
            array_ops::successive_differences_to_unrolled(std::span<const int>(values), std::span<int>(dst));
        });
        pretty_print("successive_differences (dst, unrolled)", num_values, diff_dst_agg_u);

        // Out-of-place prefix sum
        auto prefix_dst_agg_u = bench([&values, &dst]() {
            array_ops::prefix_sum_to_unrolled(std::span<const int>(values), std::span<int>(dst));
        });
        pretty_print("prefix_sum (dst, unrolled)", num_values, prefix_dst_agg_u);
    }
}