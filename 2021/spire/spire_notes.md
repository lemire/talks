---

Hello. My name is Daniel Lemire. I am a professor at the University of Quebec
and I am going to tell you about our work on processing unicode strings at
gigabytes per second.

Our goal is to read, validate and convert unicode strings at record-breaking speeds
using practical software. Our work is supported by production-quality open-source software.
Our software works on mainstream processors such as Intel, AMD, ARM and so forth.
Our goal is to process billions of characters per second or conversely, to use
less than a nanosecond per character.

It is joint work with Muła, Keiser and many others.

---

Unicode is the de facto standard for representing strings in software. It is
interesting to reflect on how such a standard came to be.

We can trace back the need to represent character strings as sequences
of bits to at least the Morse code. Under the Morse code, we might represent
the letter A as a dot and a dash, the latter B as a dash, a dot, a dot and a dot,
and so forth.

---

The Morse code was convenient to send data over a wire, but it is less convenient
on computers. It is relatively difficult to decode because it has the granularity of
a single bit. Over time, we developed many different other data formats that use
less granularity. For example, we had Baudot code that used 5-bit words.
Hollerith code with 6-bit words and more recently 
the American Standard-Code for Information Interchange (ASCII) code that used
7-bit words. With 7 bits, ASCII can represent up to 128 characters.

---

ASCII is a widespread standard. We often write software code using ASCII.
Essentially, each character is mapped to a given integer value. These integer
values are sometimes called code points. What we call a character is not
necessarily visible character, in ASCII we include so called 'control characters'
such as tabulations, line returns and so forth.

---

Unfortunately, we cannot represent all possible characters using ASCII. And
different vendors have been tempted to produce their own standards. IBM
proposed its own character encodings. Windows and Apple did the same.
Various non-English language users also felt the need to introduce different
character encodings. ISO 8859 is a family of standards that cover many
European languages. The same happened with Thai, Indian, Chinese, Japanese
and Vietnamese users.

It made software more difficult to write, and it created difficulties for
users. Conversion between these different encodings was often lossy many that
information was lost during the conversion. Having a vast number of formats
tends to lead to bugs, security faults and so forth.

---

Thus people sought to create one interoperable standard that could be universal.
Unicode arose in the late 1980s. It extends ASCII in the sense that the ASCII table
is a subset of the Unicode table. Whereas standards like ASCII or ISO 8859 represent
characters without any attempt at sophisticated typography, Unicode provides an extensive
support for typography. Furthermore, whereas ASCII is finite, Unicode is meant to be
somewhat extensible. Every year, we had new characters. For example, we recently added
support for the pregnant person emoji. The intention behind unicode is make all other
character encodings obsolete. It practice, it is succeeding well. Every year, unicode becomes
more and more dominant.

---

Initially, the authors of Unicode thought that using 16 bits would be more than enough.
After all, most existing formats were at most 8-bit formats. However, if they wanted
to meet their goals of creating a universal character encoding standard, they would
need more room. So they planned for a bit over a million distinct characters. It implies
that they would need, if using a flat number of bits per character, 21 bits. Unfortunately,
processors do not operate using 21 bits.


---

So instead of a 21-bit format, we created a few distinct formats.
So there is a single Unicode table, a map from code point values and characters. However
there are many different ways to store the code point values in bytes. There is a 32-bit format
that is not used very much of data interchange because it is wasteful. It is mostly
used internally. In practice, rather, we find UTF-16 which works with 16-bit words,
and UTF-8 which works at a granularity of a byte. The UTF-16 format is widely used 
under Windows and it is a common default in the programming languages Java and C#.
The UTF-8 dominates on the web. It is the default for XML. It is required for JSON when
doing data interchange between systems.  It is a common default for HTML. It is also
the default in many recent programming languages like Go, Rust, Swift.


---


