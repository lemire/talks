// Benchmark: ASCII to-lower, scalar (one branch per byte) vs AVX-512 (64 bytes per iteration).
// Companion to the llvm-mca slides: same two kernels, measured on real hardware with
// hardware performance counters (https://github.com/lemire/counters, vendored in ./counters).
//
// Build:  g++ -O2 -march=x86-64-v4 -Icounters/include tolower_bench.cpp -o tolower_bench
// Run:    ./tolower_bench            (prints CSV to stdout)
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <immintrin.h>
#include <string>
#include <vector>

#include "counters/bench.h"

// Scalar loop as on the slide: one byte per iteration, one branch per byte.
// The attribute keeps GCC from autovectorizing it and keeps the branch a branch.
__attribute__((noinline, optimize("no-tree-vectorize")))
void tolower_scalar(uint8_t *data, size_t n) {
  for (size_t i = 0; i < n; i++) {
    uint8_t c = data[i];
    if (uint8_t(c - 'A') < 26) { // unsigned compare: c in ['A','Z']
      data[i] = c + ('a' - 'A');
    }
  }
}

// AVX-512 loop as on the slide: 64 bytes per iteration, no branch on the data.
__attribute__((noinline))
void tolower_avx512(uint8_t *data, size_t n) {
  const __m512i A = _mm512_set1_epi8('A');
  const __m512i Z_A = _mm512_set1_epi8('Z' - 'A');
  const __m512i a_A = _mm512_set1_epi8('a' - 'A');
  size_t i = 0;
  for (; i + 64 <= n; i += 64) {
    __m512i c = _mm512_loadu_si512(data + i);
    __m512i ca = _mm512_sub_epi8(c, A);
    __mmask64 is_upper = _mm512_cmple_epu8_mask(ca, Z_A);
    c = _mm512_mask_add_epi8(c, is_upper, c, a_A);
    _mm512_storeu_si512(data + i, c);
  }
  if (i < n) { // tail: same three instructions under a load/store mask
    __mmask64 tail = (n - i >= 64) ? ~0ULL : ((1ULL << (n - i)) - 1);
    __m512i c = _mm512_maskz_loadu_epi8(tail, data + i);
    __m512i ca = _mm512_sub_epi8(c, A);
    __mmask64 is_upper = _mm512_cmple_epu8_mask(ca, Z_A);
    c = _mm512_mask_add_epi8(c, is_upper, c, a_A);
    _mm512_mask_storeu_epi8(data + i, tail, c);
  }
}

// Deterministic English-looking ASCII: words of lowercase letters, spaces, some punctuation.
// `upper_fraction` of the letters are uppercased at random, which is what the scalar
// branch has to predict.
static std::vector<uint8_t> make_text(size_t n, double upper_fraction, uint64_t seed) {
  std::vector<uint8_t> out(n);
  uint64_t s = seed;
  auto rnd = [&]() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; };
  size_t word_left = 0;
  for (size_t i = 0; i < n; i++) {
    if (word_left == 0) {
      uint64_t r = rnd();
      out[i] = (r % 16 == 0) ? '.' : ' ';
      word_left = 2 + r % 8;
      continue;
    }
    uint64_t r = rnd();
    uint8_t c = 'a' + r % 26;
    if ((r >> 8) % 1000 < upper_fraction * 1000) c -= 'a' - 'A';
    out[i] = c;
    word_left--;
  }
  return out;
}

// The AVX-512 kernel's timing does not depend on the data (no branch on the data), so it is
// measured in place on an already-lowercased buffer: no memcpy, no subtraction, no noise.
// The scalar kernel's timing depends on the data (branch prediction), so each iteration
// lowercases a fresh copy; the memcpy is timed separately and subtracted. That subtraction
// adds noise of the order of 100-200 cycles, negligible against a scalar run (>= 10k cycles).
struct kernel { const char *name; void (*fn)(uint8_t *, size_t); bool in_place; };

int main() {
  const kernel kernels[] = {{"scalar", tolower_scalar, false}, {"avx512", tolower_avx512, true}};
  const size_t sizes[] = {16 << 10, 1 << 20, 16 << 20, 256 << 20};
  const double upper_fractions[] = {0.0, 0.5};

  if (!counters::has_performance_counters()) {
    fprintf(stderr, "warning: no performance counters (cycles/instructions will be 0)\n");
  }
  printf("kernel,bytes,upper_fraction,ns_per_byte,cycles_per_byte,instructions_per_byte,ipc,"
         "branch_misses_per_kbyte,GHz,GBps\n");
  for (double uf : upper_fractions) {
    for (size_t n : sizes) {
      std::vector<uint8_t> text = make_text(n, uf, 0x9E3779B97F4A7C15ULL);
      // 64-byte aligned working buffer: an unaligned 64-byte load/store straddles two cache
      // lines and costs about one extra cycle per iteration, which llvm-mca does not model.
      // (std::vector only guarantees 16-byte alignment, so this would otherwise be luck.)
      struct aligned_buf {
        uint8_t *p;
        explicit aligned_buf(size_t n) : p((uint8_t *)std::aligned_alloc(64, (n + 63) / 64 * 64)) {}
        ~aligned_buf() { std::free(p); }
        uint8_t *data() { return p; }
      } work(n);
      for (const kernel &k : kernels) {
        counters::bench_parameter p;
        p.min_time_ns = 1'000'000'000; // 1 s warm-up target
        // sanity check on a fresh copy
        memcpy(work.data(), text.data(), n);
        k.fn(work.data(), n);
        for (size_t i = 0; i < n; i++) {
          uint8_t c = text[i];
          if (uint8_t(c - 'A') < 26) c += 'a' - 'A';
          if (work.data()[i] != c) { fprintf(stderr, "%s: mismatch at %zu\n", k.name, i); return 1; }
        }
        double ns, cyc, ins, bm;
        if (k.in_place) {
          auto agg = counters::bench([&] { k.fn(work.data(), n); }, p);
          ns = agg.elapsed_ns(); cyc = agg.cycles(); ins = agg.instructions(); bm = agg.branch_misses();
        } else {
          auto copy_only = counters::bench([&] { memcpy(work.data(), text.data(), n); }, p);
          auto agg = counters::bench([&] {
            memcpy(work.data(), text.data(), n);
            k.fn(work.data(), n);
          }, p);
          ns = agg.elapsed_ns() - copy_only.elapsed_ns();
          cyc = agg.cycles() - copy_only.cycles();
          ins = agg.instructions() - copy_only.instructions();
          bm = agg.branch_misses() - copy_only.branch_misses();
        }
        printf("%s,%zu,%.2f,%.4f,%.4f,%.4f,%.3f,%.3f,%.2f,%.2f\n", k.name, n, uf,
               ns / n, cyc / n, ins / n, ins / cyc, bm / n * 1024, cyc / ns, n / ns);
        fflush(stdout);
      }
    }
  }
  return 0;
}
