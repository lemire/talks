

probability of sigma events:

1-sigma is 32%
2-sigma is 5%
3-sigma is 0.3% (once ever 300 trials)

4-sigma is 0.00669% (once every 15000 trials)
5-sigma is 5.9e-05% (once every 1,700,000 trials)
6-sigma is 2e-07% (once every 500,000,000)
exp(-n * n / 2) /(n * sqrt(pi /2)) *100 (for n> 3)

probability of 5 values exceeding 5 other values, same binary.

average, minimum, maximum, hwo they are distributed per instance size.

software systems are complex systems: changes can have unexpected consequences.

Incremental optimization, how do you know that you are on the right track?


system calls may dominate, assume that they remain constant.

data structure layout changes can trigger expensive loads, assume that we keep that constant.


Branching can artificially lower ins count

some instructions are more expensive than others, 



Java instruction counters

C/C++ instruction counters

https://github.com/jvm-profiling-tools/async-profiler

has performance counters

Go instruction counters.
https://go.googlesource.com/proposal/+/refs/changes/08/219508/2/design/36821-perf-counter-pprof.md