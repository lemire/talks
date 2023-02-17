#include <iostream>
#include <memory>
#include <filesystem>
#include <fstream>
#include <cmath>

#include "simdutf.h"
#include "simdutf.cpp"

#include "event_counter.h"

std::string read_file(std::string filename) {
  constexpr auto read_size = std::size_t(4096);
  auto stream = std::ifstream(filename.c_str());
  stream.exceptions(std::ios_base::badbit);
  auto out = std::string();
  auto buf = std::string(read_size, '\0');
  while (stream.read(&buf[0], read_size)) {
    out.append(buf, 0, size_t(stream.gcount()));
  }
  out.append(buf, 0, size_t(stream.gcount()));
  return out;
}

event_collector collector;


double compute_std_dev(std::vector<double> input) {
  // compute the mean:
  double m = 0;

  for(double v : input) {
    m += v;
  }
  m /= input.size();

  double std = 0;
  for(double v : input) {
    std += (v - m) * (v - m) / input.size();
  }
  return sqrt(std);
}

// returns the average
double transcode(const std::string& source, size_t iterations) {
  size_t expected_utf16words = simdutf::utf16_length_from_utf8(source.data(), source.size());
  std::unique_ptr<char16_t[]> utf16_output{new char16_t[expected_utf16words]};
  double sum = 0;
  for(size_t i = 0; i < iterations; i++) {
    collector.start();
    size_t utf16words = simdutf::convert_utf8_to_utf16le(source.data(), source.size(), utf16_output.get());
    if(utf16words != expected_utf16words) {
      printf("bug\n");
    }
    event_count c = collector.end();
    sum += c.elapsed_ns();
  }
  return sum / iterations;
}


void print_stats(const std::string& source, size_t iterations_start, size_t iterations_end, size_t step) {
  for(size_t i = iterations_start; i <= iterations_end; i+=step) {
    std::vector<double> averages;
    for(size_t j = 0; j < 30; j++) { averages.push_back(transcode(source, i)); }
    std::cout << i << "\t" << compute_std_dev(averages) << std::endl;
  }
}

int main(int , char *[]) {
  print_stats(read_file("Arabic-Lipsum.utf8.txt"), 20, 2000, 20);
  return EXIT_SUCCESS;
}
