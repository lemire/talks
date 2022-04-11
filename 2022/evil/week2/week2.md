---
marp: true
theme: base
title: An evil-genius guide to computer programming
description: The six-week course is a playful guide through programming. If you have never programmed before, this course should motivate you to go further. If you are an experienced programmer, this course might help you get excited again. In this course, I will explain how programming can make you smarter. I will show how programming allows you to automate web access and find hidden treasures. I will show how programming can make you more creative and help you change the world.
paginate: true
_paginate: false
---


## <!--fit--> An evil-genius guide to computer programming



Daniel Lemire 
Montreal :canada: 

blog: https://lemire.me 
twitter: [@lemire](https://twitter.com/lemire)
GitHub: [https://github.com/lemire/](https://github.com/lemire/)

---
# Week 2

Get Smarter by Programming

---

# Random numbers

Pseudo !!!

really hard to do


---

# Loops


---

What a computer is to me is it’s the most remarkable tool that we’ve ever come up with, and it’s the equivalent of a bicycle for our minds.” ~ Steve Jobs

---

# Solve puzzling probability problems

🚪🚪🚪


---

```Python
import random

times = 1000000
hit = 0
for x in range(times):
   treasure = random.choice([1,2,3])
   mychoice = random.choice([1,2,3])
   if mychoice == treasure:
       hit += 1

print(hit / times)
# 0.333
```

---

```Python
import random

times = 1000000
hit = 0
for x in range(times):
   treasure = random.choice([1,2,3])
   mychoice = random.choice([1,2,3])
   if mychoice 1= treasure:
       hit += 1

print(hit / times)
# 0.667
```

Solve Peg solitaire

https://en.wikipedia.org/wiki/Peg_solitaire

# http://norvig.com/sudoku.html

---
# Homework


