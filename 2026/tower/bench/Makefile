CXX ?= g++
CXXFLAGS ?= -O2 -march=x86-64-v4 -Wall -Wextra
all: tolower_bench alignment_bench
tolower_bench: tolower_bench.cpp
	$(CXX) $(CXXFLAGS) -Icounters/include $< -o $@
alignment_bench: alignment_bench.cpp
	$(CXX) $(CXXFLAGS) -Icounters/include $< -o $@
run: tolower_bench alignment_bench
	./tolower_bench | tee results.csv
	./alignment_bench | tee results_alignment.csv
clean:
	rm -f tolower_bench alignment_bench
.PHONY: all run clean
