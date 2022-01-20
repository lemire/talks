#include <x86intrin.h>
#include <stdio.h>
#include <stdint.h>

int main() {
    __m128i a = _mm_setr_epi32(1,2,3,4);
    __m128i p = _mm_shuffle_epi32 (a, 0b11100100);
    uint32_t result[4];
    _mm_store_si128((__m128i*)result, p);
    printf("%u %u %u %u \n", result[0], result[1], result[2], result[3]);
    p = _mm_shuffle_epi32 (a, 0b00011011);
    _mm_store_si128((__m128i*)result, p);
    printf("%u %u %u %u \n", result[0], result[1], result[2], result[3]);
}