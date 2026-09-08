---
marp: true
theme: default
title: Le logiciel libre comme méthode de recherche
description: "Une bibliothèque libre comme simdjson ou simdutf s'exécute aujourd'hui dans Node.js, les navigateurs et les bases de données. Comment la recherche universitaire se rend-elle jusque dans la poche de milliards de gens ? Le logiciel libre n'est pas qu'un mode de diffusion : c'est une méthode de recherche, avec sa reproductibilité, son arbitrage et ses données du monde réel — et ses tensions."
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

/* ---------- extras propres à cette présentation ---------- */
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

/* le diagramme du cycle : centré verticalement, bien large */
section.diagram { justify-content: center; }
section.diagram img:not(.emoji) {
  max-height: 420px;
  max-width: 100%;
  margin: .35em auto 0;
}

/* diapositive de citation */
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

</style>


<!-- _class: lead -->
<!-- _paginate: false -->

## Le logiciel libre comme méthode de recherche

### *De l'article scientifique à des milliards d'appareils*

**Daniel Lemire**, professeur
Université du Québec (TÉLUQ)

blogue : https://lemire.me

X : [@lemire](https://x.com/lemire) · GitHub : [github.com/lemire](https://github.com/lemire/)

---

# Ce matin, sans le savoir…

<div class="stats">
<div class="stat"><div class="n">2019</div><div class="l">première version</div></div>
<div class="stat"><div class="n">20 k+</div><div class="l">étoiles GitHub</div></div>
<div class="stat"><div class="n">10⁹</div><div class="l">appareils</div></div>
</div>

- Vous avez ouvert une page web : **simdutf** a validé son texte.
- Votre application a lu du JSON : **simdjson** l'a analysé.
- Un chiffre est passé de texte à nombre : **fast_float** s'en est chargé.

<p class="note">Node.js, Chrome, Safari, Rust, Go, .NET, ClickHouse… du code écrit dans un laboratoire universitaire, au Québec.</p>

---

<!-- _class: lead big -->

## La question

Comment la recherche universitaire finit-elle
**dans la poche de milliards de gens ?**


---

<!-- _class: quote -->

# D'où viennent les idées ?

> I never come up with anything by going off to a mountaintop to think. Instead, my ideas come from two sources: talking to real users with real problems and then trying to solve them. This ensures I come up with ideas that somebody cares about and the rubber meets the road and not the sky.

<p class="attrib"><strong>Michael Stonebraker</strong> — prix Turing 2014 · Ingres, PostgreSQL, Vertica</p>

---

# Le modèle linéaire de l'innovation

- Le prof réfléchit. Il publie.
- L'ingénieur lit, conçoit.
- Le client consomme.


---

# Vers un vrai modèle de l'innovation

- Révolution industrielle : sous-vêtements.
- Origine du clavier.
- ChatGPT: GPU (jeux), textes (web), chat (Discord).
- Relativité (train)

---

<!-- _class: lead -->

## Partie 1

## Le libre comme *méthode* de recherche

---



> Le logiciel libre n'est pas seulement une façon de publier des résultats de recherche : c'est une méthode de recherche à part entière.

---

# 1. Reproductibilité

- Le code **et** les bancs d'essai sont publics.
- N'importe qui peut relancer la mesure — sur sa machine, avec ses données.
- N'importe qui peut donc **vous réfuter**. C'est le but.

<p class="note">Un gain de performance qui ne survit pas à la machine d'un inconnu n'était pas un résultat.</p>

---

# 2. Une évaluation par les pairs bien réelle

<div class="cols">
<div>

### Comité de lecture

- 2 à 3 lecteurs
- Ils lisent la description
- Un seul verdict, une seule fois
- Anonyme, sans suite

</div>
<div>

### Revue de code publique

- Des centaines d'yeux
- Ils exécutent le code
- Un verdict à **chaque** version
- Signé, et il faut y répondre

</div>
</div>

<p class="note">Les revues de code, les <em>issues</em> et les demandes d'intégration sont souvent un arbitrage plus exigeant qu'un comité de lecture.</p>

---

# 3. Les données du monde réel viennent à vous

- Des **cas adversariaux** : ça ne fonctionne pas, ça ne suffit pas.
- Des **architectures exotiques** : ARM, POWER, RISC-V, WebAssembly.
- Des **charges réelles** : les fichiers que personne n'aurait pensé à fabriquer.





---

<!-- _class: lead -->

## Partie 2

## Une histoire : *simdjson*

---

<!-- _class: diagram -->

# Le cycle

![Le cycle : code libre, article, adoption, goulot suivant](cycle.svg)

---

# Acte 1 — l'analyse du JSON

<p class="kicker">2019</p>

- Le JSON est partout, et son analyse est **lente** : des centaines de mégaoctets par seconde, au mieux.
- **D'abord le code** : simdjson, écrit avec Geoff Langdale — plusieurs **gigaoctets par seconde**, grâce aux instructions SIMD.
- **Puis un billet de blogue**, GitHub, quelques messages sur X. En quelques jours, des milliers de lecteurs.
- **Puis l'adoption** : bases de données, moteurs analytiques, environnements JavaScript.
- **L'article vient après** : *Parsing Gigabytes of JSON per Second* (VLDB Journal).

<p class="note">L'ordre compte : le logiciel était déjà adopté quand l'article est paru — et l'article n'aurait pas existé sans les mesures que l'usage a rendues possibles.</p>

---

# Acte 2 — un goulot inattendu : les nombres

<p class="kicker">Révélé par l'usage</p>

- Une fois le reste accéléré, l'analyse des **nombres à virgule flottante** devient le goulot.
- Personne n'aurait posé ce problème *a priori* : c'est le profilage d'un vrai analyseur qui l'a désigné.
- Résultat : l'algorithme **Eisel-Lemire**, exact et rapide (*Number Parsing at a Gigabyte per Second*).
- Adoption : Rust, Go, .NET, C++ — les bibliothèques standards elles-mêmes.

---

# Acte 3 — un autre goulot : l'UTF-8

<p class="kicker">Révélé par l'usage</p>

- Analyser du JSON, c'est aussi **valider** de l'UTF-8 : la sécurité en dépend.
- Objectif atteint : la validation en **moins d'une instruction par octet**.
- Le morceau s'est détaché pour devenir une bibliothèque à part entière : **simdutf**.
- Adoption : Node.js, Bun, Deno, navigateurs — la validation et la transcodification d'Unicode du web.

---

# Le même cycle, trois fois

| Problème | Code | Adoption | Article |
|---|---|---|---|
| Analyse JSON | simdjson | bases de données, moteurs JS | VLDB Journal |
| Analyse des nombres | fast_float | Rust, Go, .NET, C++ | Software: P&E |
| Validation UTF-8 | simdutf | Node.js, Bun, navigateurs | Software: P&E |

<p class="note">Chaque ligne est née de la précédente. Aucune n'était au programme de recherche du départ.</p>

---

<!-- _class: lead -->

## Partie 3

## Les tensions honnêtes

---

# La maintenance est ingrate

- Le succès se paie en **rapports de bogues**, en demandes de portage, en questions.
- Une faille de sécurité dans votre code, c'est une faille dans Node.js.
- Ce travail est **sans fin** et **invisible** — il ne s'écrit dans aucun CV académique.

<p class="note">Publier un article, c'est terminer. Publier une bibliothèque, c'est commencer.</p>

---

# Les incitatifs sont mal alignés

<div class="cols">
<div>

### Ce que les comités comptent

- Les articles
- Les citations
- Les subventions

</div>
<div>

### Ce qui change le monde

- Les demandes d'intégration
- Les versions maintenues
- Les utilisateurs

</div>
</div>

**Il n'existe pas de case « adopté par un milliard d'appareils » dans un formulaire de promotion.**

---

<!-- _class: lead big -->

## Ce que je retiens

Le code ouvert **pose** les questions de recherche,
puis il en **vérifie** les réponses.

---

<!-- _class: quote -->

# La leçon du transfert

> The problem in this business isn't to keep people from stealing your ideas; it's making them steal your ideas.

<p class="attrib"><strong>Howard Aiken</strong> — cité par David Patterson, prix Turing 2017</p>

---

<!-- _class: lead -->

## Merci

**Daniel Lemire** · Université du Québec (TÉLUQ)

blogue : https://lemire.me

X : [@lemire](https://x.com/lemire) · GitHub : [github.com/lemire](https://github.com/lemire/)

*simdjson · fast_float · simdutf · Roaring Bitmaps*
