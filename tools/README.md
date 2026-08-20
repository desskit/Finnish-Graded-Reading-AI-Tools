# tools/

Verification toolkit for the Finnish graded-reading project. Everything here
exists to keep inflected forms out of lessons unless they were *derived*, not
recalled. See `finnish-skills.md` §1 for the protocol these implement.

Python 3, no third-party dependencies.

## Files

| file | what it is |
|---|---|
| `kotus.tsv` | Kotus *Nykysuomen sanalista* v1 (2006), 94,110 headwords → inflection type + gradation class. LGPL. |
| `kotus_models.json` | The model paradigms Kotus publishes for each of the 78 types, transcribed verbatim. |
| `kotus_lookup.py` | word → type, gradation class, model paradigm. Falls back to the compound head. |
| `gradation.py` | Syllabification + consonant gradation, classes A–M, both directions. |
| `decline.py` | Nominal paradigms: four principal parts, and the full 12-case × 2-number table. |
| `conjugate.py` | Verb principal parts (incl. the conditional) for types 52–78. |
| `anki.py` | Reads a `.colpkg` directly: per-word tier (A mature / B young / C never studied / D absent), deck breakdown, leech list. **The vocabulary source of truth.** |
| `coverage.py` | Tier-aware coverage checker. Grades a draft against what Jacob actually knows, not against every note in the collection. Replaces the old `deck.py`. |
| `zstd_ctypes.py` | zstd decompression via libzstd + ctypes, because no zstd Python package is installable here. Needed to open `collection.anki21b`. |
| `function_words.py` | Closed-class Finnish words (pronouns, negative verb, *olla*, common particles) treated as known regardless of card state. |
| `validate.py` | The regression suite. Run it after any change. |

## Use

```bash
python3 kotus_lookup.py kaupunki tavata työttömyyskorvaus
python3 decline.py katto vesi kaunis
python3 conjugate.py pitää tavata nähdä
python3 -c "import sys; sys.path.insert(0,'.'); from decline import show_full; print(show_full('kaupunki'))"

python3 anki.py "/path/to/collection.colpkg"            # what he knows, by deck
python3 anki.py "/path/to/collection.colpkg" --leeches  # words he keeps forgetting
COLPKG="/path/to/collection.colpkg" python3 coverage.py draft_lesson.txt
python3 validate.py                      # regression
python3 gradation.py                     # gradation unit tests
```

## Reading the output

- A **refusal** ("CANNOT ALIGN", "NOT IN KOTUS LIST", "derive by hand") is the
  tool working correctly. Look the word up; do not talk it into an answer.
- A `!!` line is a flag: an inverse gradation the tool could not place, a stem
  with only *e*/*i* whose harmony is undetermined, a plurale tantum, or a stored
  irregular. All of these need a human decision.
- `coverage.py` reports four buckets. **A+B is the coverage figure; target
  95–98%.** Treat the two unknown lists differently: every **C** token is a word
  sitting unstudied in his own collection and is the failure mode the text export
  hid, so be ruthless about those. The **D** list still over-reports — the index
  does not model superlatives, ordinals, some derived adverbs, or every verb
  form — so triage it by hand.
- Re-export the `.colpkg` from Anki when it is more than a week or two old. The
  whole value of this source is that the scheduler state is current.

## Current test status

| suite | result |
|---|---|
| Kotus nominal models regenerated | 47/51 exact (17, 20, 41 omit a rare variant; 51 refuses by design) |
| Kotus verb models regenerated | 25/27 exact (55, 60 flag their suppletive pasts) |
| hand-verified nominal forms | 113/113 |
| hand-verified full-paradigm case forms | 32/32 |
| hand-verified verb forms | 67/68 |
| syllabification + gradation unit tests | 32/32 |
| deck nominals resolved | 99.3% |
| deck verbs resolved | 96.3% |
| collection opened, tiered and cross-checked | 3,656 notes / 7,312 cards / 22,256 reviews |

## Licence note

`kotus.tsv` and `kotus_models.json` derive from the Institute for the Languages
of Finland's *Nykysuomen sanalista*, © Kotimaisten kielten tutkimuskeskus 2006,
released under the GNU LGPL. Redistributed here under those terms.
