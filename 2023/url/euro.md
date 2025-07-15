---
marp: true
theme: base
enableHtml: true
title: Parsing Millions of URLs per Second
description: With the end of Dennard scaling, the cost of computing is no longer falling at the hardware level: to improve efficiency, we need better software. Competing JavaScript runtimes are sometimes faster than Node.js: can we bridge the gap? We show that Node.js can not only match faster competitors but even surpass them given enough effort. URLs are the most fundamental element in web applications. Node.js 16 was significantly slower than competing engines (Bun and Deno) at URL parsing. By reducing the number of instructions and vectorizing sub-algorithms, we multiplied by three the speed of URL parsing in Node.js (as of Node.js 20). If you have upgraded Node.js, you have the JavaScript engine with the fastest URL parsing in the industry with uncompromising support for the latest WHATGL URL standard. We share our strategies for accelerating both C++ and JavaScript processing in practice.
paginate: true
_paginate: false
---
<style>
img[alt~="top-right"] {
  position: absolute;
  top: 30px;
  right: 30px;
}
</style>
<style>
img[alt~="bottom-right"] {
  position: absolute;
  top: 240px;
  right: 0px;
  width: 50%;
}
</style>
<style>
img[alt~="bottom-right-graph"] {
  position: absolute;
  top: 100px;
  right: 0px;
  width: 50%;
}
</style>
<style>
img[alt~="graph"] {
  left: auto;
  right:auto;
  width: 70%;
}
</style>
<style>
img[alt~="bottom"] {
  position: absolute;
  top: 400px;
  right: 0px;
  width: 55%;
}
</style>


<!-- ![center](simdjsonlogo.png)-->

<!--  --- -->

## <!--fit--> Parsing Millions of URLs per Second


