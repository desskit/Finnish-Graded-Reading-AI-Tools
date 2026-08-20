# manifest.md — Finnish Graded Reading Project

Living reference for the project. Updated additively; the changelog at the bottom
is append-only.

Companion files: `finnish-skills.md` (grammar and pedagogy reference),
`tools/` (Kotus lookup, declension/conjugation derivation, deck coverage checker).

**Last updated:** 2026-08-20

---

## 1. Student profile

*Kept current as Jacob provides updates. Additions are dated; superseded facts are
struck through rather than deleted, so the trajectory stays visible.*

### Background

- Learning Finnish for **about 18 months** (as of 2026-08).
- Completed **Suomen Mestari 1 and 2**; ~~currently finishing chapter 1 of
  Suomen Mestari 3~~ → **as of 2026-08-20 the Anki data shows he is working
  through Suomen Mestari 3 chapter 2** (129 cards, 69% introduced, many with
  0–6 day intervals, i.e. started within the last week). Chapter 1 is fully
  introduced.
- **On the Suomen Mestari 2 gaps.** Anki has never shown him the cards for SM2
  chapters 3, 4 and 5 (456 cards) and only 16% of chapter 6. **This is a
  bookkeeping gap, not a knowledge gap** — Jacob confirmed (2026-08-20) that he
  worked through all of that vocabulary in class and in another app; those
  chapters were simply never folded back into Anki review. Treat SM2 K3–K6
  vocabulary as **probably known** (tier C-taught, §3.2), not as new.
- Working with a **Finnish teacher**, who has assessed him as **not yet B1**.

### Current grammar focus

- **Conditional mood (konditionaali).** This is the default grammar focus for
  lessons until Jacob says otherwise.

### Vocabulary

- **Anki collection**: 3,656 notes / 7,312 cards / 22,256 reviews, first review
  2025-02-13, most recent 2026-08-20.
- ~~Self-reported active recall: ~54%. It is a self-report, not a measurement —
  the txt export contains no per-card scheduling data, so an exact known/unknown
  split cannot be computed.~~ → **Superseded 2026-08-20.** The `.colpkg` carries
  the full scheduler state, so this is now measured, not estimated:

  | recognition card state (FI→EN, the direction reading uses) | notes | share |
  |---|---|---|
  | mature (interval ≥ 21 days) | 1,640 | 44.9% |
  | young (studied, interval < 21 days) | 503 | 13.8% |
  | **drilled in Anki (mature + young)** | **2,143** | **58.6%** |
  | never shown by Anki, but from a course deck he worked through elsewhere | 716 | 19.6% |
  | **likely known for reading (the working figure)** | **2,859** | **78.2%** |
  | never shown, genuine backlog (Harry Potter, Animals) | 797 | 21.8% |

  The 54% self-report tracks the *Anki-drilled* figure almost exactly, which is
  probably what he was reading off. The working figure for graded reading is
  **~78%**, because a fifth of the collection is vocabulary he has learned
  elsewhere that Anki has simply never scheduled. Median interval on the drilled
  words is 79 days (p90 258, max 569) — what he has drilled, he knows solidly.
- Production is measurably weaker than recognition, consistent with his own
  assessment: 1,803 production cards in review versus 2,109 recognition cards.
- **Shadow lexicon**: a body of words recognised passively from Finnish media but
  never entered into Anki. Real and non-trivial in size, but unmeasurable. Its
  practical effect is that vocabulary constraints can be loosened for common and
  strongly contextualised words — the 54% figure understates *reading* knowledge.

### Declared strengths

- **Case system analysis** — comfortable reasoning about what a case is doing.
- **Spoken-register reductions** — *mä/sä/se*, *oon/meen*, passive-for-1pl, etc.
- **Modal verbs.**

### Declared weak areas

- **Partitive plural**, across noun/word types.
- **Partitive genitive** — i.e. the partitive/genitive contrast and the genitive
  plural, across noun/word types.

Both are treated as standing lesson targets regardless of the nominal grammar
focus: every lesson should contain deliberate, spread-out instances rather than
whatever the topic happens to produce. See `finnish-skills.md` §6 and §7.

### Frontier areas (not the target of this project, but noted)

- **Production** (speaking and writing).
- **Unscripted listening.**

Graded reading is receptive work. It supports these indirectly — by building the
form-recognition that production draws on — but the lessons should not pretend to
be production practice. Where a lesson can cheaply add a production hook (one
short written answer, one sentence to say aloud), it is worth doing, but as a
bonus, not as the core.

### Leeches — words Anki says he keeps forgetting

23 recognition cards have 4+ lapses. These are free, high-value recycling
targets for lessons; using one in context is worth more than another repetition
of the card. Current list (regenerate with `python3 tools/anki.py <colpkg> --leeches`):

*me tullaan, kapea, kunnianhimoinen, Hauska tutustua!, Hauskaa viikonloppua!,
keskiviikkoisin, takuuvuokra, kirjoittaa ylioppilaaksi, vastuuntuntoinen, kauas,
arvata, havaita, nytkähtää, tuokio, te meette, ensimmäinen kerros, muki,
seuraavaksi, ansioluettelo, harjoittelija, kuulokkeet, kertakaikkiaan, vuorokausi*

### Study tools already in use

- **Anki** (spaced repetition) — the source of truth for tracked vocabulary.
- **A declension drill app.**
- **Clozemaster.**

Implication for lesson design: isolated form-drilling is already covered
elsewhere. This project's comparative advantage is **connected, contextualised
text** — meaning-driven exposure that the drill apps cannot provide. Lessons
should not duplicate Clozemaster.

---

## 2. Sources of truth

Three inputs, in priority order.

### 2.1 The Anki collection — `collection-YYYY-MM-DD@HH-MM-SS.colpkg` ★ primary