Thus while Unicode did become universal and did replace many different standards, we 
are still left today with two popular binary Unicode formats: UTF-8 and UTF-16.
They are both concise ways to represent the characters, but their strike a different
balance. For ASCII inputs, the UTF-8 format uses a single byte per character, 
compared to two bytes per character for UTF-16. This often helps UTF-8 be more concise
for content that is mostly ASCII such as many HTML, XML or JSON documents.
For what I call 'latin' characters, they both use two bytes. For what I call the 'asiatic'
range, UTF-16 has a slight edge using 2 bytes against the 3 bytes of the UTF-8. Thus for
documents containing, for example, Japense of Chinese text, UTF-16 might be slightly
more concise. Both formats use at must 4 bytes per character.

Because the UTF-8 format is byte-oriented, it can be used for null terminated C strings,
since those are normally byte oriented. And, of course, UTF-8 is binary-wise backward 
compatible with ASCII.

Most strings with UTF-16 can be assumed to use a flat 16-bits per characters, unless
you have some special characters like emojis, in which case some of your characters
may require 4 bytes. However, though it seems like a feature, it has proven to be error-prone.
Many software applications are unfortunately written as if characters were all 2-byte long.
When programmers make this assumption, they open themselves to security bugs.

---

Before we discuss how we can manipulate Unicode data, it is important
to review the formats.

UTF-16 as the name implies is organised as a sequence of 16-bit words.
For code-point values that fit within 2 bytes, we use precisely two bytes.
We simply store the code-point value, that is, the integer value, as a
two-byte integer.
For larger code point values, we use 4 bytes. The 16-bit words can be 
written in two orders (big endian or little endian) depending on whether
the first byte in a two byte sequence contain the most significant or less
significant bits. A common default is little endian, which means that the
less significant bits come first.


---

To store large code-point values, we need two 16-bit words. 
There is a range of code-point values that are excluded in the unicode
format. When a value from the first half of this excluded range
is followed by a value from the second range, we have a valid surrogate pair.
We then use the 10 least significant bits of each 16-bit word to make up 
20 bits of the result.

---

The UTF-8 format is made of a sequence of bytes. Each character begins
with a 'leading byte' followed by 0 to 3 'continuation' bytes.

---

A special 'leading byte' is just an ASCII byte, that is a byte value with 
the most significant bit set to zero.
All non-leading bytes have their most significant bit set to 1 and their
second most significant bit set to 0.

When we have exactly two most significant bit set, then we have a two-byte sequence.
When we have exactly three most significant bit set, then we have a three-byte sequence.
When we have exactly four most significant bit set, then we have a four-byte sequence.


---

Validating UTF-8 is requires checking many conditions. Firstly, because
characters can use no more than 4 bytes, it is not possible for the five
most significant bits to be set on any byte. We must have that the number
of continuation bytes match the leading byte. And then we have a few additional
constraints. On the one hand, we have the fact that we cannot store a code
point value in the range of values reserved for surrogate pairs. Though
UTF-8 does not have surrogate pairs, the UTF-16 format only works if these
values are omitted, so UTF-8 must also omit them.
Then we have to make sure that we always store a give code point value using
as few bytes as possible. This ensures that a given character matches a unique
byte sequence. Doing otherwise would be a security risk.


---

Let us review the two formats side by side.

First let us compare how they represent ASCII. As you can see, it is
rather easy to convert back and forth. It implies that you have to either insert
a zero byte, or remove a zero byte. Thus you should expect that converting
ASCII between UTF-8 and UTF-16 should be very fast.


---

Converting two-byte sequences between UTF-8 and UTF-16 is a bit trickier. When
going from UTF-16 to UTF-8, we have to move the data bits, and insert some 
UTF-8 coding bits. When going from UTF-8 to UTF-16, we need to pack the data bits.

---

Going from three UTF-8 bytes to one UTF-16 word is similar to the previous scenario.
In one direction, we need to pack the data bits and in the other we need insert
UTF-8 coding bits.

---

Converting 4-byte sequences is much more complicated. Thus we should expect significantly
slower speeds. Fortunately, in most documents 4-byte characters are uncommon.

---

There are many important operations we might want to do with UTF-8 and UTF-16 strings.
You may want to convert them to UTF-32, that is, to 32-bit words, for internal use.
You may want to count the number of characters. You may want to merely validate the 
input. And so forth. An important operation is to convert strings from one format
to the other.

