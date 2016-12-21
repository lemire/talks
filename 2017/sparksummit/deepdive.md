## ENGINEERING FAST INDEXES (DEEP DIVE)

Presenter: Daniel Lemire https://lemire.me 

Joint work with lots of super smart people

---


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