**This replaced `All Decks.txt` as the vocabulary source of truth on 2026-08-20.**

A `.colpkg` is a zip containing `collection.anki21b`, a zstd-compressed SQLite
database. `tools/anki.py` reads it directly (libzstd via ctypes, since no zstd
Python package is installable in this environment). It carries what the text
export does not: **per-card scheduler state** — interval, ease, reps, lapses,
queue — and the deck each note lives in.

Why this matters more than it sounds: the text export lists every note whether
or not it has ever been studied. **1,513 of the 3,656 notes have never been
seen.** Treating the txt file as a vocabulary list therefore counts more than a
third of the collection as known when it is not. That is exactly the error that
made lesson 01 too hard (§7).

What the collection contains:

| | |
|---|---|
| notes | 3,656 |
| cards | 7,312 — two per note, `ord=0` FI→EN (recognition), `ord=1` EN→FI (production) |
| reviews logged | 22,256, from 2025-02-13 to 2026-08-20 |
| note type | "Basic (and reversed card)" |

**Decks, and how much of each has actually been studied** (recognition cards):

| deck | notes | mature | young | never studied | known |
|---|---|---|---|---|---|
| Suomen Mestari 1 | 1,172 | 1,113 | 59 | 0 | **100%** |
| Suomen Mestari 2::K1 | 127 | 84 | 43 | 0 | **100%** |
| Suomen Mestari 2::K2 | 212 | 29 | 71 | 112 | 47% |
| Suomen Mestari 2::K3 | 175 | 0 | 0 | 175 | **0%** |
| Suomen Mestari 2::K4 | 167 | 0 | 0 | 167 | **0%** |
| Suomen Mestari 2::K5 | 114 | 0 | 0 | 114 | **0%** |
| Suomen Mestari 2::K6 | 128 | 16 | 4 | 108 | 16% |
| Suomen Mestari 2::K7 | 141 | 123 | 18 | 0 | **100%** |
| Suomen Mestari 2::K8 | 108 | 92 | 16 | 0 | **99%** |
| Suomen Mestari 3::K1 | 96 | 11 | 85 | 0 | **100%** |
| Suomen Mestari 3::K2 | 129 | 3 | 86 | 40 | 69% |
| My Words | 116 | 107 | 9 | 0 | **100%** |
| Ilman Sua | 29 | 0 | 29 | 0 | **100%** |
| Harry Potter::Ch1 | 625 | 40 | 50 | 535 | 14% |
| Animals | 316 | 21 | 33 | 262 | 17% |

Read that table before every lesson. The three deck groups behave differently:

- **Reliable** — SM1, SM2 K1/K7/K8, SM3 K1, My Words, Ilman Sua. Draw freely.
- **Partial** — SM2 K2/K6, SM3 K2. Check the individual word.
- **Mostly unstudied** — SM2 K3/K4/K5, Harry Potter Ch1, Animals. Treat a word
  from these as new unless the tool says otherwise. Harry Potter and Animals
  are the likely home of the "shadow lexicon", so words there may be recognised
  in context even though the card is untouched — but do not assume it.

**Handling rule.** Re-read the newest `.colpkg` in the folder fresh before
generating every lesson; never rely on a cached read. Ask Jacob to re-export
from Anki (*File → Export → Anki Collection Package*, media not required) when
the file on disk is more than a week or two old, since the whole value of this
source is that the scheduler state is current.

### 2.2 `All Decks.txt` — secondary

Still useful and still worth keeping: it is the human-readable view, and it
carries two things the database does not surface as conveniently.

- Spoken variants marked `(spoken)` — 151 entries.
- **Verb case government annotated inline**: `(+ P)`, `(+ S-MIHIN)`,
  `(+ S-MISTÄ)`, `(+ G)`, `(+ MIHIN)`, `(+ -maan/-mään)` and similar, across
  100+ entries. **Honour these exactly** when using such a verb — it is free
  reinforcement of something already studied.

Format: tab-separated, LF, no BOM, UTF-8, header lines `#separator:tab` /
`#html:false`, Finnish front / English back, four fields of which the last two
are always empty. Do **not** use it to judge whether a word is known.

### 2.3 `Jacob 2026` (Google Doc) — lesson notes from his teacher

A running document of notes from every lesson over the past ~18 months, kept in
dated entries.

**Direct link:**
<https://docs.google.com/document/d/1vwJ3WPHcsods-EtYYRLeBGxiHY3j-NyERzOPfCPlUM8/edit>
(file ID `1vwJ3WPHcsods-EtYYRLeBGxiHY3j-NyERzOPfCPlUM8`)

**Directions — run this before every lesson:**

1. Read the document (`mcp__Google_Drive__read_file_content` with the file ID
   above; fall back to `download_file_content` with `exportMimeType: text/plain`).
2. Find the **dated entries**, sort them, and take the **most recent three**.
   Recency is what matters: a topic from last week outranks the same topic from
   nine months ago.
3. From those entries, extract:
   - **grammar the teacher has just introduced or drilled** → this becomes the
     lesson's grammar focus, taking priority over the standing default in §1;
   - **errors or corrections she flagged** → these become deliberate contrast
     points in the text, and comprehension-question targets;
   - **topics or vocabulary domains covered** → candidate lesson themes, since
     re-meeting that vocabulary in connected prose is the highest-value thing
     this project can do;
   - **anything she says he struggles with** → add to the weak-area list in §1
     with a date, and treat as a standing target the way partitive plural and
     genitive plural already are.
4. If the newest entry is older than about a month, say so in the lesson notes
   and fall back to the §1 default focus rather than drilling something stale.
5. Log in §7 which dated entries a lesson drew on, so the same material is not
   worked twice in a row.

Where the teacher's notes and the Anki data disagree about readiness, **the
teacher wins on grammar** (she has assessed him in person) and **Anki wins on
vocabulary** (it has the review history).

