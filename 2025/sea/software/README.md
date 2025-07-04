# float_string_generation_benchmark

The goal of this project is to narrowly study the problem of generating
*shortest* number strings (e.g., `1.2122E4`) out of a decimal representation
(`significant * 10**power`). The implicit assumption is that you started
out from a binary floating point numbers (`float` or `double` in C/C++/Java/C#)
and you mapped it to a decimal form.

The project might have applications to more conventional problems such as converting
integer values to decimal representation.


In principle, converting `significant * 10**power` into a decimal string is not difficult.
You can compute `significant % 10` and get the last significant digits, and so forth.
This is the typically right-to-left approach: you write the least significant digit,
and the next least significant digit, and so forht.
You need to determine which way you go to the shortest string (do you write `0.1` or `1E-1`),
but that's not too difficult.

So why is this interesting? It is interesting because we noticed that a highly optimized
function in a Ryu float-to-string implementation was much slower then the implementation
in the  Dragonbox float-to-string implementation.

What is challenging? 

## Knowing where to write

One challenge is that you want to write the characters at the right place
from the start. This is not trivial because you don't known initially how many digits you 
need to write. If you consider the  right-to-left approach, it requires you to start 
writing *somewhere* implying that you know how many digits you have. Thankfully, there
are fast algorithms to count digits:

- Daniel Lemire, "Counting the digits of 64-bit integers," in Daniel Lemire's blog, January 7, 2025, https://lemire.me/blog/2025/01/07/counting-the-digits-of-64-bit-integers/.

Of course, you could write to a buffer and then copy over but that's likely more expensive than
counting the number of digits, at least in some cases.

The Dragonbox float-to-string implementation avoids this problem. The way it does it is that
it writes from left to right. So it writes the most significant digit first !!! It relies
on branching and assumes that the number of digits might be somewhat predictible, which could be true
in practice (or not).

## Storing the characters

Even if you have the digits (e.g., the integer 1) and you know where they should be written, you
still need to do something like:

```c++
buf[index] = '0' + value
```

And, once you figured out where the dot goes, you need to do

```c++
buf[index] = '.'
```

These things add up. So one trick is to compute hundreds instead of tens. And you use a lookup table.
So you have precompted strings from `00`, `01`, `02`, up `99`.
For the dot, you can also avoid having separate store by precomputing the strings
`0.`, `1.`, `2.`,... or something equivalent.

Similarly, for the exponent, you could precompute strings. E.g., you could certainly precompute `e+` and `e-` and
not have two stores.

Obviously, going from tens to hundreds to tens of housands could speed things further, although we might need
a slightly larger table (40kB?). We'd like to avoid massive tables if there are more clever approaches.

There might be room for fancier strategies. See

-  Daniel Lemire, "Converting integers to fix-digit representations quickly," in Daniel Lemire's blog, November 18, 2021, https://lemire.me/blog/2021/11/18/converting-integers-to-fix-digit-representations-quickly/.

It is a research question whether AVX-512 can solve this problem. It might. The reason
why AVX-512 might do it is that it supports *masked* stores. So you can safely store
a SIMD register to memory, writing only part of it.
It might also be possible to use SIMD in general if you allow writing beyond the expected
buffer. This might be acceptable in many settings where you can assume that the memory
is overallocated.


## Computing the digit values


This is where the fun mathematics comes in. I give you an integer, how do you compute
quickly the remainder and the quotient? See the following paper.

- Daniel Lemire, Colin Bartlett, Owen Kaser,  [Integer Division by Constants: Optimal Bounds](https://arxiv.org/abs/2012.12369),  Heliyon 7 (6), 2021
- Takahashi, D. (2023). Multiple Integer Divisions with an Invariant Dividend and Monotonically Increasing or Decreasing Divisors. In: Gervasi, O., et al. Computational Science and Its Applications – ICCSA 2023. ICCSA 2023. Lecture Notes in Computer Science, vol 13957. Springer, Cham. https://doi.org/10.1007/978-3-031-36808-0_26

Though the math is a bit tricky, we can often brute force a check for the solution.

Currently, we can *almost* bring it down to one multiplication per digit (where a digit could a value in [0,99] in this context).


## Open question

We also compute the value, e.g. the integer 43, and then we compute the string to write.

## Overall challenge

How low can you go? By a rough  estimation, the Ryu string generation algorithm might use 200 instructions
per float where as Dragonbox can go under 100 instructions per float. That's excellent, but still 
about 5 instructions per character produced.

## Usage

Currently, the benchmark is very approximative. The implementations are untested. This is at the demo stage.
We compare `champagne_lemire` which is something like the function from Ryu, `fast+champagne_lemire` which
is a slightly faster alternative and dragonbox (a very fast alternative). Some of the code is assuredly
or wrong makes assumptions not satisfied by the benchmark.

```
cmake -B build
./build/benchmark
```

To get performance counters, you might need to run the benchmark program in privileged mode (sudo).

Consider also testing with LLVM/clang.


```
CXX=clang++ cmake -B buildclang
./buildclang/benchmark
```

We definitively need more tests and better benchmarks including benchmarks on realistic data.

Further, the system archictecture is assuredly a factor.


## References

- Cassio Neri, Lorenz Schneider, Euclidean affine functions and their application to calendar algorithms, Software: Practice and Experience 53 (4), 2023.
- Daniel Lemire, Owen Kaser, Nathan Kurz, Faster remainder by direct computation: Applications to compilers and software libraries. Software: Practice and Experience, 49(6), 2019.