For example, if your database contains UTF-16 strings and you want to post the
data on the web, then you need to constently convert back and forth. You cannot
assume that the input is valid: it could come from an adversary with malicious
intentions, or it could be buggy. Thus you must validate as you transcode.

Of course, you can often avoid having to transcode entirely. But in practice it is
often difficult to do so because different software components require one encoding
or the other. Furthermore, even if you never need to decode, you will still
need to validate, which is a subset of the transcoding operation. And even if
you do not need to do any of these things, you still should know how quickly and
efficiently they can be executed.

---

So how quickly can you transcode strings currently. On a good server, with some common
data inputs, you might reach about a gigabyte per second. That is good, but transcoding
is likely to be just one step in a series of operations. And it is several times slower
than the speed of recent disks or the bandwidth between large instances in cloud infrastructures.

We are not solely interested in the speed issue. Our experience has been that drastic
reductions in the number of instructions translate into drastic reduction in energey usage.
Thus by making your software faster, you also make it greener.

---

So how can we go faster? Existing software libraries are mature and highly optimized.

We first observe that most mainstream processors, whether in your PC or in your mobile
phone have advanced instructions called SIMD which stands for Single instruction, multiple data.
Unlike regular instructions which operate over regular registers, these instructions
work over wide registers and are designed to process multiple words at once.
They seem to be ideally suited for processing unicode strings.

SIMD instruction sets rely on registers that often span 16 bytes. These 16 bytes
can also be viewed as 8 2-byte values, or 4 4-byte values. On x64 systems, you
also have larger registers, going as wide as 64 bytes on recent Intel systems.
In our implementations, we either use 16-byte or 32-byte registers. We also avoid
'expensive' instructions such as multiplications or instructions that require
floating-point numbers. 

Most of your software already use these SIMD instructions. For example, when you copy
data, it is common for these instructions to be put to good use, since it much faster
to copy data in large blocks. Similarly, many compilers will automatically 'vectorize'
your code. That is, they will compile it to code that uses SIMD instructions. Autovectorization
happens in C, C++, Java as well as many other languages.

In our work, we make deliberate use of these SIMD instructions. Indeed, it is our
experience that compilers can only go so far and that expert engineering can do 
much more on specific problems.


---


In 2008, a Canadian researcher named Cameron and, independently, an 
IBM team in Japan, proposed Unicode processing using SIMD instructions. 
The Japanese team only published their work in Japanese and their approach
does not cover the full Unicode specification. They also did not, to my knowledge,
publish their software. Cameron did publish it as an open source library called u8u16.
It seems to be no longer supported, but it can be found online.


Engineers are routinely using SIMD instructions to speed up the ASCII special case.
However, there has been few attemps at doing much more since 2008. I tracked down
an interesting effort by Goffart in 2012, and there is a more recent library
by Gatilov in 2019. I am not going to discuss further these two cases, but we
review them in our full paper to appear in the Software: Practice and Experience
journal.

In any case, there has been little academic work on the topic. We were motivated
by this gap in the research.

---


A key operation that SIMD instruction sets support is the ability to permute
bytes or wider words using  single inexpensive instruction. It was present in the
IBM POWER processors, it is available on Intel and AMD x64 processors, and it
is in the ARM processor present in your mobile phone.

Though the details vary by processor type, the general idea is the same. Given
two input sources, you can use one of the two inputs as a set of indexes pointing
at the values in the other source. Thus you can reorder or shuffle the values
of an array. Another way to think of the same operation is as a vectorized table 
lookup.

Of course, if you need to move words quickly, you should either have a precomputed
set of indexes or a convenient way to compute them quickly. I call this set of indexes
a 'shuffle mask'.

If you use these instructions for vectorized lookup tables, you must similarly 
precompute a 'table', that is a register containing values you want to access.

---

Our core UTF-8 to UTF-16 transcoding algorithm works with vectorized permutation.
We are going to assume that the input is valid UTF-8. We are going to discuss 
validation separately.