> **Access status (2026-08-20): NOT YET READ.** The Google Drive connector in
> this session cannot see the document. `search_files` and `list_recent_files`
> return nothing for any query, and fetching the file ID directly returns
> "Requested entity was not found" — which, given the ID is valid, means the
> connector is authenticated as a different Google account than the one the doc
> is shared with. The directions above are written to be robust to whatever
> structure the document turns out to have; **revise them once it can actually
> be read**, and record in the changelog what its real structure is.

---

## 3. Vocabulary knowledge: measured, not estimated

### 3.1 What changed

The original method (a four-tier scheme resting on a 54% self-report as a prior)
is superseded. With the collection, per-word knowledge is a lookup, not a guess.
The tiers survive; what changed is that tier membership is now **evidence**.

### 3.2 The tiers

Keyed on the **recognition** card (`ord=0`, FI→EN) — the direction reading uses.
Production state is tracked separately and does not affect these tiers.

| tier | definition | treatment in a lesson |
|---|---|---|
| **A** | recognition card **mature**: interval ≥ 21 days | known. Do not gloss. Use freely. |
| **B** | recognition card **young**: studied, interval < 21 days | probably known, still consolidating. Use, and gloss only if the sentence turns on it. Good recycling material — a lesson appearance reinforces a card that is still fragile. |
| **C-taught** | never shown by Anki, but the note lives in a **course deck** (Suomen Mestari, My Words, Ilman Sua) | **probably known.** Jacob covered this material in class or another app; the Anki card just was never scheduled. Counts as known in the working coverage figure. Gloss only if the sentence turns on it. |
| **C-backlog** | never shown by Anki, and the note lives in a **backlog deck** (Harry Potter, Animals) | **treat as unknown.** These are words carded from media but never actually drilled — the likeliest home of the shadow lexicon, so he may well recognise them in context, but do not rely on it. |
| **D** | not in the collection at all | genuinely new. Gloss, and recycle 3–5× per §4.4. |
| **L** | ≥ 4 lapses (overlay on A or B) | he keeps forgetting it. Deliberately work it into the text. |

The taught/backlog split is a **deck policy**, encoded in `DECK_POLICY` at the
top of `tools/anki.py`. It is Jacob-specific and he is the authority on it — ask
before classifying a new deck, and default new decks to `backlog`.

Function words (pronouns, the negative verb, *olla*, high-frequency particles)
are treated as tier A regardless of card state — they are grammatical
infrastructure, mostly absent from the collection as headwords. The list is
`tools/function_words.py`, deliberately restricted to closed classes.

### 3.3 The mechanical check

```
COLPKG=".../collection-YYYY-MM-DD@HH-MM-SS.colpkg" python3 tools/coverage.py draft.txt
```

reports the token split across A/B/C/D, the **A+B coverage percentage**, and the
C and D word lists for triage, plus sentence-length statistics.

It reports **two** figures:

- **strict = A+B** — what Anki alone can vouch for;
- **working = A+B+C-taught** — the honest estimate. **Steer by this one.**
  Target **95–98%** (§4.1).

The gap between them is Anki bookkeeping, not knowledge.

Read the three unknown lists differently:

- **C-backlog** is the list to be ruthless about — never drilled, and not
  covered in class either.
- **D** still over-reports. The index does not model superlatives, ordinals,
  some derived adverbs, or every verb form, and a few SM1-level words
  (*ihminen*, *ilta*, *työ*) exist in the collection only inside phrase cards.
  Triage by hand: intentional new words stay, everything else is a signal the
  index is missing a form. **Because of this, the working figure is itself an
  underestimate** — do not panic at a number in the 80s until the D list has
  been triaged.
- **C-taught** is mostly reassurance, but scan it: if a lesson is leaning hard on
  one unscheduled chapter, that is worth telling Jacob so he can unsuspend it.

### 3.4 The shadow lexicon, revisited

Still real, and now precisely located: it is the **C-backlog** tier — the Harry
Potter (14% drilled) and Animals (17%) decks, words met in media and carded but
never drilled. That is 797 notes, 21.8% of the collection. The tooling counts
them as unknown, which is the safe assumption; if Jacob reports that lessons
containing them feel easy, the policy for those decks can be revisited.

### 3.5 Recording what is actually known

Anki now answers "does he know this word". It cannot answer "did the gloss help",
"was the sentence too long", or "did he actually understand the joke". So the
post-lesson question in §6 still matters — it is just narrower now: ask about
**comprehension and difficulty**, not about vocabulary.

---

## 4. Graded-reading lesson design methodology

*Output of the research described in §4.1–4.7. Sources at the end of this file.*

### 4.1 The comprehension/acquisition trade-off

The two findings that anchor everything else:

- **Laufer (1989)**: ~95% lexical coverage is the threshold for *adequate*
  comprehension; below it, comprehension falls away sharply.
- **Hu & Nation (2000)**: ~98% coverage is needed for *unassisted* comprehension
  — roughly 1 unknown word in 50. Kremmel et al. (2023) replicated this.
- **Liu & Nation (1985)**: guessing an unknown word from context is unreliable
  unless ~95% of the surrounding words are already known.

The implication is a genuine tension. At 98% the text is comfortable but teaches
few new words; at 90% the student is decoding, not reading, and guessing fails.
**Nation's own resolution — two-thirds of reading time at ~98% coverage, one-third
at a lower level for fluency — is the model this project follows**, but inverted
in emphasis, because a once-per-request lesson is not an extensive-reading
programme. See §4.4.

### 4.2 On i+1

