---
marp: true
theme: default
lang: en
title: Open Source as a Research Method
description: "An open-source library like simdjson or simdutf now runs in Node.js, web browsers and databases. How does academic research end up in the pockets of billions of people? Open source is not just a way to distribute results: it is a research method, with its own reproducibility, its own peer review and its own real-world data — and its own tensions."
paginate: true
footer: "SERIQ 2026 · Daniel Lemire"
inlineSVG: true
math: mathjax
---
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --paper:      #faf8f4;
  --ink:        #1c1c28;
  --muted:      #5c5c6b;
  --accent:     #14595e;
  --accent-soft:#4f9a92;
  --rule:       #e4ded3;
  --code-bg:    #f3efe7;
  --serif: "Fraunces", "Iowan Old Style", "Palatino", Georgia, serif;
  --sans:  "Inter", -apple-system, "Helvetica Neue", Arial, sans-serif;
  --mono:  "JetBrains Mono", "SF Mono", Menlo, monospace;
}

/* ---------- base ---------- */
section {
  position: relative;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--sans);
  font-size: 28px;
  line-height: 1.5;
  letter-spacing: .005em;
  padding: 70px 80px 64px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* hairline letterhead rule along the top of content slides */
section:not(.lead) {
  border-top: 3px solid var(--accent);
}

/* ---------- headings ---------- */
h1, h2, h3 {
  font-family: var(--serif);
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -.01em;
  margin: 0 0 .5em;
}
section:not(.lead) h1 {
  font-size: 1.85em;
  line-height: 1.12;
}
section:not(.lead) h1::after {
  content: "";
  display: block;
  width: 2.2em;
  height: 3px;
  margin-top: .32em;
  background: var(--accent);
  border-radius: 3px;
}
section:not(.lead) h2 {
  font-size: 1.25em;
  font-weight: 500;
  font-style: italic;
  color: var(--accent);
}

/* ---------- lists ---------- */
ul, ol { margin: .3em 0; padding-left: 1.1em; }
li { margin: .42em 0; padding-left: .3em; }
ul > li::marker { color: var(--accent); content: "▪  "; }
ol > li::marker { color: var(--accent); font-weight: 600; }

strong { color: var(--accent); font-weight: 600; }
a { color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--rule); }

/* ---------- tables (editorial: hairlines only, no grid, no zebra) ---------- */
section table {
  border: none;
  border-collapse: collapse;
  margin: .4em auto;
  font-size: .92em;
  width: auto;
}
section table tr,
section table tbody tr:nth-child(2n) { background: transparent !important; }
section table th,
section table td {
  border: none !important;
  background: transparent !important;
  padding: .55em 1.1em;
}
section table thead th {
  font-family: var(--sans);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .06em;
  font-size: .8em;
  color: var(--muted);
  border-bottom: 2px solid var(--ink) !important;
  text-align: left;
}
section table tbody td { border-bottom: 1px solid var(--rule) !important; }
section table tbody tr:last-child td { border-bottom: 2px solid var(--ink) !important; }

/* ---------- blockquotes ---------- */
blockquote {
  border: none;
  margin: 0;
  padding: 0 0 0 .1em;
  font-family: var(--serif);
  font-style: italic;
  font-weight: 400;
  font-size: 1.28em;
  line-height: 1.5;
  color: var(--ink);
  position: relative;
  max-width: 26em;
}
blockquote::before {
  content: "\201C";
  position: absolute;
  left: -.42em;
  top: -.36em;
  font-size: 3em;
  line-height: 1;
  color: var(--accent);
  opacity: .22;
}
blockquote p { margin: .3em 0; }

/* ---------- code ---------- */
code { font-family: var(--mono); }
:not(pre) > code {
  background: var(--code-bg);
  color: var(--accent);
  padding: .1em .4em;
  border-radius: 5px;
  font-size: .85em;
}
pre {
  background: var(--code-bg);
  border: 1px solid var(--rule);
  border-radius: 12px;
  padding: .9em 1.15em;
  font-size: .74em;
  line-height: 1.55;
  box-shadow: 0 8px 24px rgba(28, 28, 40, .07);
}
pre code { color: var(--ink); background: none; }
/* larger code for short command/prompt slides */
section.prompt pre { font-size: 1.02em; line-height: 1.6; }

/* ---------- figures (exclude inline emoji) ---------- */
section img:not(.emoji),
section video {
  display: block;
  margin: 0 auto;
  max-height: 80%;
  max-width: 92%;
  border-radius: 12px;
  box-shadow: 0 14px 38px rgba(28, 28, 40, .14);
}
section img.emoji {
  box-shadow: none;
  border-radius: 0;
}
section video {
  max-height: 68%;
  max-width: 80%;
}

/* ---------- footer & pagination ---------- */
footer {
  font-family: var(--sans);
  font-size: 15px;
  letter-spacing: .04em;
  color: var(--muted);
  opacity: .9;
}
section::after {
  font-family: var(--sans);
  font-size: 15px;
  color: var(--muted);
}

/* ---------- lead (title / closing / section dividers) ---------- */
section.lead {
  align-items: center;
  text-align: center;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(20, 89, 94, .07), rgba(250, 248, 244, 0) 70%),
    var(--paper);
}
section.lead h1, section.lead h2 {
  font-family: var(--serif);
  font-weight: 600;
  font-size: 2.6em;
  line-height: 1.08;
  letter-spacing: -.015em;
  margin-bottom: .15em;
}
section.lead h2::after {
  content: "";
  display: block;
  width: 3.2em;
  height: 3px;
  margin: .45em auto .1em;
  background: var(--accent);
  border-radius: 3px;
}
section.lead p { font-size: .92em; color: var(--muted); margin: .25em 0; }
section.lead strong { color: var(--ink); }
section.lead a { border-bottom: none; }
section.lead footer { display: none; }

/* chart slides: pack title, figure, and caption from the top */
section.chart {
  justify-content: center;
}
section.chart h1 {
  margin-bottom: .15em;
}
section.chart img:not(.emoji) {
  max-height: 540px;
  max-width: 100%;
  margin: .1em auto .05em;
  box-shadow: none;
  border-radius: 0;
}
section.diagram {
  justify-content: flex-start;
}
section.diagram img:not(.emoji) {
  max-height: 500px;
  width: auto;
  max-width: 100%;
  margin-top: .2em;
  box-shadow: none;
  border-radius: 0;
  background: transparent;
}
section.compact {
  justify-content: flex-start;
}
section.compact table {
  font-size: .78em;
  margin: .25em auto;
}
section.compact table th,
section.compact table td {
  padding: .32em .65em;
}

/* ---------- extras specific to this talk ---------- */
section.big p {
  font-family: var(--serif);
  font-size: 1.45em;
  line-height: 1.35;
  max-width: 21em;
  margin: .25em auto;
}
.stats {
  display: flex;
  gap: 2.6em;
  justify-content: center;
  margin: .55em 0 .35em;
}
.stat { text-align: center; }
.stat .n {
  font-family: var(--serif);
  font-size: 2.1em;
  font-weight: 600;
  color: var(--accent);
  line-height: 1;
}
.stat .l {
  font-size: .68em;
  text-transform: uppercase;
  letter-spacing: .07em;
  color: var(--muted);
  margin-top: .5em;
}
.cols { display: flex; gap: 2.4em; align-items: flex-start; }
.cols > div { flex: 1; }
.cols h3 {
  font-family: var(--sans);
  text-transform: uppercase;
  letter-spacing: .07em;
  font-size: .7em;
  color: var(--muted);
  font-weight: 600;
  border-bottom: 1px solid var(--rule);
  padding-bottom: .35em;
  margin-bottom: .5em;
}
.note { color: var(--muted); font-size: .78em; }
.kicker {
  font-family: var(--sans);
  text-transform: uppercase;
  letter-spacing: .09em;
  font-size: .62em;
  color: var(--accent);
  font-weight: 600;
}
section.diagram svg {
  display: block;
  margin: .4em auto 0;
  max-height: 420px;
  width: auto;
  max-width: 100%;
}

section.lead h3 {
  font-family: var(--serif);
  font-size: 1.05em;
  font-weight: 400;
  font-style: italic;
  color: var(--muted);
  margin: .1em 0 .7em;
}