We take a block of bytes, we find the end of each character. The end of characters
can be defined as the byte preceding a leading byte. Leading bytes come in many forms,
but we can detect them by first finding out where the continuation bytes are,
and then inverting this selection. The contibuation bytes have their two most significant
bits as 1 and 0. If you view a byte value as signed value from -128 to 127, then the
continuation bytes are the values than are less than -64.

One we have identified the end of each character, then we can construct a corresponding
bitset. For each byte of input, we have a corresponding bit. We set the corresponding bit
to 1 if and if the corresponding byte is the end of a character.

You may wonder why we identify the end of a character rather than its beginning. The
problem with identify the beginning is that for the last character in a sequence, if you 
only know where it starts and not where it ends, you cannot decode it. If you are given the
end of all characters, you know how long they are, assuming that your first byte marks
the beginning of a character.

 
---

To illustrate the construction of such a bitset, let us look at a concrete example.
In my example, I have an ASCII character, followed by a two-byte character, followed
by another ASCII character, followed by a two byte character, followed by an ASCII
character, followed by a two byte character.

The corresponding bitset is 101101101. Treating this bitset and an integer value, 
I can use it as a key in a table.

---

So far, I did not specify how many bits I am using. In our implementation, we used
12-byte blocks and so we need a table with 4096 entries in it. In the table,
we store the number of consumed bytes. Ideally, we would consume 12 bytes each
time, but that's only possible if the last bit is set, that is, it is only possible
if we don't have part of a character at the end. We also have another index that points
inside a table where we find a shuffle mask.



---


This index to a table of shuffle masks carries information of its own.
We have three different code paths, depending on whether we have only 
encountered 1-byte and 2-byte characters, or whether we have found some
3-byte characters, or whether in are in the general case.

Another nice side-effect of this secondary table is that we only need to
store about 200 shuffle masks, so we get the benefit of some compression.
However, our tables use in total about only 11 kB.

---

We can go back to our example with the computed bitset.
We are in a scenario where we only have 1-byte and 2-byte characters.
In the first step, we use a vectorized permutation. Then we apply 
a series of inexpensive arithmetic transformations.

---

Though what we described in efficient, there are few more 
optimizations that we use. For one thing, instead of loading the data
in small blocks of 12 bytes, we load 64 bytes and create a single
bitset over which we iterate in small chunks of 12 bytes.

Doing so allow us to check for some easy cases. For example,
we can check whether we have 64 ASCII bytes. We can also
use other fast paths for the cases where all 12 bytes
are ASCII, or only 2 bytes, or only 3 bytes.

---

So far we have assumed that the input was valid. We need the validity.
We check whether the 64 bytes are correct using a fast technique
we introduced in an earlier manuscript.

---

We sketch our UTF-8 validation algorithm. We can recognize most errors
by looking at only successive bytes. For example, if you have an ASCII 
value, you know that the next byte should be a leading byte.
In fact, it is enough to look at sequences of three 4-bit or nibble values.

What we do is three vectorized lookups on nibbles, followed by bitwise AND
operations. I call the general idea a vectorized classification.

----

To understand how vectorized classification works, let us consider an example.
Suppose that I want to find all instances where the value 3 is followed by
values 1 or 2.
I build two lookup tables, one where I set the bit corresponding to value 3 to 1,
and one where I set the bits corresponding to indexes 1 and 2 to 1.
If I am given two successive values, I use the first value as an index in the first table,
and I use the second value as an index in the second table. I tend
compute the bitwise AND of the two looked up result. If I get 1, then I have
a match, otherwise I do not. The value 1 in this instance is arbitrary, any
non-zero value would match.

Over course, this can be vectorized.

----

Let us look at another example. This time, I will have several cases.
So I have, again, the value 3 followed by value 1 or 2, but then I also
add other cases, such as the value 5 followed by the value 0, and
the value 6 followed by the the value 10.