Krashen's *i+1* is the right intuition and a poor specification: it has never
been operationalised in a way that lets you build a text, and the critiques
(that *i* is unmeasurable, that comprehensible input alone is insufficient
without output and attention) are fair. This project treats i+1 as a **direction**
and uses lexical coverage plus a single grammatical target as the **measurable
proxy**. Where the two conflict, the measurable proxy wins.

### 4.3 Repetition and recycling

- Estimates of the encounters needed for incidental acquisition range from
  **6 to 20+**; ~**12** is the common planning figure (Nation), and Webb (2008)
  found that *clarity of context* mattered more for meaning than raw count.
- A single lesson cannot deliver 12 encounters. What it can do is deliver
  **3–5 encounters of each new word within the lesson**, in varied inflected
  forms, and then **recycle those words in the next two or three lessons**.
- **Narrow reading** — consecutive lessons on a related topic — is the cheapest
  way to get recycling for free, and is explicitly supported by the research.
  Worth proposing whenever Jacob doesn't specify a theme.

### 4.4 Vocabulary control for this project

Given the 54% baseline, the shadow lexicon, and the fact that this is a
single-lesson-per-request format with glossing available:

| | target |
|---|---|
| **A+B coverage** (the number that governs difficulty) | **95–98% of running tokens** |
| unknown tokens (C + D combined) | **2–5%**, i.e. roughly 1 in 20–50 |
| for a ~150-word lesson | **4–7 unknown tokens' worth**, ≈ 4–6 distinct new words |
| for a ~300-word lesson | **8–14 unknown tokens' worth**, ≈ 8–12 distinct new words |
| encounters of each new word within the lesson | **3–5**, in at least two different inflected forms |
| words carried over from the previous lesson | **3–5**, unglossed |
| tier-B and leech words worked in deliberately | **3–5**, unglossed — free reinforcement |

**C and D both count against coverage.** This is the change the collection
forced: a word sitting unstudied in the Anki deck is not a cheap word. Before
2026-08-20 the budget was reckoned against the text export, which made C-tier
words invisible and let lesson 01 ship at roughly 20 points under target.

Glossing is what makes the higher end of that range safe: with a gloss present
the text behaves like 98%-coverage text for comprehension while behaving like
94–96% text for learning. That is the deliberate design choice here.

### 4.5 Sentence and structural control

Drawn from Waring's practical guidance for graded-reader authors and from the
Selkokeskus *Easy Finnish Indicator 2.0*, adapted upward because Jacob is an
approaching-B1 L2 reader, not the cognitively-impaired L1 audience selkokieli
primarily targets.

| dial | easier | harder |
|---|---|---|
| mean sentence length | 6–9 words | 12–16 words |
| max sentence length | 12 | 22 |
| clauses per sentence | 1 | 2–3, with *joka*/*että*/*kun* |
| word order | plain SVO | fronted adverbials, existential order |
| non-finite constructions | none | one per lesson, glossed |
| participles as modifiers | none | present, agreeing |
| tense | present + imperfect | + perfect, pluperfect |
| register | standard written | marked spoken forms in dialogue |
| reference | repeat the noun | pronouns and anaphora across sentences |

Waring's points that carry over directly: control the ratio of new to old
*ideas*, not just words; watch anaphora, because pronoun chains overload
low-level readers; don't contort the message to dodge the right word — gloss it
instead; and don't let the plot become predictable just because the language is
controlled.

**The selkokieli divergence, stated deliberately.** The Easy Finnish Indicator
recommends avoiding the conditional, the passive, participial structures and
non-finite clauses. Three of those four are things Jacob either is studying now
or needs next. This project therefore **uses selkokieli's dials but not its
targets**: short sentences, concrete vocabulary, one idea per sentence, direct
word order — combined with deliberately included conditional, passive and
(sparingly) participial forms. That is a considered departure, not an oversight.

### 4.6 What separates a graded text from an authentic one

Worth naming because it is the main risk of this format. Simplified texts tend to
be lexically thinner, syntactically flatter, and — most damagingly — **less
cohesive**, because the connectives and anaphora that hold real prose together get
stripped out along with the hard words. The result reads as a sequence of
sentences rather than a text, and it teaches nothing about how Finnish is
actually built.

Countermeasures used here:

- Keep **connectives** (*mutta, koska, vaikka, kun, siksi, kuitenkin, silti*)
  even when they are not the teaching point. They are cheap and load-bearing.
- Keep **anaphora**: pronouns, *se*, demonstratives, ellipsis.
- Prefer **elaboration over deletion**: instead of removing a hard idea, restate
  it — add an appositive, a relative clause, a paraphrase. Elaborated text is
  longer but stays natural and gives the reader redundancy to work with.
- Let the text have **a point** — a small narrative arc, an opinion, a surprise.
  A description of a room teaches less than the same vocabulary in a story.

### 4.7 Glossing conventions

The research on glossing is broadly favourable — glosses improve both
comprehension and incidental vocabulary retention versus no gloss — with the
caveats that they interrupt flow, and that the gain is largest when the learner
has to do *some* work.

Conventions for this project:

- **Position**: a numbered list *after* the text, not inline and not as
  footnotes. Inline glossing destroys the reading experience; a post-text list
  preserves the first pass and supports a second.
- **Language**: **L1 (English)** for tier-D words. L1 glosses beat L2
  definitions for retention at this level, and Finnish-language definitions would
  themselves need glossing.
- **Content**: the **dictionary form** first, then the **form as it appears in
  the text**, then the meaning, then the Kotus type where the inflection is the
  point. E.g. `hovimestari (hovimestarin, type 6) — head waiter`.
- **Grammar glosses**: a separate short list, for forms rather than words —
  e.g. *"olisimme voineet* — conditional perfect, 1pl: 'we would have been
  able to'". This is where the current grammar focus gets made explicit.
- **Do not gloss** tier A or most of tier B. Over-glossing trains lookup
  dependence and destroys the guessing practice the text exists to provide.

