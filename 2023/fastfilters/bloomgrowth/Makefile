all: metric

metric: metric.cpp 3wise_xor_binary_fuse_filter_lowmem.h bloom.h hashutil.h
	c++ -std=c++17 -O3 -o metric metric.cpp
clean:
	rm -f metric