Instead of using the value 1 solely, I use the values 1, 2 and 4 as markers.
I use 1, 2 and 4 because the correspond to setting the first, second and third
bit to 1 in the result. 
As before I construct two tables.
Then I repeat again, I do the lookups, and the bitwise AND.
From the result, I can distinguish the three cases depending
on the result. That is, if the result is 1, then the first
case is a match. If the result is 2, then the second case is a match.
If the result is 4, then the third case is a match. It is not
needed that the three cases be mutually exclusive. If it were possible
for the first and second case to occur, then I might have the bitwise OR
of 1 and 2, that is, the value 3, as a result.

In practice, because we use a byte-oriented model, I can recognize up to
8 different cases. Our validation routine is based on this observation.
We can do almost the entire validation solely with vectorized classification.
We just need to check that no bit is set that would correspond to an error,
but that is quite fast. Constructing the correct three lookup table is a bit
difficult, but it only needs to be done once, during the design of the algorithm.
I refer you to our paper for details.


----


So the implementation is not too difficult. We take the input buffer, we shift
it once, shift it again, do three lookups and then compute the bitwise AND.
It compiles to few instructions.

Of course, in practice, we need to do a bit more work during the validation
because we must also check that we have the right number of continuations in
the case of two-byte and three-byte caracters.


---

Of course, we need to also go in the opposite direction and to convert
UTF-16 strings into UTF-8 strings. It is a somewhat easier problem in 
some respect, but to our knowledge, it was never addressed in the academic
literature and there are few attempts at using SIMD instructions to 
speed it up.


---
We load a full register. It may span 16 bytes or, for recent Intel and AMD
processors, 32 bytes.

In the case where we have ASCII bytes, we use a fast routine, the
the two-byte words are packed into bytes. We can check for this case
with a few simple operations and the transformation is efficient.

---

When the words need to be mapped to either 1-byte UTF-8 characters
or two-byte UTF-8 characters, we first build a bitmap which indicates
where the ASCII characters are. The bitmap allows us to lookup 
in a table a shuffle mask and then we do a vectorized permutation
followed by some arithmetic. The permutation maps the data from
16-bit words to 32-bit words.

The bitmap also gives us the number of
bytes we can consume. Indeed, we also write an fixed number of
bytes, but the number of consumed bytes depends on the data.


---

When the words need to be mapped to either 1-byte UTF-8 characters
or two-byte UTF-8 characters or three-byte characters, we use a similar approach.
It is slightly more complicated and we need a new to build an index
based on where the ASCII and two-byte characters are. We need two lookup
and two vectorized permutation. As before, the permutations map the data from
16-bit words to 32-bit words.

Overall, we use rather small lookup tables, for a total of a bit more than 8 kB.

When we detect surrogate pairs, we fallback on a scalar routine. We used to have
a complicated vectorized routine, but it involved a lot of engineering and required
rather large tables. In practice, we find that there are often few surrogate pairs so
it is not worth optimizing this case so much.

---

Our full paper has detailed experiments, but for this presentation, I will
focus on sample results using an AMD server. Note that our full paper has results
on ARM-based systems as well. We compare against the u8u16 library. As stated
previous, there are other alternatives, but the u8u16 library is part of the academic
litterature. We also compare with UCI. It is the industry standard.
For our tests, we use lipsum, so random-looking text in various languages.
---

For ASCII, we find that we are sometimes 20 times faster than UCI. Effectively,
we are nearly limited by memory bandwidth. We use the input size to determine
the volume when transcoding, so you should expect UTF-16 to UTF-8 to be faster
because it uses more bytes for storage.

---

For non-trivial languages, as you can see, we can be 4 times faster 
than UCI at UTF-8 to UTF-16 transcoding. For UTF-16 to UTF-8 transcoding,
the benefits of our approach are greater. In this particular tests, 
the u8u16 library is competitive but it does not particularly shine.

---

Our software is available online and we encourage you to take it out for a spin.
It is open source. We welcome contributions. We make it easy to use. It is
thoroughly tested. 

Though I did not cover it during this presentation, it supports runtime dispatching.
So while we have a single code base, at runtime it will check your CPU type and 
chose the best compiled routines. We support various processors.

---

If you'd like more details, our full paper is available online.

If you'd like to stay in touch with me, I have a blog where I regularly write about
software performance.