### 4.8 Comprehension checks

Design principles taken from the L2 reading-comprehension literature: questions
should span levels rather than all being literal; retrieval practice (answering
from memory) beats re-reading; and questions written *in the target language*
double as extra input, provided they don't become the hard part.

Standard set per lesson, ~6 items:

1. **2 literal** — answerable by locating a sentence. In Finnish, answerable in
   Finnish, short.
2. **1–2 inferential** — require combining two places in the text or reading an
   implication. In Finnish.
3. **1 form-focused** — targets the grammar focus directly. *"Find the three
   conditional verbs and give the dictionary form of each."* This is where the
   partitive-plural and genitive-plural targets get checked even when the nominal
   focus is something else.
4. **1 productive hook** — one or two sentences of Jacob's own, using the target
   structure. Optional, marked as such, since production is a frontier area
   rather than this project's job.

Answers supplied in a clearly separated block at the end, so self-testing is
possible before checking.

### 4.9 On morphologically rich languages specifically

Little research exists on graded readers for agglutinative languages
specifically, so this section is reasoned from the morphology rather than cited.

Finnish breaks the usual apparatus in a specific way: **the word-family and
headword counts that anglophone graded-reader levelling is built on do not
transfer.** One Finnish nominal headword covers ~24 productive case-number forms
before possessive suffixes and clitics; one verb covers well over a hundred.
Knowing *hame* does not mean recognising *hameissamme*. So:

- **Count lemmas for vocabulary load, and inflectional forms for grammatical
  load, separately.** A text can be lexically easy and morphologically brutal.
  Both budgets need setting.
- **Treat an unfamiliar *form* of a familiar lemma as a partial unknown.**
  It costs the reader something, but it also teaches — this is exactly the
  productive difficulty a graded reader for Finnish should be trading in.
- **Vary the inflection of recycled words deliberately.** If *hovimestari*
  appears three times, it should appear in three different cases. This is the
  single biggest advantage this format has over Clozemaster, which drills forms
  in isolation.
- **Gradation and stem changes are the real difficulty gradient**, not word
  length. *tietokone* is long and easy; *käsi* is short and hard.
- **Compounds are decodable and should be exploited**, not avoided: a glossed
  decomposition (*työ + ttömyys + korvaus*) teaches three things at once.

---

## 5. Lesson format

Every lesson is delivered as a single Markdown file, `lesson-NN.md`, with this
structure:

```
# Lesson NN — <title>

**Grammar focus:** …
**Target length:** ~N words   **Actual:** N words
**New words (tier D):** N   **Recycled from lesson NN-1:** …

---
## Teksti
<the Finnish text>

---
## Sanasto            (tier-D words: dictionary form, form in text, meaning, type)
## Kielioppi          (grammar glosses: the target forms, explained)
## Kysymykset         (6 comprehension questions, in Finnish)
## Tuotanto           (optional production hook)

---
## Vastaukset         (answers, separated)
## Muistiinpanot      (what was deliberately included and why — for Jacob and for the log)
```

The **Muistiinpanot** block is what makes the series coherent: it records which
partitive-plural types and which genitive-plural endings the text deliberately
contained, so the next lesson can cover different ones.

---

## 6. Working routine

### Before every lesson

1. **List the folder** and pick the **newest `.colpkg`**. Load it fresh:
   `python3 tools/anki.py <colpkg>`. Never use a cached read. If the file is
   more than a week or two old, ask Jacob to re-export before continuing.
2. **Read the `Jacob 2026` Google Doc** and pull the grammar focus, flagged
   errors and recent topics from its three most recent dated entries (§2.3).
   That focus **outranks** the standing default in §1.
3. Re-read **`All Decks.txt`** for the `(spoken)` tags and the inline verb
   rection annotations (§2.2) — but not for judging what is known.
4. Re-read **`manifest.md`** (this file) — profile, deck table in §2.1, §7 log.
5. Consult **`finnish-skills.md`** for the grammar being targeted.

### While drafting

6. Draft the Finnish text to the §4.4 and §4.5 targets.
7. Run **every inflected form of interest** through `tools/decline.py`,
   `tools/conjugate.py` or `kotus_lookup.py`. Do not rely on recall.
8. Run `COLPKG=... python3 tools/coverage.py <draft>`. **Iterate until A+B
   coverage is 95–98%**, treating the C list as the priority: every C token is
   a word he has never actually studied.
9. Run the §22 failure-mode checklist in `finnish-skills.md` over the text.
10. Flag any form that remains genuinely uncertain, in the lesson itself.

### After every lesson

11. **Ask Jacob** about comprehension and difficulty — no longer about which
    words he knew, since Anki answers that now (§3.5). Ask whether the teacher
    has flagged anything new.
12. Update §7 and the changelog. Do not rewrite history.

---

## 7. Lesson log

*Append one row per lesson. Difficulty feedback and observed errors feed §3.4 and
the next lesson's vocabulary carry-over.*

| # | date | theme | grammar focus | length | new words | Jacob's difficulty feedback | errors / notes to reinforce |
|---|---|---|---|---|---|---|---|
| 01 | 2026-08-20 | *Loppuunmyyty* — a sold-out premiere, and the old film they saw instead | conditional (present, perfect, passive, polite) + standing partitive/genitive plural | 334 words, 34 sentences, mean 9.8 | 10 tier-D; working coverage 79.6% (see correction) | *awaiting* | *awaiting* |

