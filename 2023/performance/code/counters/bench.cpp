#include <iostream>
#include <memory>
#include "simdutf.h"
#include "simdutf.cpp"

#include "event_counter.h"

void transcode(std::string source, size_t iterations) {
  event_collector collector;
  if(! collector.has_events() ) {
    std::cerr << "I lack access to performance counters.\n";
    return;
  }
  std::vector<event_count> events;
  events.reserve(iterations);
  size_t expected_utf16words = simdutf::utf16_length_from_utf8(source.data(), source.size());
  std::unique_ptr<char16_t[]> utf16_output{new char16_t[expected_utf16words]};
  for(size_t i = 0; i < iterations; i++) {
    collector.start();
    //size_t utf16words = simdutf::convert_utf8_to_utf16le(source.data(), source.size(), utf16_output.get());
   // if(utf16words != expected_utf16words) {
   //   return;
   // }
event_count c = collector.end();
    events.push_back(c);
  }
  for(event_count & e : events) {
    printf("%f %f %f\n", e.elapsed_ns(), e.cycles(), e.instructions());
  }


}


int main(int , char *[]) {
  transcode("fdfdsééééééfdsfdsfdsfsdfwee",1000);
  return EXIT_SUCCESS;
}
