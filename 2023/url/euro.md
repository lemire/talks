---
marp: true
theme: base
title: Parsing Millions of URLs per Second
description: With the end of Dennard scaling, the cost of computing is no longer falling at the hardware level: to improve efficiency, we need better software. Competing JavaScript runtimes are sometimes faster than Node.js: can we bridge the gap? We show that Node.js can not only match faster competitors but even surpass them given enough effort. URLs are the most fundamental element in web applications. Node.js 16 was significantly slower than competing engines (Bun and Deno) at URL parsing. By reducing the number of instructions and vectorizing sub-algorithms, we multiplied by three the speed of URL parsing in Node.js (as of Node.js 20). If you have upgraded Node.js, you have the JavaScript engine with the fastest URL parsing in the industry with uncompromising support for the latest WHATGL URL standard. We share our strategies for accelerating both C++ and JavaScript processing in practice.
paginate: true
_paginate: false
---



<!-- ![center](simdjsonlogo.png)-->

<!--  --- -->

## <!--fit--> Parsing Millions of URLs per Second


Yagiz Nizipli

blog: https://www.yagiz.co 
twitter: [@yagiznizipli](https://twitter.com/yagiznizipli)
GitHub: [https://github.com/anonrig](https://github.com/anonrig)



Daniel Lemire 
blog: https://lemire.me 
twitter: [@lemire](https://twitter.com/lemire)
GitHub: [https://github.com/lemire/](https://github.com/lemire/)



---

# State of Node.js Performance 2023

> Since Node.js 18, a new URL parser dependency was added to Node.js — Ada. This addition bumped the Node.js performance when parsing URLs to a new level. Some results could reach up to an improvement of 400%. (State of Node.js Performance 2023)

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

---

# Examples

- Long URLs: `http://nodejs.org:89/docs/latest/api/foo/bar/qua/13949281/0f28b//5d49/b3020/url.html#test?payload1=true&payload2=false&test=1&benchmark=3&foo=38.38.011.293&bar=1234834910480&test=19299&3992&key=f5c65e1e98fe07e648249ad41e1cfdb0`
- non-ASCII: `http://你好你好.在线`
- File: `file:///foo/bar/test/node.js`
- JavaScript: `javascript:alert("node is awesome");`
- Percent Encoding: `https://\%E4\%BD\%A0/foo`
- Pathname with dots: `https://example.org/./a/../b/./c`

---

# WHATWG URL

A common use of a URL parser is to take a URL string and normalize it. Doing so properly 
is important when supporting internalized URLs.
The WHATWG URL specification has been adopted by most browsers.  Other tools, such as curl 
and many  standard libraries, follow RFC 3986 and other older specification. 
The following table illustrates possible differences in practice
(encoding of the host, encoding of the path):

| string source | string value |
|:--------------|:--------------|
| input string | https://www.7‑Eleven.com/Home/Privacy/../Montréal |
| ada's normalized string | https://www.xn--7eleven-506c.com/Home/Montr%C3%A9al |
| curl 7.87 | https://www.7‑Eleven.com/Home/Montréal |

---

# How long are URLs?

![w:800 h:500](input_size.png)
https://github.com/ada-url/url-various-datasets/tree/main/top100

---

# How long does it take to parse a URL on average?

curl 7.81.0 (RFC 3986)

- 18 000 instructions/URL 
- 7 100 cycles/URL

---

# http benchmark

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

---

| node version | request/second (simple)    | request/second (href) | gap |
|--------------|-----------|------------|----|
| 18.15 | 60k     | 54k       | 10%  |
| 20.1      | 61k | 59k      | 3% |


---

# The ada C++ library is safe

- Fuzzing
- Extensive tests
