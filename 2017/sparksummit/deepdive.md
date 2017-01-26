<!--open with Marp-->

<style>
.slide h2 {
color:#008dc8;
}
.slide   {
border-bottom-color:#008dc8;
border-bottom-style:solid;
border-bottom-width:10px;
}
.slide {
    background-repeat: no-repeat;
    background-position:  1% 99%;
background-image: url("sparksummit2017small.png");
}

</style>

<!-- *template: invert -->
<style>
 *[data-template~="invert"] {
color:white !important;
background-color:#008dc8 !important;
}
 *[data-template~="invert"] * {
color:white !important;
background-color:#008dc8 !important;
}
</style>

## ENGINEERING FAST INDEXES (DEEP DIVE)

<img src="sparksummit2017large.png" style="float:right; width:10%"/>

Daniel Lemire :maple_leaf:
https://lemire.me 

Joint work with lots of super smart people

---

Parallelism is not just multicore.

Does vectorization matters?

AVX2 is 256 bits (4x 64 bits)

  for(size_t i = 0; i < len; i++) {
    a[i] |= b[i];
  }
  
  using scalar : 1.5 cycles per byte 
  with AVX2 : 0.43 cycles per byte (3.5 x better)
  
  
  With AVX-512 (knights landing), the performance gap exceeds 5 x


Amdahl's law 

short values (16-bit, 32-bit) are better than wider ones (64-bit) once you vectorize


power of simd  http://lemire.me/blog/2016/12/30/can-your-c-compiï¿½ï¿½åœ°-scalar-product/ 

reason in cpu cycles (popcnt)

fast hashing (zobrist, etc.)

RLE gone bad (need to scan from the beginning)

Indeed story

Maintaining cardinality is cheap

data parallelism

can't easily guess generated output from compiler

can do more than just unions and intersections

state of the art SIMD in java (java 9)

performance of binary search


constant matter : union of hash sets


throughput trumps latency if you can avoid data dependencies

accelerate hash tables with two-step

https://github.com/lemire/dictionary



constant factors matter, merge two hash sets vs two arrays

dict coding

simd algos

your processor is superscalar

hard to reason about performance from code
There are no comments on this page.


---

## What helps us...

- All modern processors have fast population-count functions (``popcnt``) to count the number of 1s in a word. 
- Cheap to keep track of the number of values stored in a bitset!
- Available from Java as an intrinsic!
