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
# Week 3

Conquer the Web
---

```Python
    try:
        something
    except:
        do something
```

---
```Python
file = open('file_path', 'w')
try:
    file.write('hello world')
finally:
    file.close()
```
---

```Python
    try:
        something
    except:
        do something
```

---
```Python
with open('file_path', 'w') as file:
    file.write('hello world !')
```

---
# String aggregation

- "ab" + "ac"
- "sb" + str(1)


---
# HTML

```HTML
<html>
<body>
</body>
</html>
```


---
# HTML

```HTML
<html>
<body>
    <p> Hello World </p>
</body>
</html>
```

---
# HTML

```HTML
<html>
<body>
    <p> <a href="https://google.com">Hello World</a> </p>
</body>
</html>
```
---
# HTML

---
# TCP/UDP

- UDP: fast, naive, data can be lost $\to$ media streaming
- TCP: connection, error checks $\to$  HTTP, web

---
# HTTP/HTTPS

- Get
- Post
- Head, Put, Delete, Connect, Options, Trace, Patch


---

Most common query is GET. A single web page can be
dozens of GET queries.


---

```Python
def search(keyword):
    result = getjson("https://api.duckduckgo.com/?q="+keyword+"&format=json")
    results = []
    for key in result["RelatedTopics"]:
      if "Result" in key:
        results.append(key["Result"])
    return results


print(search("Hamburger"))
```

---

Connections typically

http requests (types)
why can't they remain open
performance
sending and receiving images

concurrency/corruption
sqlite

package it up as a container
push it on aws

---
# Homework


