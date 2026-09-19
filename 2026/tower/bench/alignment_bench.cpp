// Benchmark: AVX-512 to-lower on a 16 KB L1-resident buffer, for every start offset 0..63
// from a 64-byte boundary. Unaligned 64-byte loads/stores straddle two cache lines.
//
// Build:  g++ -O2 -march=x86-64-v4 -Icounters/include alignment_bench.cpp -o alignment_bench
// Run:    ./alignment_bench > results_alignment_big4.csv
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <immintrin.h>

#include "counters/bench.h"

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
  if (i < n) {
    __mmask64 tail = (1ULL << (n - i)) - 1;
    __m512i c = _mm512_maskz_loadu_epi8(tail, data + i);
    __m512i ca = _mm512_sub_epi8(c, A);
    __mmask64 is_upper = _mm512_cmple_epu8_mask(ca, Z_A);
    c = _mm512_mask_add_epi8(c, is_upper, c, a_A);
    _mm512_mask_storeu_epi8(data + i, tail, c);
  }
}

int main() {
  const size_t n = 16 << 10;
  uint8_t *base = (uint8_t *)std::aligned_alloc(64, n + 128);
  for (size_t i = 0; i < n + 128; i++) base[i] = 'a' + i % 26;
  if (!counters::has_performance_counters()) {
    fprintf(stderr, "warning: no performance counters (cycles will be 0)\n");
  }
  printf("offset,bytes,ns_per_byte,cycles_per_byte,instructions_per_byte,GHz,GBps\n");
  for (int offset = 0; offset < 64; offset++) {
    uint8_t *work = base + offset; // timing does not depend on the data: measure in place
    counters::bench_parameter p;
    p.min_time_ns = 500'000'000;
    auto agg = counters::bench([&] { tolower_avx512(work, n); }, p);
    printf("%d,%zu,%.4f,%.4f,%.4f,%.2f,%.2f\n", offset, n, agg.elapsed_ns() / n, agg.cycles() / n,
           agg.instructions() / n, agg.cycles() / agg.elapsed_ns(), n / agg.elapsed_ns());
    fflush(stdout);
  }
  std::free(base);
  return 0;
}