> **Correction to lesson 01, made when the `.colpkg` arrived (2026-08-20),
> then revised the same day.**
>
> *First finding:* the lesson was graded against `All Decks.txt`, which lists
> every note whether or not it has been studied. Re-checked against the
> collection, 30 of the 96 lemmas the lesson treated as known had never been
> shown by Anki — including most of the theme vocabulary (*ensi-ilta, esitys,
> irtisanoa, lama, lipunmyynti, menettää, näytellä, pääosa, työttömyyskorvaus,
> kuukausikaupalla*, all Suomen Mestari 3 **chapter 2**, not chapter 1).
> Measured coverage came out at 71.9%, against a 95–98% target.
>
> *Revision, after Jacob clarified:* most of that is an Anki bookkeeping gap,
> not a knowledge gap — he studied the Suomen Mestari material in class and in
> another app, and those chapters were never folded back into review. With the
> taught/backlog deck policy applied (§3.2), the numbers are:
>
> | | tokens | share |
> |---|---|---|
> | A + B (Anki-drilled) | 240 | 71.9% |
> | C-taught (Anki gap, probably known) | 26 | 7.8% |
> | **working coverage (A+B+C-taught)** | **266** | **79.6%** |
> | C-backlog (genuinely undrilled) | 7 | 2.1% |
> | D (not in collection) | 61 | 18.3% |
>
> And the C-backlog list is only *ajattelin, joutui, kysyi, osannut, useita,
> usko, ymmärsin* — high-frequency verbs that happen to be carded in the Harry
> Potter deck and are near-certainly known. The D figure is inflated by the
> index limitations described in §3.3 (superlatives, ordinals, unmodelled verb
> forms, SM1 words that exist only inside phrase cards) on top of the 10
> intentional new words.
>
> **Honest verdict: lesson 01 was somewhat harder than designed, but not
> dramatically so.** The headline 71.9% was largely a tooling artifact. The real
> error was one of method rather than outcome — sourcing the theme from the tail
> of the text export on the assumption that file position tracks recency. It
> does not: the export is a merge of decks in mixed order, and that tail is SM3
> chapter 2. §8 defaults amended to forbid the heuristic.
>
> The Finnish itself is unaffected — every form was derived and verified, and
> re-verification found no errors. It was the difficulty grading that was
> shaky, not the language. Jacob's read on how it actually felt is still the
> most useful evidence available.

**Lesson 01 — what was covered, so lesson 02 can go elsewhere**

- Partitive plural types used: 1, 2, 10, 12, 38, 39, 48, plus one gradating word
  (*lippu* → *lippuja*, strong grade retained before *-ja*).
  **Not yet used:** the *-ejä* group (type 5: *rivejä, filmejä*), type 9 *-oja*
  (*kaloja*), and the three-syllable *-oita* group (*tarinoita*). Target next.
- Genitive plural: all four endings (*-jen, -ien, -iden, -ten*) appeared.
- Conditional: 14 present, 8 perfect, 1 passive, 1 polite *-ko*; 4 *jos*-sentences
  with the conditional in both halves. Strong-grade point carried by *ehdottaa*
  and *suositella*.
- Deliberately **not** used, available as future difficulty: participial
  modifiers, temporal and referative constructions, potential mood, spoken
  register. Text is entirely standard written Finnish.
- Tier-D words introduced: *ehdottaa, pettyä/pettymys, sattuma, kohtaus,
  mielipide, suositella* (recycled) and *ilme, rivi, pelastaa, toimia* (single).
  These are the carry-over candidates for lesson 02 (§4.4: 3–5 unglossed).

---

## 8. Lesson request template

```
Lesson Request
- Lesson #:
- Grammar focus: [blank = default to manifest's current focus]
- Theme/topic: [optional]
- Target length: [e.g. ~150 words, ~300 words]
- New vocabulary to seed in: [optional]
- Notes on last lesson: [too hard / too easy / anything specific]
```

Defaults when a field is left blank:

- **Grammar focus** → whatever the three most recent dated entries in the
  `Jacob 2026` doc point to (§2.3). Only if that is unavailable or stale, fall
  back to the current focus in §1 (presently: conditional mood). Either way,
  always alongside the standing partitive-plural / genitive-plural targets.
- **Theme** → continue the previous lesson's topic area if there is one
  (narrow reading, §4.3); otherwise pick something concrete and everyday.
- **Length** → ~200 words.
- **New vocabulary** → tier-C words from the deck he is currently working
  (SM3 K2), which Anki will introduce soon anyway, plus tier-D words the theme
  requires, plus 3–5 tier-B and leech words for free reinforcement. Never draw
  from "the tail of `All Decks.txt`" — file position is not recency, and that
  mistake is what made lesson 01 too hard.

---

## 9. Sources

**Comprehensible input, coverage and extensive reading**

- Laufer, B. (1989), on the ~95% coverage threshold for adequate comprehension.
- Hu, M. & Nation, P. (2000), *Unknown vocabulary density and reading
  comprehension* — the ~98% figure for unassisted comprehension.
- Kremmel, B. et al. (2023), *Unknown Vocabulary Density and Reading
  Comprehension: Replicating Hu and Nation (2000)*, **Language Learning** —
  <https://onlinelibrary.wiley.com/doi/10.1111/lang.12622>
- Liu, N. & Nation, P. (1985), on guessing from context requiring ~95% coverage.
- Nation, P., *Principles guiding vocabulary learning through extensive reading*,
  Reading in a Foreign Language — <https://files.eric.ed.gov/fulltext/EJ1059712.pdf>
  (the ~12-encounters planning figure; the two-thirds/one-third split).
- Conti, G. (2025), *Why the input we give our learners must be 95–98%
  comprehensible* — <https://gianfrancoconti.com/2025/02/27/why-the-input-we-give-our-learners-must-be-95-98-comprehensible-in-order-to-enhance-language-acquisition-the-theory-and-the-research-evidence/>

**Repetition and incidental acquisition**

- Uchihara, Webb & Yanagisawa (2019), on the 6–20+ encounter range.
- Webb, S. (2008), on context clarity outweighing repetition count for meaning.
- EAP Foundation, *Incidental vocabulary learning* —
  <https://www.eapfoundation.com/vocab/learn/incidental/>

