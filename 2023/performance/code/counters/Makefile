all: bench min_avg_distributions

bench: bench.cpp apple_arm_events.h  event_counter.h     linux-perf-events.h simdutf.h simdutf.cpp
	c++ -O3 -o bench bench.cpp -std=c++17 -Wall -Wno-unused-function

min_avg_distributions: min_avg_distributions.cpp apple_arm_events.h  event_counter.h     linux-perf-events.h simdutf.h simdutf.cpp
	c++ -O3 -o min_avg_distributions min_avg_distributions.cpp -std=c++17 -Wall -Wno-unused-function

clean:
	rm -r -f bench min_avg_distributions