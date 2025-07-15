all: metric

metric: metric.cpp 3wise_xor_binary_fuse_filter_lowmem.h bloom.h hashutil.h
	c++ -std=c++17 -O3 -o metric metric.cpp -I. -I/opt/homebrew/include/ -L/opt/homebrew/lib/ -lzstd
clean:
	rm -f metric