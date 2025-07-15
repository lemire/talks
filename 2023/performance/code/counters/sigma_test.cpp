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


// returns the average and the min
std::pair<event_count,event_count> transcode(const std::string& source, size_t iterations) {
  std::vector<event_count> events;
  events.reserve(iterations);
  size_t expected_utf16words = simdutf::utf16_length_from_utf8(source.data(), source.size());
  std::unique_ptr<char16_t[]> utf16_output{new char16_t[expected_utf16words]};
  for(size_t i = 0; i < iterations; i++) {
    collector.start();
    size_t utf16words = simdutf::convert_utf8_to_utf16le(source.data(), source.size(), utf16_output.get());
    if(utf16words != expected_utf16words) {
      printf("bug\n");
    }
    event_count c = collector.end();
    events.push_back(c);
  }
  event_count accumul_event = events[0];
  event_count min_event = events[0];
  // We are going to compute both the min and the average
  for(size_t i = 1 ; i < events.size() ; i++) {
    event_count & e = events[i];
    accumul_event += e;
    min_event = min_event.min(e);
  }
  accumul_event = accumul_event / (unsigned long long)events.size();
  return {accumul_event, min_event};
}

double sigma_test(const std::string& source, size_t warmup, size_t iterations) {
  std::vector<double> input;
  input.reserve(iterations);
  size_t expected_utf16words = simdutf::utf16_length_from_utf8(source.data(), source.size());
  std::unique_ptr<char16_t[]> utf16_output{new char16_t[expected_utf16words]};
  for(size_t i = 0; i < iterations + warmup; i++) {
    collector.start();
    volatile size_t utf16words = simdutf::convert_utf8_to_utf16le(source.data(), source.size(), utf16_output.get());
    event_count c = collector.end();
    if(i >= warmup) { input.push_back(c.elapsed_ns()); }
  }
  // compute the mean:
  double m = 0;
  double ma = input[0];
  for(double v : input) {
    if(ma < v) { ma = v; }
    m += v;
  }
  m /= input.size();

  double std = 0;
  for(double v : input) {
    std += (v - m) * (v - m) / input.size();
  }
  return (ma-m)/sqrt(std);
}



int main(int , char *[]) {
  std::cout << sigma_test(read_file("Arabic-Lipsum.utf8.txt"), 100, 300) << std::endl;
  return EXIT_SUCCESS;
}