Yagiz Nizipli :us:
GitHub: [https://github.com/anonrig](https://github.com/anonrig)



Daniel Lemire :canada:
GitHub: [https://github.com/lemire](https://github.com/lemire)


---

# Software performance

- Reduces cost (AWS, Azure)
- Improves latency
- Reduce complexity (parallelism, caching)
- Don't cause climate change

<!--
footer: D
-->

---

# State of Node.js Performance 2023

> Since Node.js 18, a new URL parser dependency was added to Node.js — Ada. This addition bumped the Node.js performance when parsing URLs to a new level. Some results could reach up to an improvement of 400%. (State of Node.js Performance 2023)

<!--
footer: D
-->

---

> Just had a benchmark for a code change go from 11 seconds to complete down to about half a second to complete. This makes me very happy.

James Snell, Cloudflare
*Referencing adding Ada URL to Cloudflare Workers*

<!--
footer: Y
-->

---

# Structure of an URL

Example: https://user:pass@example.com:1234/foo/bar?baz#quu

- protocol
- user name, password
- hostname
- port
- pathname
- search
- hash

<!--
footer: Y
-->

---

# Examples

<!-- - Long URLs: `http://nodejs.org:89/docs/latest/api/foo/bar/qua/13949281/0f28b//5d49/b3020/url.html#test?payload1=true&payload2=false&test=1&benchmark=3&foo=38.38.011.293&bar=1234834910480&test=19299&3992&key=f5c65e1e98fe07e648249ad41e1cfdb0`-->
- non-ASCII: `http://你好你好.在线`
- File: `file:///foo/bar/test/node.js`
- JavaScript: `javascript:alert("node is awesome");`
- Percent Encoding: `https://\%E4\%BD\%A0/foo`
- Pathname with dots: `https://example.org/./a/../b/./c`
- Ipv4 address with hex/octal digits: `https://127.0.0x0.1`

<!--
footer: D
-->
---

# WHATWG URL

<!--most browsers, JavaScript runtimes ; curl, runtime libraries $\to$ RFC 3986-->
<!--PHP (`parse_url`): naive processing (no validation, no normalization)-->


| input string | `https://7-Eleven.com/Home/../P/Montréal` |
|:--------------|:--------------|
| PHP | unchanged |
| Python | unchanged |
| WHATWG URL | `https://xn--7eleven-506c.com/Home/P/Montr%C3%A9al` |
| curl 7.87 | `https://7-Eleven.com/P/Montr%C3%A9al` |
| Go runtime (`net/url`) | `https://7-Eleven.com/Home/../P/Montr%C3%A9al` |

<!--
footer: D
-->

<!-----

# How long are URLs?

![w:800 h:500](input_size.png)
https://github.com/ada-url/url-various-datasets/tree/main/top100

---

# How long does it take to parse a URL on average?

curl 7.81.0 (RFC 3986), written in C

- 18 000 instructions/URL
- 7 100 cycles/URL
-->

---

# Assumptions

> Does URL parsing really matter? Is it bottleneck to some performance metric? Tbh i care more about JS runtimes to handle CI/CD processes faster and more parallelized.

> URLs are free, you don't gain anything by overloading them.

<!--
footer: Y
-->

---

# HTTP Benchmark

```JavaScript
const f = require('fastify')()

f.post('/simple', async (request) => {
    const { url } = request.body
    return { parsed: url }
})

f.post('/href', async (request) => {
    const { url } = request.body
    return { parsed: new URL(url).href }
})
```

Input:
`{ "url": "https://www.google.com/hello-world?query=search\#value" }`


<!--
footer: Y
-->

---

# URL parsing was a bottleneck in Node 18.15

![graph](simplehref.png)

<!--
footer: Y
-->
---

# Wrote a C++ library (called Ada)

- Named after Ada Nizipli
- Full WHATWG URL support
- No dependency, full portability
- Over 20,000 lines of code
- Six months of work, 25 contributors
- Apache-2.0, MIT licensed
- Available at https://github.com/ada-url/ada

<!--
footer: Y
-->

---

- 6 million URLs parsed/second
- Apple M2, LLVM 14
- Wide range of realistic data sources
- Faster than alternatives in C, C++, Rust
- WHATWG URL: whatwg-url and rust-url

![bottom-right-graph](m2.png)

<!--
footer: D
-->


---

# Trick 1: perfect hashing

```C++
std::string_view names[] = {"http", " ",   "https", "ws",
                            "ftp",  "wss", "file",  " "};
enum type : uint8_t { HTTP, NOT_SPECIAL, HTTPS, WS, FTP, WSS, FILE};

type get_scheme_type(std::string_view scheme) noexcept {
  int hash_value = (2 * scheme.size() + scheme[0]) % 8;
  const std::string_view target = names[hash_value];
  if (target == scheme) {
    return type(hash_value);
  } else {
    return NOT_SPECIAL;
  }
}
```

<!--
footer: D
-->
---

# Trick 2: use memoization (tables)

https://en.wikipedia.org/wiki/Memoization


```C++
uint8_t contains_bad_char(unsigned char* input, size_t length) {
  uint8_t accumulator = 0;
  for (size_t i = 0; i < length; i++) {
    accumulator |= is_bad_char[input[i]];
  }
  return accumulator;
}
```

<!--
footer: D
-->

---

# Trick 3: use vectorization

Do no process byte-by-byte when you can process 16-byte by 16-byte.

```C++
bool has_tabs_or_newline(std::string_view user_input) {
  size_t i = 0;
  const __m128i mask1 = _mm_set1_epi8('\r');
  const __m128i mask2 = _mm_set1_epi8('\n');
  const __m128i mask3 = _mm_set1_epi8('\t');
  __m128i running{0};
  for (; i + 15 < user_input.size(); i += 16) {
    __m128i word = _mm_loadu_si128(user_input.data() + i);
    running = _mm_or_si128(
        _mm_or_si128(running, _mm_or_si128(
          _mm_cmpeq_epi8(word, mask1),
          _mm_cmpeq_epi8(word, mask2))),
          _mm_cmpeq_epi8(word, mask3));
  }
  return _mm_movemask_epi8(running) != 0;
}
```

<!-- Compilers may do it for you, but not always.-->

<!--
footer: D
-->
---

# Efficient C++/JavaScript bridge

- Passing multiple strings is expensive.
- Pass one string with offsets.

![bottom](components.png)

<!--
footer: Y
-->

---

# JavaScript Benchmark

```JavaScript
bench(filename, () => {
    for (let i = 0; i < lines.length; i++) {
      try {
        length += new URL(lines[i]).href.length;
        good_url++;
      } catch (e) {
        bad_url++;
      }
    }
    return length;
  });
```

https://github.com/ada-url/js_url_benchmark/

<!--
footer: Y
-->

---

# JavaScript Results

![w:800 h:500](runtimem2.png)

<!--
footer: Y
-->

<!--
---

# URL parsing no longer a bottleneck in Node 20

| node version | request/second (simple)    | request/second (href) | gap |
|--------------|-----------|------------|----|
| 20.1      | 61k | 59k      | 3% |

-->

---

# The Ada C++ library is safe and efficient

- Modern C++
- Sanitizers
- Fuzzing
- Unit tests

$\to$ A few minor bugs were reported, mostly related to the standard. Quickly fixed.

<!--
footer: D
-->

---

# Ada is available in the language of your choice

- JavaScript with Node.js
- C bindings at https://github.com/ada-url/ada
- Rust bindings at https://github.com/ada-url/rust
- Go bindings at https://github.com/ada-url/goada
- Python bindings at https://github.com/ada-url/ada-python
- R bindings at https://github.com/schochastics/adaR

Often the only way to get WHATWG URL support!

<!--
footer: Y
-->
---

# Links

- https://www.ada-url.com (includes a playground)
- @yagiznizipli's blog: https://www.yagiz.co
- @lemire's blog: https://lemire.me

<!--
footer: Y
-->
