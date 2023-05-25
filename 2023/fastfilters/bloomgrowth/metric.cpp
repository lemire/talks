#include <iostream>

#include "bloom.h"
#include "3wise_xor_binary_fuse_filter_lowmem.h"
#include "4wise_xor_binary_fuse_filter_lowmem.h"

struct bits_fp {
    double bits_per_item;
    double fp;
};

template<size_t bits_per_item>
bits_fp measure_bloom(size_t actual_size, size_t capacity) {
    using bloom_t = bloomfilter::BloomFilter<uint64_t, bits_per_item, false, SimpleMixSplit>;
   // actual_size = 0;
    bloom_t filter(capacity);
    // assume good hashing
    for(size_t i = 0; i < actual_size; i++) {
        filter.Add(i);
    }
    size_t false_positives = 0;
    size_t total = 1000000;
    // given good hash functions, this should be fine:
    for(size_t i = actual_size; i < actual_size + total; i++) {
        uint64_t key = i;
        if(filter.Contain(key) == bloomfilter::Ok) {
            false_positives++;
        }
    }
    return {double(filter.arrayLength*sizeof(uint64_t)*8)/actual_size, double(false_positives)/total};
}

template <typename fingerprint>
bits_fp measure_binary_3wise(size_t actual_size) {
    using binaryfuse_t = xorbinaryfusefilter_lowmem::XorBinaryFuseFilter<uint64_t,fingerprint, SimpleMixSplit>;
    binaryfuse_t filter(actual_size);
    // assume good hashing
    std::vector<uint64_t> data(actual_size);
    for(size_t i = 0; i < actual_size; i++) {
        data[i] = i;
    }
    filter.AddAll(data.data(), 0, actual_size);

    size_t false_positives = 0;
    size_t total = 1000000;
    // given good hash functions, this should be fine:
    for(size_t i = actual_size; i < actual_size + total; i++) {
        if(filter.Contain(i) == xorbinaryfusefilter_lowmem::Ok) {
            false_positives++;
        }
    }
    return {double(filter.arrayLength*sizeof(fingerprint)*8)/actual_size, double(false_positives)/total};
}

template <typename fingerprint>
bits_fp measure_binary_4wise(size_t actual_size) {
    using binaryfuse_t = xorbinaryfusefilter_lowmem4wise::XorBinaryFuseFilter<uint64_t,fingerprint, SimpleMixSplit>;
    binaryfuse_t filter(actual_size);
    // assume good hashing
    std::vector<uint64_t> data(actual_size);
    for(size_t i = 0; i < actual_size; i++) {
        data[i] = i;
    }
    filter.AddAll(data.data(), 0, actual_size);

    size_t false_positives = 0;
    size_t total = 1000000;
    // given good hash functions, this should be fine:
    for(size_t i = actual_size; i < actual_size + total; i++) {
        if(filter.Contain(i) == xorbinaryfusefilter_lowmem4wise::Ok) {
            false_positives++;
        }
    }
    return {double(filter.arrayLength*sizeof(fingerprint)*8)/actual_size, double(false_positives)/total};
}

int main() {
    // 1000000 items
    size_t final_size = 1000000;
    for(size_t size = 1000; size <= 10*final_size; size*=1.4) {
        auto [bits_per_item, fp] = measure_bloom<12>(size, final_size);
        auto [bits_per_item_set, fp_set] = measure_bloom<12>(size, size);
        auto [bits_per_item_bin, fp_bin] = measure_binary_3wise<uint8_t>(size);
        auto [bits_per_item_bin4, fp_bin4] = measure_binary_4wise<uint8_t>(size);

        std::cout << size << "\t" << bits_per_item << " " << fp << "\t "<< bits_per_item_set << " " << fp_set << "\t " << bits_per_item_bin << " " << fp_bin << "\t " << bits_per_item_bin4 << " " << fp_bin4 << "\n";
    }
}