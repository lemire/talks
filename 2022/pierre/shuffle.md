---
marp: true
theme: base
title: Floating-point number parsing with perfect accuracy at a gigabyte per second
description: Parsing decimal numbers from strings of characters into binary types is a common but relatively expensive task.
paginate: true
_paginate: false
---



<!-- ![center](simdjsonlogo.png)-->

<!--  --- -->


# shuffle


```
__m128i _mm_shuffle_epi32 (__m128i a, int imm8)
```

---

# 32-bit

```
__m128i a = _mm_setr_epi32(1,2,3,4);
```



---



```
__m128i p = _mm_shuffle_epi32 (a, 0b11100100);
```


---

```
__m128i p = _mm_shuffle_epi32 (a, 0b00011011);

```

