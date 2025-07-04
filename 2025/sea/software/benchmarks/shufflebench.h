#include <vector>
#include <random>
#include <algorithm>

void shuffle(std::span<int> values) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::shuffle(values.begin(), values.end(), gen);
}