**Writing graded readers**

- Waring, R., *Writing Graded Readers*, Extensive Reading Central —
  <https://www.er-central.com/authors/writing-a-graded-reader/writing-graded-readers-rob-waring/>
- Claridge, G. (2005), *Simplification in graded readers: Measuring the
  authenticity of graded texts*, Reading in a Foreign Language (on how simplified
  texts diverge from authentic ones).

**Glossing**

- *How do different forms of glossing contribute to L2 vocabulary learning from
  reading?*, Studies in Second Language Acquisition —
  <https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/abs/how-do-different-forms-of-glossing-contribute-to-l2-vocabulary-learning-from-reading/38124150D59DF3039EE1FF5AE88FE922>
- *The effects of glosses on English L2 incidental vocabulary learning through
  reading: a meta-analysis*, Frontiers in Language Sciences —
  <https://www.frontiersin.org/journals/language-sciences/articles/10.3389/flang.2026.1815571/full>

**Comprehension questions**

- Liu, Y. (2021), *Does questioning strategy facilitate L2 reading
  comprehension?*, Journal of Research in Reading —
  <https://onlinelibrary.wiley.com/doi/10.1111/1467-9817.12339>

**Critiques of i+1**

- *Beyond comprehensible input: a neuro-ecological critique of Krashen's
  hypothesis in language education*, Frontiers in Psychology (2025) —
  <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1636777/full>

**Finnish-specific graded/plain language**

- Selkokeskus, *The Easy Finnish Indicator 2.0* —
  <https://selkokeskus.fi/in-english/easy-finnish/the-easy-finnish-indicator-2-0/>
  (96 criteria across text, words, structures and layout; the explicit list of
  structures to avoid, including the conditional — see §4.5 for why this project
  departs from it).
- Selkokeskus, *Writing in Easy Finnish* —
  <https://selkokeskus.fi/in-english/easy-finnish/writing-in-easy-finnish/>

**Anki internals**

- Collection package format: zip containing `collection.anki21b`, a
  zstd-compressed SQLite database. Card state semantics (`type` 0=new, 1=learning,
  2=review, 3=relearning; `queue` −1=suspended; `ivl` in days; `factor` ×1000;
  `reps`, `lapses`) and the 21-day maturity convention are Anki's own, as used by
  its built-in card-counts graph.

Grammar sources are cited in `finnish-skills.md`.

---

## 10. Changelog

*Append-only. New entries at the bottom.*

### 2026-08-20 — project set up

- Created `manifest.md` and `finnish-skills.md`.
- Recorded the initial student profile as given (§1): ~18 months of study,
  Suomen Mestari 1–2 complete and 3 ch.1 in progress, conditional mood as the
  current focus, ~54% self-reported deck recall, shadow lexicon acknowledged,
  weak areas partitive plural and partitive/genitive, strengths case analysis /
  spoken reductions / modal verbs, frontier areas production and unscripted
  listening, assessed by his teacher as not yet B1.
- Analysed `All Decks.txt` (3,656 entries). **Confirmed the export carries no
  per-card performance data** — the two trailing columns are empty for every
  row — so the 54% self-report stands as the working baseline and no exact
  known/unknown split is computable. Recorded the deck's composition in §2.
- Built the vocabulary-estimation method in §3: a four-tier scheme (in-deck core /
  in-deck ordinary / transparent-but-absent / genuinely new) with tier D as the
  difficulty lever, plus a mechanical coverage floor from an ~85,000-form
  inflected index generated from the deck.
- Researched graded-reader design and wrote the methodology in §4: coverage
  thresholds, the comprehension/acquisition trade-off, repetition and recycling
  targets, sentence and structure dials, the graded-vs-authentic problem,
  glossing conventions, comprehension-check design, and a section on what
  changes for a morphologically rich language.
- Noted and resolved the **selkokieli tension**: Finnish plain-language
  guidelines recommend avoiding the conditional, passive and participial
  structures, which are precisely this student's current and next targets. This
  project adopts selkokieli's *dials* but not its *targets* (§4.5).
- Built and validated `tools/` against the Kotus *Nykysuomen sanalista* (94,110
  headwords with inflection type and gradation class): lookup, declension and
  conjugation derivation, and a deck coverage checker. Validation: 51/51 nominal
  and 25/27 verb model paradigms regenerated, 113/113 hand-verified nominal
  forms, 32/32 full-paradigm case forms, 67/68 verb forms, 99.3% of deck
  nominals and 96.3% of deck verbs resolved. Known limits declared in
  `finnish-skills.md` §1.4.
- Verification pass: cross-checked every "lemma : form" claim in the prose of
  `finnish-skills.md` against the generator. This surfaced one real error class —
  Kotus type 41 *-is* words were being given an *a*-stem by analogy with the
  model *vieras* (*kaunian* for *kauniin*); six deck words affected. Fixed and
  re-validated. Also established, against sources, that *meri* has genuinely
  **mixed** vowel harmony (*merta* but *meriä*); it is now stored as a checked
  irregular rather than derived.
- Established the finding that the **conditional is built on the strong grade**
  (*pitäisi*, not *pidäisi*) — verified against Kotus paradigms for all 27 verb
  types and independently confirmed against Uusi kielemme. Flagged as the
  highest-risk form class while the conditional is the focus.
- No lessons created yet, per instruction.

### 2026-08-20 — lesson 01 delivered

- Re-read `All Decks.txt` fresh before drafting; unchanged since setup
  (3,656 entries, same mtime and byte count).
- Lesson 01 *Loppuunmyyty*: 334 words, conditional focus, theme drawn from the
  Suomen Mestari 3 chapter 1 tail (theatre/film/criticism, plus the
  recession/unemployment strand). 15 SM3 ch.1 words recycled. All fields in the
  request were blank, so manifest defaults applied: conditional focus, standing
  partitive/genitive-plural targets, theme from the deck tail.
