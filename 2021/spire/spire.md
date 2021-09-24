---
marp: true
theme: base
title: Unicode at gigabytes per second
description: We often represent text using Unicode formats (UTF-8 and UTF-16).  UTF-8 is increasingly popular (XML, HTML, JSON, Rust, Go, Swift, Ruby). UTF-16 is most common in Java, .NET, and inside operating systems such as Windows.
paginate: true
_paginate: false
---

<!--  --- -->

## <!--fit--> Unicode at gigabytes per second


Daniel Lemire 
professor, Université du Québec (TÉLUQ)
Montreal :canada: 

blog: https://lemire.me 
twitter: [@lemire](https://twitter.com/lemire)
GitHub: [https://github.com/lemire/](https://github.com/lemire/)

:exclamation:  work with Wojciech Muła, John Keiser and others!


---

# From characters to bits

Morse code

- A : 0 1
- B : 1 0 0 0
- C : 1 0 1 0

26 letters.


---

# From characters to bits

Morse code

- A : 0 1
- B : 1 0 0 0
- C : 1 0 1 0

26 letters.


---

# Fixed-length codes

- Baudot code (~1860). 5 bits.
- Hollerith code (~1896). 6 bits.
- American Standard-Code for Information Interchange or ASCII (~1961). 7 bits. 128 characters.

![width:600px](ascii.png)


# Too many fixed-length codes!


- IBM: Binary Coded Decimal Interchange Code.  6 bits.
- IBM: Extended Binary Coded Decimal Interchange Code or EBCDIC. 8 bits. 
- ISO 8859 (~1987). 8 bits. European.
- Thai (TIS 620), Indian languages (ISCII), Vietnamese (VISCII) and Japanese (JIS X 0201).
- Windows character sets, Mac character sets.

---

# Unicode (late 1980s)

- Extends ASCII.
- Universal.
- Replaces all other standards.
- Typography, full localisation, extensible.

---

# Unicode: how many bits?

- 16 bits ought to be enough?
- Numerical range from 0x000000 to 0x10FFFF.
- Would need 20 to 21 bits.


---

# UTF-16 and UTF-8

Two main formats.

UTF-16: Java, C#, Windows

UTF-8: XML, JSON, HTML, Go, Rust, Swift


---

# UTF-16 and UTF-8

| character range | UTF-8 bytes | UTF-16 bytes |
|:----------------|:------------|:-------------|
| ASCII (0000-007F) |  1  |   2 |
| latin (0080-07FF) |  2  |   2 |
| asiatic (0800-D7FF, E000-FFFF) |  3  |   2 |
| supplemental (010000-10FFFF) |  4  |   4 |

---

# UTF-16

- 16-bit words. 
- characters in 0000-D7FF and E000-FFFF, stored as 16-bit values---using two bytes.
- characters in 010000-10FFFF are stored using a 'surrogate pair'.
- Comes in two flavours (little and big endian at the 16-bit level).

---

# UTF-16 (surrogate pair)

- first word in d800-dbff.
- second word in dc00-dfff.
- character value is 10 least significant bits of each---second element is least significant.
- add 0x10000 to the result.

---

# UTF-16 (pros/cons)

- pro: often just 16-bit characters (no surrogate pair).
- pro: easy validation (just check for values in range d800-dfff).

- con: not binary compatible with ASCII.
- con: less concise when content is mostly just ASCII.
- con: emoji usage makes surrogate pairs more common.

---

# UTF-8

- 8-bit words (no endianess)
- One 'leading' byte followed by 0 to 3 bytes.

---

# UTF-8 format

- Most significant bit of leading is zero, ASCII.
- 3 most significant bits 110, two-byte sequence.
- 4 most significant bits 1100, three-byte sequence.
- 5 most significant bits 11000, four-byte sequence.
- Non-leading bytes have 10 as the two most significant bits.

---

# UTF-8 validation rules

- The five most significant bits of any byte cannot be all ones.
- The leading byte must be followed by the right number of continuation bytes. 
- A continuation byte must be preceded by a leading byte.
- The decoded character must be larger than 7F for two-byte sequences, larger than 7FF for three-byte sequences, and larger than FFFF for four-byte sequences. 
- The decoded code-point value  must be less  than 110000 
- The code-point value must not be in the range D800-DFFF.

---

# UTF-8 to UTF-16 transcoding

- Need both UTF-8 and UTF-16.
- Most validate both formats.
- Must convert (transcode) from one format to the other format, while validating the input.

---

# Some numbers

- bandwidth between node instances: over 3 GB/s
- PCIe 4.0 disks (and PlayStation 5): over 5 GB/s
- Popular C++ trancoding library (ICU): ~1 GB/s

---

# Can we go to gigabytes per second?

- x64, ARM, POWER: have SIMD instructions.
- Can permute blocks of 16 bytes (or 32 bytes) using a single cheap instruction.
 
---

# UTF-8 to UTF-16 transcoding



All commodity software with SIMD instructions (e.g., x64, ARM, POWER) have fast instructions to  permute bytes within a SIMD register  according to a sequence of indexes. Our transcoding techniques depend critically on this feature: we code in a table the necessary parameters---including the indexes (sometimes called shuffle masks)---necessary to process a variety of incoming characters.

Our  accelerated  UTF-8 to UTF-16 transcoding algorithm  processes  up to 12~input UTF-8 bytes at a time. From the input bytes, we can quickly determine the leading bytes and thus the end beginning of each character. We use a 12-bit word as a key in a 1024-entry table. Each entry in the table contains the number of UTF-8 bytes that will be consumed and an index into another table where we find shuffle masks. The value of the index into the other table also determines one of three possible code paths. The first 64~index values  indicate  that we have 6~characters spanning between one and two bytes.  Index values in $[64,145)$ indicate that we have 4~characters spanning between one and three bytes. The remaining indexes represent the general case: 3~characters spanning between one and four bytes.
The shuffle mask can then be applied to the 12~input bytes to form a vector register that can be transformed efficiently.
We use this 12-byte routine inside  64-byte blocks. After loading a 64-byte block,  
we apply the Keiser-Lemire validation routine~\cite{keiser2020validating}. Afterward,
we identify the leading bytes, and then process the block in multiple iterations, using up to 12~bytes each time. In the special case where all 64~bytes are ASCII, we use a fast path.
For even greater efficiency, we have three other fast paths within the 12-byte routine: we check whether the next 16~bytes are ASCII bytes,  whether they are all two-byte characters, or all  three-byte characters. 



Our UTF-16 to UTF-8 algorithm iteratively reads a block of input bytes in a SIMD register.  If all 16-bit words in the loaded SIMD register are in the range \codepointrange{0000}{007f}, we use a fast routine to convert the 16~input bytes into eight equivalent ASCII bytes.
 If all 16-bit words are in the range \codepointrange{0000}{07ff}, then we use a fast routine to produce sequences of one-byte or two-byte UTF-8 characters. Given an 8-bit bitset which indicates which 16-bit words are ASCII, we load a byte value from a table indicating how many bytes will be written, and a 16-byte shuffle mask. 
If all 16-bit words are in the ranges \codepointrange{0000}{d777}, \codepointrange{e000}{ffff}, we use another similar specialized  routine to produce sequences of one-byte, two-byte and three-byte UTF-8 characters.
Otherwise, when we detect that the input register contains at least one part of a surrogate pair, we fall back to a conventional code path.




\section{Experiments}
\label{sec:experiments}

We make available our software as a portable open-source  C++ library.\footnote{\url{https://github.com/simdutf/simdutf}}
As a benchmarking system, we use a recent AMD processor (AMD EPYC 7262,  Zen~2 microarchitecture, \SI{3.39}{\GHz}) and GCC~10.
We compare against a popular library: International Components for Unicode (UCI)~\cite{uci} (version~67.1).
We also use the \texttt{u8u16} library~\cite{cameron2008case}. Unlike UCI and our own work, the  \texttt{u8u16} library only provides UTF-8 to UTF-16 transcoding.
For our experiments, we use lipsum text in various languages.\footnote{\url{https://github.com/rusticstuff/simdutf8}} 
All of our transcoding tests include validation.
To measure the speed, we record the time by repeating the task \num{2000}~times. We compare the average time with the minimal time and find that we have an accuracy of at least 1\%. We divide the input volume by the time required for the transcoding. Fig.~\ref{fig:transcoding} shows our results. 
Our UTF-8 to UTF-16 transcoding speed exceeds  \SI{4}{\gibi\byte\per\second} for Chinese and Japanese texts, which is about four times faster than UCI. In our tests, the \texttt{u8u16} library only surpasses ICU significantly for Arabic.
Our UTF-16 to UTF-8 transcoding speed is nearly \SI{6}{\gibi\byte\per\second} in all tests which is nearly ten~times faster than UCI.

For ASCII transcoding (not shown in the figures), we achieve  \SI{36}{\gibi\byte\per\second} for UTF-16 to UTF-8 transcoding, and  \SI{20}{\gibi\byte\per\second} for UTF-8 to UTF-16 transcoding. Effectively, we are so fast that we are nearly limited by memory bandwidth. Comparatively, UCI delivers \SI{2}{\gibi\byte\per\second} and \SI{1}{\gibi\byte\per\second} in our tests.

\begin{figure}\centering
\subfloat[UTF-8 to UTF-16 transcoding]{
\includegraphics[width=0.49\textwidth]{lipsumspeedutf8utf16.tikz}
}
\subfloat[UTF-16 to UTF-8 transcoding]{
\includegraphics[width=0.49\textwidth]{lipsumspeedutf16utf8.tikz}
}

\caption{\label{fig:transcoding} Transcoding speeds for various test files. }
\end{figure}

\section{Conclusion}



Our SIMD-based transcoders can surpass popular transcoders (e.g., UCI) by a wide margin (e.g., $4\times$). Our UTF-16 to UTF-8 transcoder achieves speed of about \SI{6}{\gibi\byte\per\second} for many Asiatic languages using a recent x64 processor. In some cases, we achieve  \SI{4}{\gibi\byte\per\second}  for UTF-8 to UTF-16 transcoding with full validation. For ASCII inputs, we achieve tens of gigabytes per second.


---

## Software

<!-- This is a presenter note for this page. -->

https://github.com/simdutf/simdutf

- ARM NEON, SSE, AVX...


---

## Further reading

- Lemire, Daniel and Wojciech Muła , Transcoding Billions of Unicode Characters per Second with SIMD Instructions, Software: Practice and Experience (to appear) https://r-libre.teluq.ca/2400/
- Blog: https://lemire.me/blog/