/* colour-highlighted JSON on the parsing slide */
section.step { justify-content: flex-start; }
section.step h1 { margin-bottom: .28em; }
section.step .kicker { margin: .05em 0 0; }
section.step ul { margin: .2em 0 0; }
section.step pre {
  font-size: .72em;
  line-height: 1.28;
  margin: .28em 0 0;
  padding: .5em .95em .4em;
}
section.step .k { color: var(--accent); font-weight: 500; }
section.step .s { color: #9a3e2b; }
section.step .n { color: #1d4e89; }
section.step .p { color: var(--muted); }
section.diagram { justify-content: center; }
section.diagram img:not(.emoji) {
  max-height: 420px;
  max-width: 100%;
  margin: .35em auto 0;
}

/* title across the top, examples on the left, figure on the right */
section.split-figure {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  grid-template-rows: auto 1fr;
  align-content: center;
  column-gap: 1.5em;
}
section.split-figure h1 { grid-column: 1 / -1; }
section.split-figure ul { margin: .2em 0 0; }
section.split-figure p:has(img) {
  grid-column: 2;
  grid-row: 2;
  margin: 0;
  align-self: center;
}
section.split-figure img:not(.emoji) {
  max-height: 430px;
  max-width: 100%;
  width: auto;
  margin: 0;
}

/* quote slide */
section.quote { justify-content: center; }
section.quote blockquote {
  font-size: 1.12em;
  max-width: 30em;
  margin: .1em 0 .1em .5em;
}
section.quote .attrib {
  margin: 1.1em 0 0 .6em;
  font-size: .82em;
  color: var(--muted);
}
section.quote .attrib strong { color: var(--ink); }

/* quote with a portrait on the right */
section.quote.with-photo {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 2.4em;
}
section.quote.with-photo .quote-text {
  flex: 1 1 auto;
  min-width: 0;
  padding-left: .45em;
}
section.quote.with-photo blockquote {
  font-size: 1.08em;
  max-width: none;
  margin: 0;
}
section.quote.with-photo .attrib { margin: .95em 0 0 .15em; }
section.quote.with-photo figure.portrait {
  margin: 0;
  flex: 0 0 auto;
}
section.quote.with-photo figure.portrait img {
  width: 332px;
  height: 442px;
  max-width: none;
  max-height: none;
  margin: 0;
  object-fit: cover;
  border-radius: 10px;
}
section.quote.with-photo figure.portrait.wide img {
  width: 480px;
  height: auto;
  max-height: 400px;
  object-fit: contain;
}
section.quote.with-photo figure.portrait figcaption {
  margin-top: .4em;
  font-size: 13px;
  letter-spacing: .02em;
  color: var(--muted);
  text-align: right;
}

</style>


<!-- _class: lead -->
<!-- _paginate: false -->

## Open Source as a Research Method

### *From the research paper to billions of devices*

**Daniel Lemire**, professor
Université du Québec (TÉLUQ)

blog: https://lemire.me

X: [@lemire](https://x.com/lemire) · GitHub: [github.com/lemire](https://github.com/lemire/)


---

<!-- _class: quote with-photo -->

<div class="quote-text">

<blockquote>
<p>The problem in this business isn't to keep people from stealing your ideas; it's making them steal your ideas.</p>
</blockquote>

<p class="attrib"><strong>Howard Aiken</strong><br>quoted by David Patterson, 2017 Turing Award</p>

</div>

<figure class="portrait wide">
<img src="aiken.jpg" alt="Howard Aiken">
</figure>

---

<!-- _footer: "" -->

![bg contain](arxiv_monthly.png)

---

# The linear model of innovation

- The professor thinks. The professor publishes.
- The engineer reads, designs.
- The customer consumes.

---

<!-- _class: quote with-photo -->

<div class="quote-text">

<blockquote>
<p>The industrial revolution was driven by demand for cheap and better clothing for the masses.</p>
</blockquote>


</div>

<figure class="portrait">
<img src="eugenie.jpg">
<figcaption>David Monniaux, CC BY-SA 4.0</figcaption>
</figure>

---

<!-- _class: quote with-photo -->

<div class="quote-text">

<blockquote>
<p>In effect, our customer has vanished and been replaced by either the whales or a vacuum. This loss of our customer has resulted in a collection of bad effects. First, there are no “real world” clients to keep us focused.</p>
</blockquote>

<p class="attrib"><strong>Michael Stonebraker</strong> — “Where We Have Failed”<br><em>Making Databases Work</em>, 2018</p>

</div>

<figure class="portrait">
<img src="stonebraker.jpg" alt="Michael Stonebraker">
<figcaption>David Monniaux, CC BY-SA 4.0</figcaption>
</figure>






---

<!-- _class: lead -->


## A story: *simdjson*


---

<!-- _class: step -->

# Step 1 — parsing JSON

<p class="kicker">2019</p>

- JSON is everywhere, and parsing it is **slow**

<pre><code><span class="p">{</span>
  <span class="k">"Image"</span><span class="p">:</span> <span class="p">{</span>
    <span class="k">"Width"</span><span class="p">:</span> <span class="n">800</span><span class="p">,</span>
    <span class="k">"Height"</span><span class="p">:</span> <span class="n">600</span><span class="p">,</span>
    <span class="k">"Title"</span><span class="p">:</span> <span class="s">"View from 15th Floor"</span><span class="p">,</span>
    <span class="k">"Thumbnail"</span><span class="p">:</span> <span class="p">{</span>
      <span class="k">"Url"</span><span class="p">:</span> <span class="s">"http://www.example.com/81989943"</span><span class="p">,</span>
      <span class="k">"Height"</span><span class="p">:</span> <span class="n">125</span><span class="p">,</span>
      <span class="k">"Width"</span><span class="p">:</span> <span class="n">100</span>
    <span class="p">}</span>
  <span class="p">}</span>
<span class="p">}</span></code></pre>

---

<!-- _class: quote with-photo -->

<div class="quote-text">

<blockquote>
<p>The scientist builds in order to study; the engineer studies in order to build.</p>
</blockquote>

<p class="attrib"><strong>Frederick P. Brooks, Jr.</strong><br>“The Computer Scientist as Toolsmith II,” CACM, 1996</p>

</div>

<figure class="portrait">
<img src="brooks.jpg" alt="Frederick P. Brooks, Jr.">
<figcaption>David Monniaux, CC BY-SA 3.0</figcaption>
</figure>

---

<!-- _class: chart -->
<!-- _footer: "" -->

![JSON parsing: simdjson at 4800 MB/s on an Intel Xeon Gold 6548N, twitter.json](simdjson_parsing.png)

---

<!-- _class: quote -->

# The real publication

> An article about computational science in a scientific publication is not the scholarship itself, it is merely advertising of the scholarship. The actual scholarship is the complete software development environment and the complete set of instructions which generated the figures.

<p class="attrib"><strong>Jon Claerbout</strong> — as recorded by Buckheit and Donoho, 1995</p>


---

# Step 2 — bottleneck: numbers

<p class="kicker">Revealed by use</p>

- Once everything else is fast, parsing **floating-point numbers** becomes the bottleneck.
- Result: the **Eisel-Lemire** algorithm, exact and fast (*Number Parsing at a Gigabyte per Second*).
- Adoption: Rust, Go, .NET, C++ — the standard libraries themselves.
---

<!-- _class: quote -->

# Where do ideas come from?

> I never come up with anything by going off to a mountaintop to think. Instead, my ideas come from two sources: talking to real users with real problems and then trying to solve them. This ensures I come up with ideas that somebody cares about and the rubber meets the road and not the sky.

<p class="attrib"><strong>Michael Stonebraker</strong> — 2014 Turing Award · Ingres, PostgreSQL, Vertica</p>

---

# Step 3 — another bottleneck: UTF-8

<p class="kicker">Revealed by use</p>

- Parsing JSON also means **validating** UTF-8: security depends on it.
- Goal reached: validation in **less than one instruction per byte**.
- That piece broke off to become a library of its own: **simdutf**.
- Adoption: Node.js, Bun, Deno, browsers — Unicode validation and transcoding for the web.

---

<!-- _class: quote with-photo -->

<div class="quote-text">

<blockquote>
<p>For my successful projects, the early indicators were not papers or awards, but non-researchers trying to use our ideas.</p>
</blockquote>

<p class="attrib"><strong>David Patterson</strong><br>“How to Build a Bad Research Center,” CACM, 2014</p>

</div>

<figure class="portrait">
<img src="patterson.jpg" alt="David Patterson">
<figcaption>Peg Skorpinski, CC BY-SA 3.0</figcaption>
</figure>


---

<!-- _class: lead -->

## Thank you

**Daniel Lemire** · Université du Québec (TÉLUQ)

blog: https://lemire.me

X: [@lemire](https://x.com/lemire) · GitHub: [github.com/lemire](https://github.com/lemire/)

*simdjson · fast_float · simdutf · Roaring Bitmaps*