- Verification: ~180 inflected forms derived from their Kotus types and checked —
  54 nominal and 60 verb forms in the text, 66 more in the glossary, grammar
  tables and answer key. **0 mismatches.** Two checker flags investigated and
  both resolved in the text's favour: *esitettäisiin* (the checker's harmony
  heuristic was wrong) and *seisoi* (*seisoa* type 52, not *seistä* type 66).
- **Tool bug found and fixed during drafting:** class-D gradation (k : –) after an
  i-diphthong was deriving *aian* for *aika*; the correct genitive is *ajan*
  (likewise *poika : pojan*), while *reikä : reiän* and *lika : lian* take no *j*.
  No consulted source (VISK, Korpela, Uusi kielemme) states the conditioning
  rule, so per the §1.5 uncertainty rule the tool now **stores** *aika* and
  *poika* as verified irregulars (checked against cooljugator) and **flags**
  every other class-D-after-i-diphthong word for manual checking rather than
  guessing. The lesson itself was unaffected — it uses only the essive *aikana*,
  which is strong-grade either way.
- Vocabulary budget: the first draft ran to 17 tier-D words, over the §4.4 budget
  of 8–12 for this length. Reduced to 10 by substituting deck words where the
  substitution did not damage the sentence (*kehua* → *ihailla*, which also
  honours its deck-annotated `(+ P)` rection; *syntyä* → a second *sattuma*;
  *luukku* → *vuoro*; *varoitus* → *yllättäen*; *vaihdella* → *erilainen*;
  *jatkua* → *kestää*), following Waring's rule not to contort the message to
  dodge a word.
- Mechanical coverage: 74.6% against the deck index. Residue triaged and found to
  be pronouns, superlatives, ordinals, possessive-suffixed forms, 3rd-plural and
  passive verb forms, and SM1-level words that appear in the deck only inside
  phrases (*ilta*, *ihminen*, *työ*). Genuinely new content = the 10 tier-D words.
- **Awaiting Jacob's feedback** on difficulty, which words were already known,
  and any errors made, to fill the §7 row and calibrate lesson 02.

### 2026-08-20 — Anki collection replaces the text export; Google Doc directions added

- Jacob supplied `collection-2026-08-20@06-57-02.colpkg` and access to a Google
  Doc of his teacher's lesson notes.
- **The `.colpkg` is readable and is now the vocabulary source of truth (§2.1).**
  It is a zip holding a zstd-compressed SQLite database; no zstd Python package
  is installable in this environment, so `tools/zstd_ctypes.py` calls libzstd
  through ctypes. Built `tools/anki.py` (collection reader, tiering, deck
  breakdown, leech list) and `tools/coverage.py` (tier-aware coverage checker,
  replacing the old `deck.py`).
- **The headline finding: 1,513 of 3,656 notes have never been studied**, and
  they are concentrated, not spread — Suomen Mestari 2 chapters 3, 4 and 5 are
  at 0%, chapter 6 at 16%, Harry Potter Ch1 at 14%, Animals at 17%, while SM1,
  SM2 K1/K7/K8 and SM3 K1 are at ~100%. Full table in §2.1.
- Measured recognition knowledge: **58.6% known for reading** (44.9% mature,
  13.8% young), median interval 79 days. The 54% self-report was accurate; what
  it could not convey was *which* words, or that the gaps are clustered.
- **Profile corrected:** he is working through Suomen Mestari 3 **chapter 2**,
  not finishing chapter 1 — 129 cards, 69% introduced, many with 0–6 day
  intervals.
- §3 rewritten: the four tiers are unchanged in shape but are now keyed on
  actual card state (A mature / B young / C in-collection-but-unstudied /
  D absent), with a leech overlay. Added `tools/function_words.py` so closed-class
  grammar words are not counted as unknown vocabulary.
- §4.4 budget restated as an **A+B coverage target of 95–98%**, with C and D both
  counting against it.
- **Lesson 01 re-graded and a correction logged in §7:** it measured 71.9%
  coverage against a 95–98% target, because 30 lemmas it treated as known had
  never been studied. Cause identified: file position in the text export was
  used as a recency proxy, and the export is a merge of decks in mixed order.
  §8 defaults amended to forbid that heuristic.
- **Deck policy added after Jacob clarified the Suomen Mestari gaps.** He
  studied SM2 K3–K6 in class and in another app; those chapters were never
  folded back into Anki review. Tier C is therefore split by deck policy
  (`DECK_POLICY` in `tools/anki.py`): **C-taught** for course decks (Suomen
  Mestari, My Words, Ilman Sua) where an unscheduled card is a bookkeeping gap,
  **C-backlog** for media decks (Harry Potter, Animals) where it is a real gap.
  This moves the working knowledge figure from 58.6% to **78.2%**, and revises
  the lesson-01 verdict from "well below target" to "somewhat harder than
  designed" (§7). New decks default to `backlog`; ask Jacob before reclassifying.
- `coverage.py` now reports **strict (A+B)** and **working (A+B+C-taught)**
  coverage, and splits the unknown output into C-taught / C-backlog / D so the
  three can be triaged differently.
- **Google Doc (`Jacob 2026`) directions added as §2.3**: read the three most
  recent dated entries before every lesson and take the grammar focus, flagged
  errors, recent topics and struggle areas from them; the teacher's focus
  outranks the standing default in §1. **The document could not be read in this
  session** — the Drive connector returns nothing for every query and reports
  "Requested entity was not found" for the known-good file ID, indicating it is
  authenticated as a different Google account. The directions are written to be
  robust to the document's actual structure and are marked for revision once it
  can be read.
