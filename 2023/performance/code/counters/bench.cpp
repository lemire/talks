#include <iostream>
#include <memory>
#include <filesystem>
#include <fstream>

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
std::tuple<double,double,double> overhead(size_t iterations) {
  event_collector collector;
  if(! collector.has_events() ) {
    std::cerr << "# I lack access to performance counters.\n";
  }
  double elapsed_ns = 1e100;
  double cycles = 1e100;
  double instructions = 1e100;

  for(size_t i = 0; i < iterations; i++) {
    collector.start();
    event_count c = collector.end();
    if(c.elapsed_ns() < elapsed_ns) { elapsed_ns = c.elapsed_ns(); }
    if(c.cycles() < cycles) { cycles = c.cycles(); }
    if(c.instructions() < instructions) { instructions = c.instructions(); }
  }
  return {elapsed_ns, cycles, instructions};
}

void transcode(const std::string& source, size_t iterations) {
  event_collector collector;
  if(! collector.has_events() ) {
    std::cerr << "I lack access to performance counters.\n";
    return;
  }
  auto [elapsed_ns, cycles, instructions] = overhead(iterations);
  std::vector<event_count> events;
  events.reserve(iterations);
  size_t expected_utf16words = simdutf::utf16_length_from_utf8(source.data(), source.size());
  std::unique_ptr<char16_t[]> utf16_output{new char16_t[expected_utf16words]};
  for(size_t i = 0; i < iterations; i++) {
    collector.start();
    size_t utf16words = simdutf::convert_utf8_to_utf16le(source.data(), source.size(), utf16_output.get());
    if(utf16words != expected_utf16words) {
      return;
    }
    event_count c = collector.end();
    events.push_back(c);
  }
  for(event_count & e : events) {
    printf("%f %f %f\n", e.elapsed_ns()-elapsed_ns, e.cycles()-cycles, e.instructions()-instructions);
  }
}


int main(int , char *[]) {
  transcode(read_file("Arabic-Lipsum.utf8.txt"),200);
  return EXIT_SUCCESS;
}
