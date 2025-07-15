all: bench min_avg_distributions sigma_test std_scale

bench: bench.cpp apple_arm_events.h  event_counter.h     linux-perf-events.h simdutf.h simdutf.cpp
	c++ -O3 -o bench bench.cpp -std=c++17 -Wall -Wno-unused-function

min_avg_distributions: min_avg_distributions.cpp apple_arm_events.h  event_counter.h     linux-perf-events.h simdutf.h simdutf.cpp
	c++ -O3 -o min_avg_distributions min_avg_distributions.cpp -std=c++17 -Wall -Wno-unused-function

std_scale: std_scale.cpp apple_arm_events.h  event_counter.h     linux-perf-events.h simdutf.h simdutf.cpp
	c++ -O3 -o std_scale std_scale.cpp -std=c++17 -Wall -Wno-unused-function

sigma_test: sigma_test.cpp apple_arm_events.h  event_counter.h     linux-perf-events.h simdutf.h simdutf.cpp
	c++ -O3 -o sigma_test sigma_test.cpp -std=c++17 -Wall -Wno-unused-function

clean:
	rm -r -f bench min_avg_distributions sigma_test std_scale