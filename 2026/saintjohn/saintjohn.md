---
marp: true
theme: default
title: Programming in the Era of AI
description: "By some accounts, much of the practice of software programming has been transformed in recent months. Agentic AI systems can now design an application, write the code, test it, and deploy it, starting from high-level requirements. This talk examines the practical components that make current agentic approaches effective: benchmarks and tests as guiding constraints, techniques for context management, and methods for orchestrating parallel agents. It closes with what this means for what we teach, how we organize development work, and which research questions we should prioritize."
paginate: true
footer: ""
inlineSVG: true
math: mathjax
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --paper:      #faf8f4;
  --ink:        #1c1c28;
  --muted:      #5c5c6b;
  --accent:     #9a2b2b;
  --accent-soft:#c45c52;
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
  font-size: 18px;
  font-weight: 500;
  color: var(--muted);
  right: 24px;
  bottom: 18px;
  padding: 2px 10px;
  border-radius: 999px;
  background: rgba(250, 248, 244, .85);
}

/* ---------- lead (title / closing / section dividers) ---------- */
section.lead {
  align-items: center;
  text-align: center;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(154, 43, 43, .06), rgba(250, 248, 244, 0) 70%),
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
  justify-content: flex-start;
}
section.chart h1 {
  margin-bottom: .15em;
}
section.chart img:not(.emoji) {
  max-height: 390px;
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
</style>

<!-- _class: lead -->
<!-- _paginate: false -->

## Programming in the Era of AI

**Daniel Lemire**, professor
Université du Québec (TÉLUQ)
Montréal :canada:

blog: https://lemire.me

X: [@lemire](https://x.com/lemire) · GitHub: [github.com/lemire](https://github.com/lemire/)

---

# Normal vs. revolutionary science

Thomas Kuhn, *The Structure of Scientific Revolutions* (1962)

- **Normal science**: puzzle-solving inside an accepted paradigm. Shared tools, shared methods, shared idea of what counts as a good answer.
- **Revolutionary science**: anomalies pile up, the old paradigm cracks, a new one replaces it.
- After a revolution, the old experts are not always the best guides.

**Is programming in a period of normal science, or of revolution?**

---

# Where I am coming from

- Author of high-performance libraries integrated into major browsers, runtimes and standard libraries: **simdutf**, **fast_float**, **simdjson**, **Roaring Bitmaps**.
- Among the top 2% of scientists worldwide (Stanford/Elsevier), 100+ peer-reviewed papers.
- Among the 1000 most-followed developers on GitHub.
- **And: I have not typed most of my code by hand in over a year.**

---

<!-- _class: lead -->

## Preface

## Back in the 1990s

---

# The singularity

> « I believe that the creation of greater than human intelligence will occur during the next thirty years. (I'll be surprised if this event occurs before 2005 or after 2030.)  »

Vernor Vinge, 1993


---

<!-- _class: lead -->

## Part 1

## Where we actually are


---

![bg contain](screenshot_20261020.png)


---

# SWE-bench Verified

- Real GitHub issues from real open-source Python repositories.
- The model gets the repository, the issue text, and nothing else.
- Success = the project's own **hidden tests** pass afterwards.
- 500 tasks, human-validated as solvable.



---

![bg](sota_frontier.png)





---

# Terminal-Bench 4.0

- The agent gets a **real terminal** in a sandboxed container.
- Tasks: build, configure, debug, migrate, train... whatever the shell allows.
- Success = automated tests check the final state of the machine.
- 66 hard tasks, up to 8 hours each (August 2026).

**Human experts scored about 50% on Terminal-Bench 2.0.**
**There is no human baseline for 4.0.**

---

![bg contain](8Jn4M.png)

---

![bg right:60% contain](stripe.png)

> January 1st marked the beginning of the singularity.

—Stripe, August 19, 2026

---

![bg right:40% contain](andreesen.png)

> People often talk about this concept called AGI, meaning artificial general intelligence, that is, an AI as intelligent as a person. I actually think we crossed that threshold about three months ago.

— Marc Andreessen, May 19, 2026

---

# A summer of AI optimization

- Six mature open-source libraries: roaring, CRoaring, ada, fast_float, simdjson, simdutf.
- Shipped in GCC, Chromium, Node.js... used by millions.
 
---

![bg contain](summer_timeline.png)

---   c



---

<!-- _class: lead -->

## Are we all going to be out of a job?



---

![bg contain](U6BRG.png)

---

![bg contain](software_dev_postings.svg)




---

# Jevons paradox

- 1865: William Stanley Jevons, *The Coal Question*.
- James Watt's steam engines burned far less coal per unit of work...
- ...and Britain's coal consumption **went up**, not down.

**When something gets cheaper to use, we use much more of it.**

- Tokens got cheaper: we consume far more tokens.
- Code got cheaper: we write far more code, and review, test, host and maintain it.


---

<!-- _class: lead -->

## How does it work

---

<!-- _class: diagram -->

# How an LLM works

![](llm_pipeline.svg)



---

![bg contain](open_weights.png)

---

![bg fit](grok-weights.png)


---

![bg contain](4dVwN.png)

---


# How can a language model write software?

* I write a query, it is maybe 80 characters.
* I get back a full program with 100,000 lines.
* Not how it works, there is more information invovled.

---


<!-- _class: diagram -->

# The inference loop

![](inference_loop.svg)





---

<!-- _class: diagram -->

# Reinforcement learning

![](rl_loop.svg)



---

![bg contain](HTyCNdbX0AAEu9V.jpeg)


---

<!-- _class: diagram -->

# Jagged: metacognition

![](jagged_metacognition.svg)

---

<!-- _class: diagram -->

# Jagged: sensorimotor skill

![](jagged_sensorimotor.svg)

---

# Moravec's paradox

> « It is comparatively easy to make computers exhibit adult level performance on intelligence tests or playing checkers, and difficult or impossible to give them the skills of a one-year-old when it comes to perception and mobility. »

Hans Moravec, *Mind Children*, 1988

---

<!-- _class: diagram -->

# Jagged: visual-spatial reasoning

![](jagged_spatial.svg)

---

<!-- _class: diagram -->

# Jagged: long-term memory

![](jagged_memory.svg)


---

<!-- _class: lead -->

## Human attention is limited

---

![bg contain](llm_writing.png)

---



![bg contain](arxiv_monthly.png)

---

# arXiv capped submissions at two a month

- October 1, 2026: **two submissions per person per month.**
- September 2026: over 40,000 papers, up from about 20,000 two years earlier.
- Doubling every two years. Moderated by volunteers.
- Google stopped accepting new bug reports in its open-source bounty program: they could not cope with the influx.


<small>lemire.me/blog/2026/10/04/arxiv-capped-submissions-at-two-a-month/</small>




---


![bg](github-outage.png)


---

![bg contain](bugpoll.png)


---

<!-- _class: lead -->

## Emerging ideas

---

# Emerging idea: ephemeral testing

1. Build a component (by hand or with an agent).
2. Ask an agent to build **throwaway software on top of it**: an app, another layer.
3. Have it test what it built.
4. Judge the foundation by how well the layers above work. Then discard them.

<small>lemire.me/blog/2026/10/05/ephemeral-testing/</small>

---

![bg right:45% contain](layered_model.svg)

# Emerging idea: a layered model

- Keep a **small core** that changes slowly and on purpose.
- For the core, you read the code. You insist on tests. No vibe coding.
- **Everything else can move fast.** There will be bugs, but the AI fixes them quickly.
- **The core cannot depend on the outer layers.**

<small>lemire.me/blog/2026/09/05/ai-programming-a-layered-model/</small>



---

# Emerging idea: AI cloning


- WordCraft → Microsoft Word  https://getartcraft.com/apps/wordcraft
- GridCraft → Microsoft Excel https://getartcraft.com/apps/gridcraft
- DeckCraft → Microsoft PowerPoint https://getartcraft.com/apps/deckcraft
- PhotoCraft → Photoshop https://getartcraft.com/apps/photocraft
- VectorCraft → Illustrator https://getartcraft.com/apps/vectorcraft


---

## Business challenge

- Once your application is public, people can clone it.
- Meaning of copyright changed. Think fashion industry, cooking.

---

# Emerging idea: cheap custom software

1. Build your own video software https://github.com/lemire/lemirecut
2. Your own election-night app https://lemire.me/montmorency2026/

---

## Business opportunity

- Help people deploy software specific for their needs, even if just 3 users.
- Build throw-away application (short lived)


---


# Emerging idea: AI-first operating software

![bg right:60% contain](omarchy.png)




---

# Summary

1. **It is real**: benchmarks near saturation; mature libraries 2–5× faster in one summer.
2. **Cheaper code means more code** (Jevons), not less work.
3. **An agent is a model in a loop**: tools, tests, reinforcement on verifiable outcomes.
4. **The skills are jagged**: superhuman at some tasks, weak at self-doubt, touch, space and memory.
5. **Human attention is the bottleneck**: review, moderation, trust.
6. **New practices are emerging**: ephemeral testing, a small stable core, custom software for a few users.

---

<!-- _class: lead -->

## Questions?

**Daniel Lemire** — [lemire.me](https://lemire.me) (blog)

<https://simdjson.org> · <https://roaringbitmap.org>

<https://simdutf.github.io/simdutf/> · <https://fastfloat.github.io/fast_float/>

:canada:

credit : @fromdevoid @birkenkrahe @gcomeaudotcom @JoyfulBadger @nabendu82 @MatRopert @dyaroshev @opdroid1234 @jrdi @Hassan_Abedi @NinadSachania @RonanTournier
