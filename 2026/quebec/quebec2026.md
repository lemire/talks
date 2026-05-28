---
marp: true
theme: base
title: La prochaine frontière : IA et code
description: "Présentation sur l'impact de l'intelligence artificielle sur le développement logiciel, la génération de code, la performance et l'avenir de la profession de programmeur."
paginate: true
_paginate: false
inlineSVG: true
---


## <!--fit--> La prochaine frontière : IA et code

Christian Jauvin, professeur
Daniel Lemire, professeur
Université du Québec (TÉLUQ)
Montréal :canada:

blogs: https://cjauvin.github.io  https://lemire.me

X: [@ChristianJauvin](https://x.com/ChristianJauvin)  [@lemire](https://x.com/lemire)
GitHub: [https://github.com/cjauvin](https://github.com/cjauvin) [https://github.com/lemire/](https://github.com/lemire/)


---


![](aiuse.png)


---

![bg right:40% contain](andreesen.png)


> Um, and so I I actually people talk about this concept called AGI, which means artificial general intelligence, which basically means an AI that's as smart as a person. And I actually think we crossed that about 3 months ago. (Andreesen, 19 mai 2026)



---


![bg right:40% contain](progress.png)


---


![bg right:40% contain](ranking.png)

---

# Agentic AI


- Comprendre des objectifs
- Les décomposer en étapes
- Utiliser des outils (recherche web, exécution de code, APIs, etc.)
- Itérer et s’adapter en fonction des résultats

---


![](copilot.png)




---


![](grok.png)


---


![](claude.png)

---

# MarkDown

```markdown
## Introduction à Java (exemple)

Nous pouvous définir une variable en Java ainsi.

Notez les *différents* éléments de la syntaxe.

- Type
- Nom de variable
- Assignation d'une valeur
```


---

# Skills (compétences)


- Un dossier réutilisable contenant un fichier `SKILL.md` 
- Un mécanisme de chargement dynamique : l'IA ne charge que le nom et la description au démarrage
- Un moyen de créer des agents spécialisés


---

# Exemple

- Aller chercher des données officielles
- Créer un graphique (`PNG`)
- Anglais/Français


---

# Créer le dossier

Le skill va se nommer `plotdata`.

```
mkdir -p ~/.claude/skills/plotdata
```


---

# Créer le fichier

```
~/.claude/skills/plotdata/SKILL.md
```

---

```MarkDown
---
name: data-plot
description: Fetches data from the web and generates
 publication-quality matplotlib plots in both French and English.
allowed-tools: Bash(mkdir *) Bash(uv *) Bash(python3 *) 
  Bash(curl *) Bash(wget *) Bash(ls *) Bash(cat *) Bash(cd *) 
  WebFetch WebSearch Read Write Edit
argument-hint: [query describing the data to plot]
---
```


---

```MarkDown

# Data Plot Skill

Given a query, find reliable online data, download it, and produce bilingual 
(French/English) matplotlib plots.

## Working directory

All output goes in `~/myplots/<slug>/` where `<slug>` is a short kebab-case name

1. Ensure `~/myplots` exists (`mkdir -p ~/myplots`)
2. Create the subdirectory for this query, e.g. `~/myplots/canada-population-2024/`
3. All scripts, data, README, and PNGs go in that subdirectory

## Data sourcing

- Prefer official/government sources
- Prefer machine-readable formats in this order: **CSV > JSON > HTML table**
- Use WebSearch + WebFetch to locate the dataset URL.
- Record the exact source URL and access date for the README.

## Python environment

Always use `uv` for dependencies. Initialize the project in the subdirectory:

```bash
cd ~/myplots/<slug>
uv init --no-readme --no-workspace
uv add pandas matplotlib requests
```


---

# Utilisation

```
 /plotdata  I want the fertility rate per canadian province along 
  with the percentage of woman in each  province with a university degree.
````

---



![](claudeplotresult.png)


---

# Et voilà!

- Rédige le skill une fois
- Automatise la production de graphiques

![bg right:40% contain](plot_sm.png)


---

```
/plotdata fait un graphique qui donne l'âge moyen 
par province au Canada, et ajoute l'âge moyen 
aux États-Unis (comme onzième province).
```

![bg right:40% contain](plot_age.png)



---

# Permissions


- `~/.claude/settings.json``

```json
{
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash(git status)", "Bash(git commit -m:*)"],
    "deny": ["Read(.env*)", "Bash(rm -rf /)", "Bash(sudo:*)"],
    "ask": ["Bash(git push --force:*)", "Bash(docker run:*)"]
  }
}
```

---

# allow, deny, ask

- `allow`: actions autorisées automatiquement (faible risque, frequentes).
- `deny`: actions interdites en tout temps (secrets, operations destructives).
- `ask`: actions sensibles qui exigent une confirmation explicite.



---

# MCP (Model Context Protocol)

- Relie un LLM a des outils externes.
- Il standardise l'acces aux outils.
- Exemple: Git, Slack, Oracle,  PostgreSQL, SSH, Google Drive.


---

# Etendre des skills en securite

- N'exposer que les actions strictement nécessaires dans le serveur MCP.
- Traçabilite: journaliser les appels MCP et auditer regulierement.

Exemple: pour un skill SSH/SFTP, on autorise lecture/ecriture dans un seul dossier et on place toute operation destructive en mode `ask`.


---

# Exemple de serveur MCP: server.py

- Ce script démarre un serveur MCP nomme `ssh-files`.
- Il lit `credentials.json` (host, username, remotedirectory) pour se connecter en SSH/SFTP.
- Il expose des outils: `upload_file`, `download_file`, `list_files`, `make_dir`, `delete_file`, `delete_dir`.
- Tous les chemins sont confinés à `remotedirectory` (protection contre la sortie de sandbox).
- Il applique des garde-fous: verification des clés SSH.

---

```
claude mcp add ssh-files server.py  --scope user 
```


---

`claude mcp list`

  - claude.ai Google Drive — needs authentication
  - claude.ai Gmail — needs authentication
  - claude.ai Google Calendar — needs authentication
  - ssh-files (./ssh-mcp/server.py) — ✓ Connected


---


> Upload using the  ssh-files  MCP to a corresponding directory. And give me the URL. Create a nice index.html file.

---


```
/data-plot Estimated market value of Anthropic, OpenAI and xAI.
```

---


![bg right:40% contain](web.png)


https://lemire.me/plot_data/ai-lab-valuations/


---

Bonjour Claude,
Dans le dossier "TRA 4030", tu vas trouver des documents word (docx) représentant le contenu du cours TRA 4030 dans son état actuel.
Je veux que tu me fasses un site web moderne (dans le dossier html) avec une version moderne du cours. Tu vas copier le contenu du cours vers mon site à https://lemire.me/trad4030/
La TÉLUQ a l'habitude de diviser un cours en modules. Dans chaque module, il y a des sections courantes comme "démarrer, s'informer, etc.". Je t'invite à explorer le contenu du site https://m2.teluq.ca/course/view.php?id=3274
Essaie de copier le style du site.
N'oublie pas d'inclure une feuille de route. Le cours dure 15 semaines.

![bg right:40% contain](vieux.png)


---

https://lemire.me/trad4030/

![bg right:40% contain](nouveau.png)


---

Rest is garbage -- stop here.

---


 reordered so each one builds on the last:

MCP — The foundation. Before agents can do anything interesting, they need a standard way to talk to tools and data. Start here because everything downstream assumes the model can reach outside itself.

Google Calendar, Drive, Slack, GitHub, Git, Postgres,


Hooks — Once your agent is doing real work, you need control. Hooks are how you intercept, validate, log, or block agent behavior at runtime. This is the discipline layer — the move from "it works on my machine" to "it works in production."
Git worktrees — With a controlled single agent working well, the next question is parallelism. Worktrees let one agent (or many) operate on isolated branches simultaneously without stepping on each other. The infrastructure prerequisite for what comes next.
Subagents / agent orchestration — Now spawn them. A primary agent delegates specialized work to children — research, refactoring, testing — each in its own context and (often) its own worktree. This is where the earlier pieces compound.
Autoresearch — The capstone. An agent that plans, spawns subagents, uses MCP-connected tools and skills, runs in worktrees, is governed by hooks, and goes off for hours to investigate something. Every prior topic shows up here.

---

# Plan de la présentation

- L'état actuel de l'IA générative pour le code
- Comment fonctionnent les grands modèles de langage (LLM)
- Outils d'assistance au codage
- Qualité et performance du code généré
- Impacts sur la profession
- Ce qui vient ensuite

---

# La révolution en cours

- Les LLM génèrent du code depuis ~2021 (Codex, Copilot)
- En 2026, les assistants IA sont omniprésents
- Plus de 70% des développeurs utilisent un assistant IA
- La question n'est plus « si » mais « comment »

---

# Qu'est-ce qu'un grand modèle de langage?

- Réseau de neurones entraîné sur d'immenses corpus de texte
- Prédit le prochain jeton (token) dans une séquence
- Le code est du texte : les LLM s'y appliquent naturellement
- Pas de « compréhension » au sens humain, mais une capacité de synthèse remarquable

---

# L'entraînement en bref

- Phase 1 : pré-entraînement sur des milliards de lignes de code
- Phase 2 : fine-tuning avec des exemples de haute qualité
- Phase 3 : RLHF — apprentissage par rétroaction humaine
- Résultat : un modèle qui produit du code syntaxiquement correct la majorité du temps

---

# Les outils d'aujourd'hui

| Outil | Approche |
|---|---|
| GitHub Copilot | Complétion en ligne dans l'éditeur |
| Claude Code | Agent en ligne de commande |
| Cursor / Windsurf | IDE augmenté par IA |
| ChatGPT / Claude | Conversation interactive |
| Codex CLI | Exécution autonome de tâches |

---

# Démonstration typique

```python
# Demande : trier une liste de dictionnaires par clé "score"
données = [{"nom": "Alice", "score": 88},
           {"nom": "Bob", "score": 95},
           {"nom": "Charlie", "score": 72}]

résultat = sorted(données, key=lambda x: x["score"],
                  reverse=True)
```

L'IA génère ce code en moins d'une seconde.
Mais est-ce **performant**?

---

# Le piège de la facilité

- Le code généré compile et passe les tests de base
- Mais il peut être :
  - Sous-optimal en performance
  - Fragile face aux cas limites
  - Difficile à maintenir
- « Ça marche » ≠ « C'est bon »

---

# Mesurer la performance : pourquoi c'est crucial

- Un programme 10× plus lent, c'est 10× plus de serveurs
- L'énergie consommée est proportionnelle au temps CPU
- La performance, c'est aussi de la durabilité
- Daniel Lemire : « La performance n'est pas un luxe, c'est une responsabilité »

---

# Exemple : parsing JSON

- **simdjson** : ~3 Go/s sur un seul cœur
- Code naïf généré par IA : ~200 Mo/s
- Facteur **15×** de différence
- L'IA ne connaît pas les instructions SIMD spécialisées
- L'expertise humaine reste irremplaçable pour l'optimisation bas niveau

---

# L'IA et les algorithmes

- Les LLM reproduisent les algorithmes courants (tri, recherche)
- Mais peinent avec :
  - L'optimisation vectorielle (SIMD)
  - Les structures de données non standard
  - Les compromis espace/temps subtils
- Les algorithmes nouveaux exigent encore une réflexion humaine

---

# Bitmaps compressés : un cas d'étude

- Roaring Bitmaps : utilisé par Google, Apache, Uber
- Structure hybride : tableaux, bitmaps, runs
- L'IA peut *utiliser* la bibliothèque
- Mais elle ne pourrait pas *inventer* cette structure
- L'innovation algorithmique reste humaine

---

# Ce que l'IA fait bien

- Écrire du code « boilerplate »
- Traduire entre langages
- Générer des tests unitaires
- Documenter du code existant
- Prototyper rapidement
- Expliquer du code inconnu

---

# Ce que l'IA fait mal

- Raisonner sur la complexité algorithmique
- Optimiser pour le matériel spécifique
- Comprendre le contexte métier profond
- Gérer la concurrence et les conditions de course
- Garantir la sécurité (injections, failles)
- Maintenir la cohérence dans un grand projet

---

# Le problème de l'hallucination

- Les LLM inventent des API qui n'existent pas
- Ils citent des bibliothèques fictives
- Le code peut sembler plausible mais être incorrect
- Vérification humaine **obligatoire**
- « Faire confiance, mais vérifier » — surtout vérifier

---

# Transparence et honnêteté

- Christian Jauvin propose le concept de « Proof of Prompt »
- Idée : déclarer ouvertement quand l'IA a contribué
- Pas de honte à utiliser un outil
- Mais l'honnêteté intellectuelle exige la transparence
- Le code généré par IA devrait être étiqueté

---

# L'impact sur les développeurs juniors

- Risque : apprendre à « prompter » au lieu de « programmer »
- L'IA masque la complexité sous-jacente
- Un développeur qui ne comprend pas le code qu'il utilise est fragile
- L'apprentissage des fondamentaux reste essentiel
- L'IA est un accélérateur, pas un substitut à la compétence

---

# L'impact sur les développeurs seniors

- Productivité accrue pour les tâches répétitives
- Plus de temps pour l'architecture et la réflexion
- Nouveau rôle : « réviseur de code IA »
- La valeur se déplace vers le jugement, pas l'exécution
- Les experts en performance sont plus précieux que jamais

---

# Benchmarks : code humain vs code IA

| Tâche | Humain expert | IA (2026) |
|---|---|---|
| Code correct | 95% | 85% |
| Code performant | 80% | 40% |
| Code sécuritaire | 75% | 50% |
| Code maintenable | 85% | 60% |

*Estimations basées sur la littérature récente*

---

# Le coût énergétique de l'IA

- Entraîner un LLM : des milliers de MWh
- Chaque requête de complétion consomme de l'énergie
- Paradoxe : l'IA peut générer du code inefficace
  qui consomme *plus* de ressources à l'exécution
- Il faut mesurer le coût total : génération + exécution

---

# Les langages et l'IA

- L'IA est meilleure en Python et JavaScript (plus de données)
- Performance variable en C, C++, Rust
- Les langages moins courants (Zig, Nim) posent problème
- Biais vers les solutions « populaires », pas les « optimales »
- Le choix du langage influence la qualité de la sortie IA

---

# Tests et validation

- L'IA peut générer des tests, mais :
  - Elle teste ce qu'elle « pense » être correct
  - Les cas limites sont souvent négligés
  - La couverture est superficielle
- Le test reste une discipline humaine
- Fuzzing et tests de propriété : compléments essentiels

---

# Sécurité du code généré

- Les LLM reproduisent des patrons vulnérables (injection SQL, XSS)
- Ils ne comprennent pas les modèles de menace
- Le code généré doit passer par les mêmes revues de sécurité
- Ne jamais déployer du code IA sans audit
- La sécurité est un processus, pas une fonctionnalité

---

# L'IA comme partenaire de revue de code

- Excellente pour détecter :
  - Le code mort
  - Les incohérences de style
  - Les bogues évidents
- Moins fiable pour :
  - Les problèmes d'architecture
  - Les failles de sécurité subtiles
  - La logique métier

---

# L'avenir proche (2026–2028)

- Agents autonomes capables de résoudre des bogues complets
- Meilleure intégration avec les outils de build et CI/CD
- Modèles spécialisés par domaine (embarqué, web, données)
- Compréhension de projets entiers, pas juste de fichiers isolés
- Boucle de rétroaction : l'IA apprend du code en production

---

# L'avenir lointain : spéculations

- Programmation en langage naturel comme interface primaire?
- Les langages de programmation deviennent-ils des « bytecode »?
- Le développeur comme « architecte d'intention »?
- Ou bien : les fondamentaux restent, l'IA accélère
- L'histoire de l'informatique suggère : les abstractions montent, mais le bas niveau ne disparaît jamais

---

# Conseils pratiques

1. Utilisez l'IA pour le code jetable et le prototypage
2. Vérifiez **toujours** le code généré
3. Mesurez la performance avant de faire confiance
4. Investissez dans votre compréhension des fondamentaux
5. Soyez transparent sur l'utilisation de l'IA
6. Restez curieux : l'outil évolue rapidement

---

# Ce qu'on ne vous dit pas assez

- L'IA ne remplace pas 10 ans d'expérience en une requête
- Les benchmarks marketing ≠ la réalité du terrain
- Le code le plus rapide est celui qu'on n'exécute pas
- Un bon algorithme bat toujours un mauvais algorithme optimisé par IA
- La pensée critique est votre compétence la plus précieuse

---

# Conclusion

- L'IA transforme le développement logiciel — c'est indéniable
- Mais elle ne remplace pas l'expertise, elle l'amplifie
- La performance, la sécurité, le jugement restent humains
- Adoptons ces outils avec lucidité et rigueur
- La prochaine frontière, c'est la collaboration humain-IA

---

## <!--fit--> Questions?

Christian Jauvin — [cjauvin.github.io](https://cjauvin.github.io/)
Daniel Lemire — [lemire.me](https://lemire.me)

Merci! :canada:
