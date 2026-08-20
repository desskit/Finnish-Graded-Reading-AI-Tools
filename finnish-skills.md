# finnish-skills.md

Working grammar and pedagogy reference for the Finnish graded-reading project.
Not written for the student. Consulted before every lesson is drafted.

Companion file: `manifest.md` (student profile, grading method, lesson design).
Companion toolkit: `tools/` (Kotus lookup, declension and conjugation derivation,
deck coverage checker).

**Last updated:** 2026-08-20

---

## 0. Why this file exists

Finnish is morphologically dense in a way that punishes fluent guessing. A form
like *kaupungeissa* is four decisions deep (type → plural stem → gradation →
harmony), and every one of them can go wrong independently while the result still
*looks* like Finnish. A wrong form in a graded reader is worse than a missing one:
the student is reading for acquisition, so an error gets encoded as a fact.

The rule for this project is therefore:

> **No inflected form goes into a lesson because it feels right.**
> It goes in because it was derived from the word's Kotus inflection type, or
> because it was checked against a source, or it does not go in at all.

Section 1 is the protocol that enforces this. Everything after it is the grammar
the protocol assumes.

---

## 1. Verification protocol

### 1.1 The authority chain

1. **Kotus inflection data** (`tools/kotus.tsv`) — the Institute for the Languages
   of Finland's *Nykysuomen sanalista* v1, 94,110 headwords, each tagged with an
   inflection type number (1–51 nominal, 52–78 verb, 99 indeclinable) and, where
   it applies, a consonant-gradation class (A–M). This is the primary authority
   for *which paradigm a word follows*.
2. **Kotus model paradigms** (`tools/kotus_models.json`) — the eight principal
   parts Kotus publishes for each type, transcribed verbatim. Primary authority
   for *what that paradigm looks like*.
3. **VISK** (*Iso suomen kielioppi*, the reference grammar) — for rules, usage and
   anything the paradigms don't settle.
4. **Uusi kielemme / Korpela's Handbook** — for usage and pedagogical framing.
   Useful, secondary; not used to settle a form against Kotus.

### 1.2 The mechanical step

Before a word appears inflected in a lesson:

```
python3 tools/kotus_lookup.py <word>     # type + gradation class + model paradigm
python3 tools/decline.py <word>          # four principal parts, derived
python3 -c "...show_full('<word>')"      # all 12 productive cases, sg + pl
python3 tools/conjugate.py <verb>        # eight verb principal parts
```

`decline.py` and `conjugate.py` do not generate from pattern memory. They align
the target word to its Kotus model word, transfer the model's suffix material
(stored archiphonemically so vowel harmony can be re-applied), and then apply
consonant gradation *phonologically* — by syllabifying the built form and asking
whether the syllable the gradating consonant onsets is closed. Anything that
can't be aligned is reported as a refusal, never guessed.

### 1.3 What the tools have actually been tested on

| test | result |
|---|---|
| regenerate all 51 nominal Kotus model paradigms | 47/51 exact (17, 20 and 41 omit a rare parenthesised variant; 51 refuses by design) |
| regenerate all 27 verb Kotus model paradigms | 25/27 exact (55 and 60 flag their suppletive past variants *sousi*, *läksi* rather than deriving them) |
| hand-verified nominal forms | 113/113 |
| hand-verified full-paradigm case forms (sg + pl) | 32/32 |
| hand-verified verb forms | 67/68 |
| syllabification and gradation unit tests | 32/32 |
| whole deck: nominals resolved | 99.3% (18 refusals, all reported) |
| whole deck: verbs resolved | 96.3% |

The failures found during that testing are the reason the tests exist. Bugs the
suite caught, each of which would have put wrong Finnish in a lesson:

- no vowel harmony on transferred suffixes (*takkiä* for *takkia*);
- the illative treated as gradation-triggering (*katoon* for *kattoon*);
- non-initial `ie` parsed as a diphthong, closing a syllable that is actually
  open (*takien* for *takkien*);
- inverse-gradation types not strengthened (*rikaan* for *rikkaan*);
- an identical consonant cluster in the *ending* mistaken for the gradation site
  (*kattoitta* for *katoitta*);
- the weak genitive stem used for the essive (*vedenä* for *vetenä*);
- word-initial gradation (*dainnut* for *tainnut*);
- type 41 aligned literally to its model, so the lengthened stem vowel was taken
  from *vieras* instead of the word itself (*kaunian* for *kauniin*, *kallian*
  for *kalliin*, *valmian* for *valmiin*). Six words in the deck were affected.
  Found by cross-checking the prose of this file against the generator — which
  is the reason that cross-check is part of the routine.

### 1.4 Known limits — declare, don't paper over

- **Gradation class D (k : ∅) in an inverse type.** The weak grade is *nothing*,
  so there is no anchor for where the *k* goes: *pelätä : pelkään*, *aie :
  aikeen*. The tools mark these `(?)`. Look them up.
- **Stems with only *e* and *i*.** Vowel harmony is undetermined by the stem
  (*meri* takes *merta*, back, against the default). The tools flag these.
- **Kotus type 51** (*nuoripari*), where both halves of the compound inflect.
  Refused outright.
- **Words absent from the 2006 list** — recent loans, proper nouns, slang. About
  8% of the deck's single-token headwords. No type, no derivation, look it up.
- **Plurale tantum** (*häät*, *markkinat*, *polttarit*). Kotus gives the singular
  type; the tools rebuild the singular and flag that the plural is the real
  dictionary form.
- **Genuinely irregular lexemes** are stored, not derived. Currently only *meri*.
  Anything else that turns out to be irregular goes in the same table, with the
  source that settled it.
- The tools cover **case and principal parts**. Possessive suffixes, clitics,
  participle agreement and the non-finite constructions are *not* generated;
  they are built by hand from §12, §14, §17–19 below and checked.

### 1.5 Standing uncertainty rule

If a form is genuinely uncertain after all of the above, say so in the lesson
notes rather than presenting it confidently. An explicit "I'm not certain
*X* is the right partitive plural here" costs the student ten seconds. A
confidently wrong form costs a re-learned habit.

---

## 2. Phonology

### 2.1 Vowel harmony

Back **a o u** · front **ä ö y** · neutral **e i**.

A simple (non-compound) word contains back vowels or front vowels, not both;
neutral vowels are compatible with either. Every suffix containing A, O or U has
two shapes, chosen by the stem: *talossa* / *kylässä*, *taloksi* / *kyläksi*.

- Neutral-only stems take **front** endings by default: *tie → tietä*, *vesi →
  vettä*, *kieli → kieltä*. **Exceptions exist and are genuinely irregular.**
  *meri* has *mixed* harmony: back in the singular consonant-stem forms
  (*merta*) but front in the plural (*meriä*, *merissä*). No rule derives that,
  so *meri* is stored as a checked irregular in `decline.py`. Any other
  neutral-only stem gets flagged by the tools for manual checking rather than
  guessed.
- **Compounds harmonise on the last component**: *isoäiti → isoäitiä* (front,
  from *äiti*), *työpaikka → työpaikkaa* (back, from *paikka*). Scanning for the
  last non-neutral vowel gets this right; scanning for *any* back vowel does not.
- Some loanwords are disharmonic (*Olympia*, *amatööri*) and follow their final
  syllable.

### 2.2 Length

Vowel and consonant length are phonemic and carry meaning: *tuli* (fire) /
*tuuli* (wind) / *tulli* (customs); *tapan* (I kill) / *tapaan* (I meet). Doubling
is never decorative. Every long vowel and geminate in a lesson text must be
deliberate.

### 2.3 Syllabification

Needed because gradation depends on it.

- A single consonant between vowels begins the next syllable: *ka-tu*.
- In a cluster, all but the last consonant close the preceding syllable, and the
  last begins the next: *kat-to*, *laa-tik-ko*, *ajat-te-len*.
- Long vowels and diphthongs are one nucleus.
- **All eighteen diphthongs occur in the first syllable; only the *i*-final and
  *u/y*-final ones occur later.** So *ie*, *uo*, *yö* are heterosyllabic outside
  the first syllable: *tak-ki-en*, not *tak-kien*. This is what makes *takkien*
  strong-grade.
- A syllable is *closed* if it ends in a consonant.

### 2.4 Other

Stress is fixed on the first syllable, with secondary stress on odd-numbered
later syllables — this matters for rhythm when the text will be read aloud. Word-
initial consonant clusters occur only in loans (*strategia*), and colloquial
speech may still reduce them (*ruuvi* ← *skruvi*).

---

## 3. Consonant gradation (astevaihtelu)

The single richest source of quietly wrong Finnish.

### 3.1 The classes

Kotus labels each gradating word A–M. Direction depends on the word (§3.3).

| class | strong : weak | nominal example | verb example |
|---|---|---|---|
| A | kk : k | takki : takin | liikkua : liikun |
| B | pp : p | kaappi : kaapin | hyppiä : hypin |
| C | tt : t | tyttö : tytön | saattaa : saatan |
| D | k : – | reikä : reiän | hakea : haen |
| E | p : v | sopu : sovun | viipyä : viivyn |
| F | t : d | satu : sadun | pitää : pidän |
| G | nk : ng | aurinko : auringon | tunkea : tungen |
| H | mp : mm | kumpi : kumman | empiä : emmin |
| I | lt : ll | ilta : illan | yltää : yllän |
| J | nt : nn | hento : hennon | myöntää : myönnän |
| K | rt : rr | virta : virran | kertoa : kerron |
| L | k : j | arki : arjen | särkeä : särjen |
| M | k : v | suku : suvun | (rare) |

L applies where *k* stands after **h, l, r** and before *e*; M in *-uku-* and
*-yky-* sequences. Quantitative gradation (A–C) is still productive and applies
to new loans (*bloggaan : blogata*); the qualitative classes are not.

### 3.2 When the weak grade appears

**Phonologically: the weak grade appears when the syllable that the gradating
consonant begins is closed.** Everything else follows from this.

*katto* → *kat-to* (open, strong) · *ka-ton* (closed, weak) · *kat-to-a* (open,
strong) · *ka-tos-sa* (closed, weak) · *kat-to-na* (open, **strong** — the essive
is the one singular local-ish case that keeps the strong grade) · *ka-toik-si*
(closed, weak).

**The one systematic exception: the illative never triggers the weak grade**, in
either number. *kattoon*, *kattoihin*, *aurinkoon*, *kaupunkiin*, *iltaan*. The
*-h-* of the original *-hen* protected it. Getting this wrong produces *katoon*,
which is the single most common gradation error in generated Finnish.

Practical singular summary for a direct-gradation nominal:

| strong | weak |
|---|---|
| nominative sg, partitive sg, **illative sg**, essive sg | genitive sg, nominative pl, inessive, elative, adessive, ablative, allative, translative, abessive |

Plural forms are decided by the same syllable test on the plural stem:
*kattojen*, *kattoja*, *kattoihin*, *kattoina* strong; *katoissa*, *katoilla*,
*katoitta* weak.

For verbs the same test applies: *otan* (ot-tan, closed, weak) but *ottaa*,
*ottaisi*, *ottanut*, *otti*; *otettiin* weak.

### 3.3 Direct vs inverse

- **Direct** (*suora*): vowel-final nominatives and most infinitives are strong,
  and the weak grade appears in closed syllables. *katto : katon*, *ottaa : otan*.
- **Inverse** (*käänteinen*): the dictionary form is *weak* and the inflected stem
  is *strong*. Nominal types 32–37, 41, 43–49; verb types 72–75.
  *opas : oppaan*, *porras : portaan*, *kate : katteen*, *sivellin : siveltimen*,
  *tavata : tapaan*, *levätä : lepään*, *rohjeta : rohkenen*.
  For inverse nominals the weak grade survives in the forms built on the
  **consonant stem**: *vieras/vierasta*, *kytkin/kytkintä/kytkinten*.
  For the inverse verb types 72–75 the strong grade appears in exactly the
  present, past and **conditional**; the infinitive, potential, imperative,
  NUT-participle and passive stay weak: *tavata, tapaan, tapasi, tapaisi,
  tavannee, tavatkoon, tavannut, tavattiin*.
- **Gradation never touches a word-initial consonant.** *tainnut*, not *dainnut*.

### 3.4 Words that don't gradate

Many loans (*auto : auton*, *vaasi : vaasin*), acronyms, some names. Kotus simply
omits the class letter — which is why the lookup is worth doing rather than
assuming *-tt-* implies gradation.

---

## 4. Nominal stems and the Kotus type system

Finnish nominals inflect off up to three stems:

- **vowel stem** — genitive singular minus *-n*: *talo-*, *naise-*, *vede-*.
  Carries most singular cases.
- **consonant stem** — used by some types for the partitive, a *-ten* genitive
  plural and a few others: *vieras-*, *kytkin-*, *lapse-/las-*.
- **plural stem** — vowel stem plus *-i-*, with the vowel changes in §6.3:
  *taloi-*, *naisi-*, *vesi-*, *kaloi-*.

A word is *one-stem* if the vowel stem does everything (*talo*), *two-stem* if a
consonant stem is also needed (*vieras*, *nainen*, *pieni*).

The Kotus number encodes all of this. **Look it up; don't infer it from the
ending.** *paperi* is type 6 and *risti* is type 5, both ending in *-i*, and they
have different plural partitives (*papereita/papereja* vs *ristejä*). *kirjasto*
is type 2, not type 1, and therefore licenses both *kirjastoja* and *kirjastoita*.

Full type table with partitive and genitive plurals: **Appendix A**.

---

## 5. The case system

Fifteen cases. Twelve are fully productive; three (abessive, comitative,
instructive) are marginal in speech and largely confined to fixed expressions and
formal registers.

| case | ending | rough sense | *talo* | *kylä* |
|---|---|---|---|---|
| nominative | – | subject, total object | talo | kylä |
| genitive | -n | possession, total object, postpositions | talon | kylän |
| partitive | -A / -tA / -ttA | §6 | taloa | kylää |
| inessive | -ssA | in | talossa | kylässä |
| elative | -stA | out of, about | talosta | kylästä |
| illative | -Vn / -hVn / -seen | into | taloon | kylään |
| adessive | -llA | on, at, by, with; possessor | talolla | kylällä |
| ablative | -ltA | off, from | talolta | kylältä |
| allative | -lle | onto, to | talolle | kylälle |
| essive | -nA | as, in the capacity of; on (a day) | talona | kylänä |
| translative | -ksi | into (becoming), for | taloksi | kyläksi |
| abessive | -ttA | without | talotta | kylättä |
| comitative | -ine- + poss. | (together) with | taloineen | kylineen |
| instructive | -in | by means of (fixed) | (jaloin) | — |
| accusative | -t | only on personal pronouns | (minut) | — |

Notes that matter for writing lessons:

- The **internal** series (*-ssA -stA -Vn*) is used for enclosed spaces and, for
  most Finnish place names, for towns: *Helsingissä*. The **external** series
  (*-llA -ltA -lle*) is used for surfaces, for some place names (*Tampereella*),
  and for the possessive construction.
- **The illative is irregular by type** and is the case most worth checking:
  *-Vn* after a short vowel (*taloon*), *-hVn* after a long vowel or diphthong in
  a monosyllable (*maahan*, *työhön*, *tiehen*), *-seen* after a long vowel in a
  longer word (*vieraaseen*, *hameeseen*). Plural: *-ihin*, *-iin*, *-isiin*.
- **Comitative is plural-form-only and requires a possessive suffix**:
  *vaimoineen* "with his wife". Avoid it below C1 unless it is the teaching point.
- The **essive keeps the strong grade**: *iltana*, *kattona*, *lapsena*.

---

## 6. The partitive — deep dive

*One of the two declared weak areas. Treat every partitive plural in a lesson as
a form to be derived, not recalled.*

### 6.1 What the partitive does

1. **Negated object and negated existential subject.** *En osta autoa.* *Ei ole
   aikaa.* This is absolute: negation always partitives the object.
2. **Partial or unbounded quantity.** *Ostin leipää* (some bread) vs *ostin
   leivän* (a/the loaf).
3. **Atelic / ongoing action.** *Luen kirjaa* (reading at it) vs *luen kirjan*
   (will read it through). The object case is where Finnish encodes aspect.
4. **After numerals above one, and after quantity words.** *kaksi kuppia*,
   *paljon ihmisiä*, *vähän aikaa*. Note: the noun is **singular** partitive after
   a numeral, but plural partitive after a plural quantifier.
5. **Existential subjects that are indefinite/mass.** *Pöydällä on kirjoja.*
6. **Government of specific verbs** — *rakastaa, odottaa, auttaa, katsoa,
   kuunnella, ajatella, harrastaa, pelätä, ikävöidä, tarvita*… Your deck marks
   these inline as `(+ P)`; there are 34 such annotations, and they are worth
   honouring exactly, because a partitive verb takes the partitive even when the
   action is complete.
7. **Predicate complements of mass/abstract subjects.** *Ilma on kylmää.*
8. **After certain prepositions/postpositions**: *ilman rahaa*, *ennen joulua*.

### 6.2 Partitive singular

The ending is **-A**, **-tA** or **-ttA**, chosen by type, and the choice is not
predictable from spelling alone (*risti → ristiä* but *tiili → tiiltä*). Broadly:

- **-A** after a single short vowel stem: *kala → kalaa*, *talo → taloa*,
  *risti → ristiä*, *ovi → ovea*, *koira → koiraa*.
- **-tA** after a long vowel, diphthong or consonant stem: *maa → maata*,
  *työ → työtä*, *vieras → vierasta*, *nainen → naista*, *mies → miestä*,
  *pieni → pientä*, *puhelin → puhelinta*, *kevät → kevättä*.
- **-ttA** for the *-e* type and the *-Us/-yys* abstracts: *hame → hametta*,
  *huone → huonetta*, *perhe → perhettä*, *kalleus → kalleutta*.
- Type 41 (*vieras*) lengthens **the vowel already in the word**, which is not
  always *a*: *vieras : vieraan : vierasta* but *kaunis : kauniin : kaunista*,
  *kallis : kalliin*, *valmis : valmiin*, *tiivis : tiiviin*, *altis : alttiin*.
  The partitive itself is built on the consonant stem, so it stays *-s* + *-tA*.
- Types 27–31 replace *-si*: *käsi → kättä*, *uusi → uutta*, *lapsi → lasta*,
  *veitsi → veistä*, *kaksi → kahta*.

The partitive singular keeps the **strong** grade of a direct-gradation word
(*kattoa*, *takkia*) and the **weak/consonant-stem** grade of an inverse one
(*vierasta*, *kytkintä*, *katetta*).

### 6.3 Partitive plural — the hard part

Formation is **plural stem + -A or -tA**. Two things have to be right: the plural
stem, and which ending it takes.

**Step 1 — build the plural stem** (vowel stem + *-i-*):

| stem ends in | change before -i- | example |
|---|---|---|
| -o, -ö, -u, -y | nothing | talo → taloi-, kylpy → kylpyi- |
| -i | → -e- | risti → riste-i-, takki → takke-i- |
| -e | drops | hame → hamei-, nalle → nallei- |
| -a (2-syll., 1st syll. has a/o/u) | → -o- | kala → kaloi-, ilta → iltoi- |
| -a (2-syll., 1st syll. has e/i) | drops | koira → koiri-, kirja → kirjoi- ⚠ |
| -ä | drops | kylä → kyli-, pöytä → pöyti- |
| -aa, -ää | shortens | vapaa → vapai-, maa → mai- |
| -ea/-eä | e drops | korkea → korkei- |
| -ia/-iä (3+ syll.) | → -oi-/-öi- | asia → asioi-, kulkija → kulkijoi- |
| long/diphthong | shortens or fronts | suo → soi-, työ → töi-, tie → tei- |

⚠ The two-syllable *-a* rule is the classic trap and the reason to check rather
than reason: *kala → kaloja* but *koira → koiria*. Kotus splits them into types
9 and 10 precisely because the rule is lexical. **Look the word up.**

**Step 2 — choose the ending.**

- **-A** (i.e. *-ja/-jä*, *-ia/-iä*, *-eja/-ejä*) after a short plural stem:
  *taloja, koiria, kaloja, ristejä, kaupunkeja, naisia, opettajia*.
- **-tA** (i.e. *-ita/-itä*, *-oita/-öitä*) after a long vowel, diphthong or
  consonant stem: *maita, töitä, vieraita, hameita, kulkijoita, asioita,
  vastauksia*… and the three-or-more-syllable *-ia/-ijA* words generally.
- Several types license **both**, and Kotus lists both: *palveluja ~ palveluita*,
  *laatikkoja ~ laatikoita*, *mansikoita ~ mansikkoja*, *papereja ~ papereita*.
  Where both exist, pick one and use it consistently within a lesson; note in the
  glossary that the other exists.

**Gradation interacts.** With *-jA* the stem syllable stays open, so the strong
grade survives (*mansikkoja*, *laatikkoja*); with *-itA* the stem is reshaped and
the weak grade appears (*mansikoita*, *laatikoita*). Both are correct; they are
different forms of the same word.

**Frequency in the student's own deck.** Of the deck's exactly-matched nominals,
1,612 sit in types whose plural partitive is a simple *-jA/-iA/-ejA*, and 359 in
the *-itA/-OitA* types. So the *-itA* group is the minority — but it contains
*asia, kulkija/opiskelija/tutkija, mansikka, vieras, hame, maa, työ*, which are
exactly the high-frequency words a lesson will reach for.

### 6.4 The partitive drill this suggests

Since the weakness is specifically partitive plural, lessons should aim for a
**deliberate spread of types** rather than whatever the topic throws up: one
*-jA* word, one *-iA* word, one *-itA* word and one gradating word per text, all
glossed with their nominative singular so the student can reconstruct the path.

---

## 7. The genitive — deep dive

*The second declared weak area, specifically the genitive/partitive contrast and
the plural genitive.*

### 7.1 What the genitive does

1. Possession and part–whole: *Matin auto*, *talon katto*.
2. **Total object** in an affirmative, telic clause: *Ostin auton.*
3. Complement of most postpositions: *talon takana*, *sinun kanssasi*.
4. Subject of necessive constructions: *Minun täytyy mennä.*
5. Agent of the agent participle: *isän tekemä ruoka*.
6. Genitive of measure/duration: *kahden tunnin matka*.

### 7.2 Genitive singular

Uniformly **vowel stem + -n**, taking the weak grade in direct-gradation words:
*talon, kaupungin, katon, naisen, vieraan, hameen, veden, miehen, lapsen*.
This is the reliable one.

### 7.3 Genitive plural — four endings

| ending | where | examples |
|---|---|---|
| **-ien** | most *-i* types and many two-stem words | ristien, ovien, koirien, kielien, kaupunkien, pienien |
| **-jen** | after a two-syllable plural stem in *-oi-/-öi-/-ui-* etc., where *-i-* surfaces as *j* between vowels | talojen, kalojen, kylpyjen, laatikkojen |
| **-iden / -itten** | after a long vowel or diphthong plural stem | maiden/maitten, vieraiden, hameiden, kulkijoiden, asioiden, töiden |
| **-ten** | consonant-stem types | naisten, lasten, miesten, pienten, nuorten, kytkinten |

Several types allow two or three of these, and Kotus lists them in order of
currency: *naisten ~ naisien*, *pienten ~ pienien*, *sisarien ~ sisarten*,
*paperien ~ papereiden ~ papereitten*. The archaic *-in* (*kalain*, *koirain*)
survives only in fixed phrases and poetry — do not use it in lessons.

**Practical rule for drafting**: the plural genitive is the form most worth
running through `decline.py` every single time, because the four endings are
distributed lexically and the *-ten* type is not predictable from the nominative.

### 7.4 Genitive vs partitive: the contrast to teach

The pair that actually matters at this level is **total vs partial object**:

| | partitive object | total object |
|---|---|---|
| aspect | ongoing, atelic | completed, telic |
| quantity | partial, unbounded | whole, bounded |
| negation | always | never |
| *Luin kirjaa.* | I was reading the book | |
| *Luin kirjan.* | | I read the book (through) |
| *Join kahvia.* | I drank (some) coffee | |
| *Join kahvin.* | | I drank the coffee (up) |

The total object appears in the **genitive** form in an ordinary affirmative
clause (*ostin auton*), but in the **nominative** after an imperative
(*osta auto!*), in a necessive clause (*minun täytyy ostaa auto*), and in the
passive (*ostettiin auto*); and as **nominative plural** for plural totals
(*söin omenat*). Personal pronouns use the dedicated accusative: *minut, sinut,
hänet, meidät, teidät, heidät*.

---

## 8. Adjectives

Adjectives agree with their head in **case and number**: *isossa punaisessa
talossa*, *kauniita kukkia*, *vanhojen ystävien*. Agreement is total, which makes
adjective-heavy sentences an efficient way to drill case morphology — and an
efficient way to produce four errors at once, so check each agreeing word.

Predicative adjectives take the nominative with a countable subject (*talo on
iso*) and the **partitive** with a mass/abstract subject (*vesi on kylmää*,
*ilma on raikasta*) and with plural subjects (*talot ovat isoja*).

### Comparison

- **Comparative**: *-mpi* on the vowel stem, with *-mpi/-mman-* (type 16):
  *iso → isompi : isomman : isompaa*. Two-syllable stems in *-a/-ä* change it to
  *-e-*: *vanha → vanhempi*, *kylmä → kylmempi*.
- **Superlative**: *-in*, with stem changes: *iso → isoin : isoimman*;
  *kaunis → kaunein*; *hyvä → paras : parhaan*.
- Suppletive: *hyvä – parempi – paras*; *pitkä – pidempi – pisin*.
- Comparison objects: *kuin* (*isompi kuin talo*) or the partitive of comparison
  (*taloa isompi*).

---

## 9. Numerals

- 1–10: *yksi, kaksi, kolme, neljä, viisi, kuusi, seitsemän, kahdeksan, yhdeksän,
  kymmenen*. All inflect: *yksi : yhden : yhtä*; *kaksi : kahden : kahta*;
  *seitsemän : seitsemän : seitsemää* (Kotus notes these inflect as though the
  nominative were *seitsemä*, *kahdeksa*, *yhdeksä*, *kymmen*).
- **A numeral above one puts its noun in the partitive singular**: *kaksi kirjaa*,
  *kolmekymmentä vuotta*. In an oblique case, both numeral and noun inflect and
  agree: *kahdessa kirjassa*, *kolmelle lapselle*.
- Ordinals: *ensimmäinen, toinen, kolmas, neljäs…* (*kolmas : kolmannen*, type 45).
- Compound numerals inflect every part in careful register: *kahdellakymmenellä-
  viidellä*. Lessons below B2 should keep numerals in the nominative or the
  partitive.

---

## 10. Pronouns

- Personal: *minä, sinä, hän, me, te, he* — with the accusative *minut, sinut,
  hänet, meidät, teidät, heidät*, and partitive *minua, sinua, häntä, meitä,
  teitä, heitä*.
- Genitive forms double as possessive determiners and normally co-occur with the
  possessive suffix: *minun autoni*, *hänen talonsa*.
- Demonstratives: *tämä, tuo, se* (sg) / *nämä, nuo, ne* (pl). *se/ne* also serve
  as third-person pronouns for non-humans and, in speech, for humans too.
- Interrogatives: *kuka/ketkä* (who), *mikä/mitkä* (what/which), *kumpi* (which of
  two), *millainen* (what sort).
- Relative: *joka* (agrees with a nominal antecedent), *mikä* (with a clause,
  a superlative or a *se*-antecedent). *Talo, jossa asun.* / *Se, mikä minua
  kiinnostaa.*
- Indefinite/negative: *joku, jokin, kukaan, mikään, jokainen, kaikki, moni,
  muutama, harva*. *kukaan/mikään* require negation.
- Reflexive: *itse* + possessive suffix (*itseni, itsesi…*).

---

## 11. Postpositions and prepositions

Finnish is overwhelmingly postpositional, and **most postpositions govern the
genitive**: *talon edessä, pöydän alla, sinun kanssasi, kaupungin läpi, tämän
jälkeen, minun mielestäni*. A smaller set governs the **partitive**: *ilman
rahaa, ennen joulua, pitkin katua, vastapäätä taloa*. A few words work either
way (*keskellä*).

**Verb rection** (case government) is lexical and must be learned per verb; it is
one of the highest-value things a graded reader can recycle. The deck already
annotates it inline — `(+ P)`, `(+ S-MIHIN)`, `(+ S-MISTÄ)`, `(+ G)`,
`(+ -maan/-mään)` — across 100+ entries. Honour these annotations exactly when
using such a verb in a lesson; that is free reinforcement of something already
studied. Common patterns: *pitää **jostakin***, *tykätä **jostakin***, *rakastua
**johonkuhun***, *tutustua **johonkin***, *auttaa **jotakuta***, *osallistua
**johonkin***, *kiinnostua **jostakin***.

---

## 12. Possessive suffixes

| person | suffix |
|---|---|
| 1sg | -ni |
| 2sg | -si |
| 3sg/3pl | -nsa / -nsä, or -Vn after a case ending |
| 1pl | -mme |
| 2pl | -nne |

Attached **after** the case ending, to the strong-grade stem:
*taloni, talossani, taloissamme, ystäväni, ystävälleni*.

Points that trip learners:

- The possessive suffix **blocks the weak grade** where it would otherwise apply,
  because it re-opens the syllable: *pöytä → pöydän* but *pöytäni*;
  *takki → takin* but *takkini*.
- The nominative and genitive singular fall together under a possessive suffix:
  *taloni* = "my house" (nom) or "of my house" (gen).
- The 3rd person after a case ending lengthens the vowel and adds *-n*:
  *talossaan*, *ystävälleen*.
- With a personal-pronoun genitive the suffix is still required in standard
  written Finnish (*minun autoni*), but **spoken Finnish drops it** (*mun auto*).
  Decide per lesson which register you are writing and be consistent.

---

## 13. Clitic particles

Attach to the end of the word, after any possessive suffix, and are subject to
vowel harmony.

| clitic | force |
|---|---|
| **-kO** | yes/no question, on the focused word: *Tuletko?* *Sinäkö tulet?* |
| **-kin** | also, too, even; mild surprise: *Minäkin tulen.* |
| **-kAAn** | the negative-polarity counterpart of *-kin*: *En minäkään tule.* |
| **-hAn** | shared knowledge, softening, "you know": *Onhan se totta.* |
| **-pA / -pä** | emphasis, contradiction, exclamation: *Onpa kaunista!* |
| **-kA** | attaches to negatives and conjunctions: *eikä, jotta, vaikka* |

They stack in a fixed order (*-kO* before *-hAn*: *onkohan*). For graded reading
they are excellent value: high frequency, low morphological cost, and they carry
the conversational texture that makes a text feel like real Finnish rather than
textbook Finnish.

---

## 14. Verbs: types and stems

Six traditional learner types map onto Kotus 52–78 (full table in Appendix B):

| learner type | infinitive shape | Kotus | stem rule | example |
|---|---|---|---|---|
| 1 | -A after a vowel | 52–57, 61 | drop -A | sanoa → sano- |
| 2 | -dA | 62–65 | drop -dA | juoda → juo- |
| 3 | -lA, -nA, -rA, -stA | 66, 67, 70 | drop the last two letters, add -e- | tulla → tule- |
| 4 | -AtA, -OtA, -UtA | 73, 74 | drop -tA, add -A- | tavata → tapaa- |
| 5 | -itA | 69 | drop -tA, add -tse- | tarvita → tarvitse- |
| 6 | -etA | 72, 75 | drop -tA, add -ne- | vanheta → vanhene- |

Every verb has a **strong stem** (visible in the 3rd person: *he ottavat*) and,
for gradating verbs, a **weak stem** (visible in the 1st/2nd person: *minä otan*).
Which stem a form uses is the thing to get right; see §15.2.

Personal endings, present: **-n, -t, –(lengthening), -mme, -tte, -vAt**.
The 3rd singular lengthens the stem-final vowel (*ottaa*, *sanoo*, *lukee*) —
except where the stem already ends in a long vowel or diphthong (*saa*, *juo*, *voi*).

---

## 15. Tenses and moods

### 15.1 Tenses

- **Present** doubles as the future: *Menen huomenna.*
- **Imperfect (past)** marker *-i-*, with the vowel changes that make it hard:
  *ottaa → otti*, *sanoa → sanoi*, *lukea → luki*, *antaa → antoi*,
  *huutaa → huusi*, *tietää → tiesi*, *juoda → joi*, *käydä → kävi*.
  Note *-ta-/-tä-* → *-si-* in types 54–57 and 76 (*huutaa → huusi*,
  *tietää → tiesi*, *ymmärtää → ymmärsi*).
- **Perfect**: *olla* (present) + NUT-participle. *Olen lukenut.*
- **Pluperfect**: *olla* (imperfect) + NUT-participle. *Olin lukenut.*
- Negation: the negative verb *en, et, ei, emme, ette, eivät* + the connegative
  (bare weak stem in the present, NUT-participle in the past): *en ota*,
  *en ottanut*, *emme ottaneet*.

### 15.2 Conditional (konditionaali) — the current teaching focus

**Marker `-isi-`, between the stem and the personal ending.**

**The rule that matters most: the conditional is built on the STRONG stem.**
Not the 1st-person-singular stem. This is verified against Kotus for all 27 verb
types and stated explicitly by Uusi kielemme ("you will add this marker to the
strong stem… every form will be strong in the conditional").

| verb | 1sg present (weak) | conditional (strong) |
|---|---|---|
| pitää | pi**d**än | pi**t**äisi |
| ottaa | o**t**an | o**tt**aisi |
| lukea | luen | lu**k**isi |
| huutaa | huu**d**an | huu**t**aisi |
| lähteä | läh**d**en | läh**t**isi |
| antaa | a**nn**an | a**nt**aisi |
| ymmärtää | ymmä**rr**än | ymmä**rt**äisi |
| kertoa | ke**rr**on | ke**rt**oisi |
| tietää | tie**d**än | tie**t**äisi |
| nähdä | näen | nä**k**isi |
| tavata | ta**p**aan | ta**p**aisi |

Getting this wrong produces *pidäisi*, *otaisi*, *huudaisi* — plausible-looking
and completely wrong. Since the conditional is the current textbook topic, this
is the single highest-risk form class in the project right now.

**Stem behaviour before -isi-**

| stem ends in | before -isi- | example |
|---|---|---|
| -o, -u, -y, -ö | unchanged | sanoa → sanoisi, puhua → puhuisi |
| -a, -ä | **unchanged** (unlike the past tense) | ottaa → ottaisi, muistaa → muistaisi |
| -e | drops | lukea → lukisi, tulla → tulisi, tuntea → tuntisi |
| -i | drops | sallia → sallisi, oppia → oppisi |
| -aa, -ää (long) | shortens | salata (salaa-) → salaisi, saada → saisi |
| diphthong | as in the past | juoda → joisi, syödä → söisi, viedä → veisi, käydä → kävisi |
| -tse- (type 69) | e drops | valita → valitsisi, tarvita → tarvitsisi |
| -ne- (types 72/75) | e drops / -äisi | vanheta → vanhenisi, selvitä → selviäisi |

Contrast with the imperfect, which is where the confusion comes from:
*ottaa → **otti*** (a drops) but *ottaisi* (a stays).

**Full paradigm** (*ottaa*): *ottaisin, ottaisit, ottaisi, ottaisimme,
ottaisitte, ottaisivat.*
**Negative**: negative verb + the *-isi* form without a personal ending —
*en ottaisi, et ottaisi, ei ottaisi, emme ottaisi…*
**Conditional perfect**: *olisi* + NUT-participle — *olisin ottanut*
("I would have taken"). Negative: *en olisi ottanut*.
**Passive conditional**: *-ttAisiin* — *otettaisiin*, *sanottaisiin*, *mentäisiin*.

**Uses** — worth spreading across lessons rather than drilling one:

1. **Hypothetical *jos*-clauses**, conditional in *both* halves:
   *Jos minulla olisi aikaa, matkustaisin Lappiin.* (Finnish does not use a past
   tense in the *if*-clause the way English does.)
2. **Counterfactual past**: *Jos olisin tiennyt, olisin tullut.*
3. **Politeness** — the highest-frequency everyday use: *Saisinko kahvin?*
   *Voisitko auttaa?* *Haluaisin kysyä.* *Olisiko sinulla hetki aikaa?*
4. **Softened opinion / hedging**: *Sanoisin, että…* *Se olisi ehkä parempi.*
5. **Wishes**: *Kunpa sataisi!* *Toivoisin, että…*
6. **Future-in-the-past / reported**: *Hän sanoi, että tulisi myöhemmin.*
7. **After *jotta*/*että* of purpose in some registers**: *Lähdin aikaisin, jotta
   ehtisin junaan.*

Note the register tension worth being aware of: Finnish **plain-language
(selkokieli) guidelines explicitly recommend avoiding the conditional**. That
recommendation targets readers with cognitive or reading difficulties, not L2
learners working through a textbook chapter on the conditional. For this project
the conditional is a *teaching target*, so it goes in deliberately and densely —
but that is a considered departure from selkokieli, not an oversight.

### 15.3 Imperative

- 2sg: the bare weak stem — *ota!*, *tule!*, *lue!*; negative *älä ota*.
- 2pl: *-kAA* on the strong stem — *ottakaa!*; negative *älkää ottako*.
- 3rd person: *-kOOn / -kOOt* — *ottakoon* (rare outside formal/liturgical text).
- 1pl: *-kAAmme* in writing; in speech the **passive** does this job —
  *mennään!* "let's go".

### 15.4 Potential

*-ne-* on the strong stem: *ottanee* "may well take", *lienee* (from *olla*).
Rare in speech, present in news and formal writing. Recognition-only at B1.

### 15.5 Passive / impersonal

Finnish "passive" is really an **impersonal**: no agent may be expressed, and the
implied subject is a human indefinite.

- Present: *-tAAn / -dAAn* — *otetaan, sanotaan, mennään, tehdään*.
- Past: *-ttiin / -tiin* — *otettiin, sanottiin, mentiin*.
- Perfect: *on otettu*; pluperfect *oli otettu*.
- Negative: *ei oteta*, *ei otettu*.
- Conditional: *otettaisiin*.
- The passive takes the **weak grade** in the present/past (*otetaan* from
  *ottaa*), which is a common error site.
- In speech the passive routinely replaces the 1st person plural:
  *me mennään* for *me menemme*. Extremely high frequency — worth teaching
  early as comprehension, and flagging as spoken register.

---

## 16. Infinitives

| infinitive | forms | use |
|---|---|---|
| **1st (A)** | *ottaa*, *tulla*; long form *ottaakseni* | dictionary form; purpose (*ostin kirjan lukeakseni sen*) |
| **2nd (E)** | *ottaessa*, *ottaen* | temporal "while/when" (*syödessäni*), manner (*hymyillen*) |
| **3rd (MA)** | *ottamassa/-masta/-maan/-malla/-matta* | with motion and many verbs: *menen ostamaan*, *lopetin ostamasta*, *ilman että → ostamatta* |
| **4th (MINEN)** | *ottaminen* | verbal noun: *lukeminen on hauskaa* |

The MA-infinitive illative (*-mAAn*) is the one your deck already annotates as
`(+ -maan/-mään)` for verbs like *panna*, *oppia*, *ruveta*. Use those verbs with
that complement to reinforce a pattern already studied.

---

## 17. Participles

| participle | active | passive |
|---|---|---|
| **present (VA/TAVA)** | *ottava* "taking" | *otettava* "to be taken / that must be taken" |
| **past (NUT/TU)** | *ottanut* "having taken" | *otettu* "taken" |
| **agent (MA)** | — | *isän ottama* "taken by father" |
| **negative (MATON)** | *ottamaton* "untaken, un-taking" | — |

All participles are adjectives and **decline and agree** fully: *otetussa
kirjassa*, *väsyneitä ihmisiä*, *äidin tekemää ruokaa*. This is where a lot of
generated Finnish quietly goes wrong, because the participle has to agree *and*
the noun has to be in the right case *and* both have to gradate correctly.

The **agent participle** (*isän tekemä ruoka* "food made by father") takes its
agent in the **genitive** and requires no *by*-phrase. It is a common B1/B2 topic
and a good later target.

---

## 18. Non-finite clause substitutes (lauseenvastikkeet)

Finnish compresses subordinate clauses into participial phrases. These are the
hallmark of authentic written Finnish and are also exactly what selkokieli tells
you to avoid — which makes them a deliberate difficulty dial for this project.

- **Referatiivirakenne** (replacing an *että*-clause): *Tiedän hänen tulevan.*
  = *Tiedän, että hän tulee.* Formed with the genitive subject + VA-participle
  (present reference) or NUT-participle + *-n* (past reference: *Tiedän hänen
  tulleen*).
- **Temporaalirakenne** (replacing a *kun*-clause):
  *Tullessani kotiin…* "when I came home" (2nd infinitive inessive, same subject);
  *Hänen tultuaan kotiin…* "after he came home" (TU-participle + possessive,
  genitive subject).
- **Finaalirakenne** (purpose): *Menin kauppaan ostaakseni leipää.*
- **Modaalirakenne** (manner/means): *Hän tuli juosten.* / *opitaan lukemalla*.

For a student not yet at B1, these belong in **recognition** work with a gloss,
not in production targets. Introduce one construction per lesson at most, always
glossed with its finite-clause paraphrase.

---

## 19. Syntax

### 19.1 Clause types worth writing deliberately

- **Existential**: *Pöydällä on kirja / kirjoja.* Location first, verb *olla* in
  the 3rd singular, subject last and often partitive. Negated: *Pöydällä ei ole
  kirjaa.*
- **Possessive**: *Minulla on auto.* Adessive possessor + *olla* + nominative
  possessed. Negated with partitive: *Minulla ei ole autoa.*
- **Necessive**: *Minun täytyy / pitää / on pakko mennä.* Genitive subject,
  3rd-singular verb, nominative total object.
- **Result/state**: *Minua väsyttää*, *Minun on kylmä* — partitive/genitive
  experiencer, no nominative subject.
- **Generic/zero person**: *Täällä ei saa tupakoida.* No subject at all.

### 19.2 Word order

Basic SVO, but order is **information-structural**, not grammatical: the topic
comes first, new information last. *Kirja on pöydällä* (where the book is) vs
*Pöydällä on kirja* (what is on the table). For graded reading this is a real
control: keeping to plain SVO makes text easier; fronting adverbials and using
existential order makes it more natural and harder. Use it as a difficulty dial.

Questions: yes/no with *-kO* on the fronted focus (*Tuletko sinä?* / *Sinäkö
tulet?*); wh-questions front the question word.

---

## 20. Derivational morphology

Worth exploiting: a graded reader can teach a suffix once and then let the
student decode a dozen new words for free.

- *-jA* agent: *opettaa → opettaja*, *lukea → lukija*
- *-minen* action noun: *lukeminen*
- *-Us / -Os* result: *vastata → vastaus*, *tulla → tulos*
- *-UUs* abstract quality: *kaunis → kauneus*, *lapsi → lapsuus*
- *-lA* place: *kahvi → kahvila*, *sairas → sairaala*
- *-in* instrument: *avata → avain*, *puhua → puhelin*
- *-tOn* caritive "without": *koti → koditon*, *työ → työtön*
- *-llinen* "-ful, -ic": *onni → onnellinen*, *taide → taiteellinen*
- *-tAA* causative: *nousta → nostaa*; *-UtUA* reflexive/anticausative:
  *avata → avautua*
- *-skellA / -ellA* frequentative: *kävellä*, *opiskella*
- *-AhtAA* momentane: *huudahtaa* "to give a shout"

Compounding is unbounded and productive; the head is final and carries the
inflection (*työttömyyskorvaus* → *työttömyyskorvauksen*). When a lesson uses a
long compound, gloss it **decomposed** — that is often more useful than the
translation.

---

## 21. Spoken register (puhekieli)

A declared strength, so it can be used freely as a comprehension bridge — but it
must be **marked** in a lesson, never mixed silently into standard prose. The
deck already tracks 151 entries with a `(spoken)` tag.

| standard | spoken |
|---|---|
| minä, sinä, hän, me, te, he | mä, sä, se, me, te, ne |
| tämä, tuo | tää, toi |
| minun autoni | mun auto |
| olen, olet, on | oon, oot, on |
| menen, tulen | meen, tuun |
| me menemme | me mennään |
| he menevät | ne menee |
| en ole | emmä oo / en oo |
| punainen | punanen (-nen → -nen; *-inen* → *-i*) |
| kirjoittaa | kirjottaa |
| kysyä | kysyy (3sg lengthening lost in some verbs) |
| -a/-ä partitive after o/u/i/e | -oo/-uu/-ii/-ee (*taloa → taloo*) |
| olisi | ois |
| ei ole | ei oo / eiks |

Note the last row: *ois* for *olisi* is very high frequency and directly relevant
to the current conditional topic.

---

## 22. Failure modes to watch for in generated Finnish

A checklist to run over any drafted lesson text.

1. **Weak grade in the illative.** *katoon* for *kattoon*. Check every *-Vn*,
   *-hVn*, *-seen*, *-ihin*.
2. **Weak grade in the conditional.** *pidäisi* for *pitäisi*. Check every *-isi-*.
3. **Weak grade in the essive.** *katona* for *kattona*.
4. **Vowel harmony broken across a compound.** *isoäitia* for *isoäitiä*.
5. **Wrong two-syllable *-a* plural.** *koiroja* for *koiria*, *kaloja* right but
   *kirjoja* also right — these are lexical; look them up.
6. **Wrong plural genitive ending.** *naisien* is licensed, *naisten* is commoner;
   *lapsien* vs *lasten*; *miehien* vs *miesten*.
7. **Partitive/total object confusion.** Check aspect and negation on every object.
8. **Negation forgetting the partitive.** *En osta auton* is wrong.
9. **Numeral not partitive-singular.** *kaksi kirjat* for *kaksi kirjaa*.
10. **Adjective not agreeing** in a plural or oblique case.
11. **Possessive suffix with the weak grade.** *pöydäni* for *pöytäni*.
12. **Verb rection ignored** where the deck already annotates it.
13. **Register mixing** — a *mä* in an otherwise standard paragraph.
14. **Consonant-stem forms invented** for types that don't have them.
15. **Type 41 *-is* words given an *a*-stem** by analogy with *vieras*:
    *kaunian* for *kauniin*.
16. **A neutral-only stem given front endings without checking** — most are
    front, *meri* is not.

---

## Appendix A — Kotus nominal types 1–51

Model paradigms transcribed verbatim from Kotus. "deck" = how many of the
student's single-token headwords match this type exactly; examples are drawn
from that deck.

| # | model | sg part | pl part | pl gen | deck | examples from your deck |
|---|---|---|---|---|---|---|
| 1 | valo | valoa | valoja | valojen | 180 | aalto, aivot, apu, asunto |
| 2 | palvelu | palvelua | palveluja palveluita | palvelujen palveluiden palveluitten | 33 | arvostelu, autoilu, haastattelu, henkilö |
| 3 | valtio | valtiota | valtioita | valtioiden valtioitten | 18 | improvisaatio, kaakao, kaksio, kallio |
| 4 | laatikko | laatikkoa | laatikkoja laatikoita | laatikkojen laatikoiden laatikoitten | 9 | kolikko, kriitikko, laatikko, lepakko |
| 5 | risti | ristiä | ristejä | ristien | 170 | aasi, ambulanssi, antilooppi, appelsiini |
| 6 | paperi | paperia | papereja papereita | paperien papereiden papereitten | 56 | alligaattori, bakteeri, banaani, biisoni |
| 7 | ovi | ovea | ovia | ovien | 36 | arki, arpi, hanhi, hauki |
| 8 | nalle | nallea | nalleja | nallejen (nallein) | 2 | ale, itse |
| 9 | kala | kalaa | kaloja | kalojen (kalain) | 100 | ahma, aika, aita, ala |
| 10 | koira | koiraa | koiria | koirien (koirain) | 160 | ahkera, asema, avara, boa |
| 11 | omena | omenaa | omenia omenoita (omenoja) | omenien omenoiden omenoitten (omenojen) (omenain) | 2 | kihara, omena |
| 12 | kulkija | kulkijaa | kulkijoita | kulkijoiden kulkijoitten (kulkijain) | 49 | allergia, apina, asia, energia |
| 13 | katiska | katiskaa | katiskoita katiskoja | katiskoiden katiskoitten katiskojen (katiskain) | 15 | gorilla, hyeena, kampela, karitsa |
| 14 | solakka | solakkaa | solakoita solakkoja | solakoiden solakoitten solakkojen (solakkain) | 19 | alpakka, etikka, haarukka, harakka |
| 15 | korkea | korkeaa korkeata | korkeita | korkeiden korkeitten (korkeain) | 26 | ainoa, ankea, hempeä, hirveä |
| 16 | vanhempi | vanhempaa | vanhempia | vanhempien (vanhempain) | 2 | kumpi, parempi |
| 17 | vapaa | vapaata | vapaita | vapaiden vapaitten | 4 | paluu, suklaa, takuu, vapaa |
| 18 | maa | maata | maita | maiden maitten | 20 | hai, häät, jää, kuu |
| 19 | suo | suota | soita | soiden soitten | 3 | suo, vyö, yö |
| 20 | filee | fileetä | fileitä | fileiden fileitten | 0 | — |
| 21 | rosé | roséta | roséita | roséiden | 0 | — |
| 22 | parfait | parfait'ta | parfait'ita | parfait'iden | 0 | — |
| 23 | tiili | tiiltä | tiiliä | tiilien | 4 | lohi, moni, tuli, vuohi |
| 24 | uni | unta | unia | unien unten | 5 | hiiri, huuli, kuusi, meri |
| 25 | toimi | tointa toimea | toimia | toimien tointen | 2 | lumi, niemi |
| 26 | pieni | pientä | pieniä | pienten pienien | 13 | huoli, juuri, kieli, mieli |
| 27 | käsi | kättä | käsiä | käsien (kätten) | 7 | kuukausi, käsi, susi, tosi |
| 28 | kynsi | kynttä | kynsiä | kynsien (kyntten) | 3 | kansi, kynsi, varsi |
| 29 | lapsi | lasta | lapsia | lasten lapsien | 1 | lapsi |
| 30 | veitsi | veistä | veitsiä | veitsien (veisten) | 1 | veitsi |
| 31 | kaksi | kahta | kaksia | kaksien | 2 | kaksi, yksi |
| 32 | sisar | sisarta | sisaria | sisarien sisarten | 8 | ahven, höyhen, joutsen, kämmen |
| 33 | kytkin | kytkintä | kytkimiä | kytkimien kytkinten | 10 | avain, avoin, eläin, hapan |
| 34 | onneton | onnetonta | onnettomia | onnettomien (onnetonten) | 19 | huolimaton, hyödytön, kelvoton, kesytön |
| 35 | lämmin | lämmintä | lämpimiä | lämpimien (lämpimäin) | 1 | lämmin |
| 36 | sisin | sisintä | sisimpiä | sisimpien sisinten (sisimpäin) | 0 | — |
| 37 | vasen | vasenta (vasempaa) | vasempia | vasempien vasenten (vasempain) | 1 | vasen |
| 38 | nainen | naista | naisia | naisten naisien | 139 | aamiainen, aikuinen, aktiivinen, ampiainen |
| 39 | vastaus | vastausta | vastauksia | vastausten vastauksien | 78 | ahdistus, ajoitus, alennus, aloitus |
| 40 | kalleus | kalleutta | kalleuksia | kalleuksien | 21 | erikoisuus, hiljaisuus, juhlallisuus, kiitollisuus |
| 41 | vieras | vierasta | vieraita | vieraiden vieraitten | 45 | ahdas, ahnas, arvokas, asukas |
| 42 | mies | miestä | miehiä | miesten miehien | 1 | mies |
| 43 | ohut | ohutta | ohuita | ohuiden ohuitten | 2 | lyhyt, olut |
| 44 | kevät | kevättä | keväitä | keväiden keväitten | 1 | kevät |
| 45 | kahdeksas | kahdeksatta | kahdeksansia | kahdeksansien | 1 | yhdeksäs |
| 46 | tuhat | tuhatta | tuhansia | tuhansien (tuhanten) | 0 | — |
| 47 | kuollut | kuollutta | kuolleita | kuolleiden kuolleitten | 5 | ahdistunut, hermostunut, kokenut, masentunut |
| 48 | hame | hametta | hameita | hameiden hameitten | 43 | aihe, alue, aste, esite |
| 49 | askel | askelta | askelia | askelien askelten | 1 | sammal |
| 50 | isoäiti | isoäitiä | isoäitejä | isoäitien | 8 | isoisä, isovanhemmat, isoäiti, kovakuoriainen |
| 51 | nuoripari | nuortaparia | nuoriapareja | nuortenparien nuorienparien | 3 | isoveli, mustamakkara, uusivuosi |


## Appendix B — Kotus verb types 52–78

Eight principal parts per type, verbatim from Kotus. The conditional column is
bolded because it is the current teaching focus and because it is the column that
shows the strong grade most clearly against the 1sg present.

| # | 1st inf | pres 1sg | past 3sg | **cond 3sg** | pot 3sg | imper 3sg | NUT | pass past | deck | examples |
|---|---|---|---|---|---|---|---|---|---|---|
| 52 | sanoa | sanon | sanoi | **sanoisi** | sanonee | sanokoon | sanonut | sanottiin | 99 | aikoa, astua, asua, haukkoa |
| 53 | muistaa | muistan | muisti | **muistaisi** | muistanee | muistakoon | muistanut | muistettiin | 154 | ahdistaa, aiheuttaa, aloittaa, arvostaa |
| 54 | huutaa | huudan | huusi | **huutaisi** | huutanee | huutakoon | huutanut | huudettiin | 19 | alentaa, huutaa, kiertää, kohentaa |
| 55 | soutaa | soudan | souti sousi | **soutaisi** | soutanee | soutakoon | soutanut | soudettiin | 3 | kiitää, liitää, yltää |
| 56 | kaivaa | kaivan | kaivoi | **kaivaisi** | kaivanee | kaivakoon | kaivanut | kaivettiin | 22 | ajaa, alkaa, antaa, auttaa |
| 57 | saartaa | saarran | saarsi saartoi | **saartaisi** | saartanee | saartakoon | saartanut | saarrettiin | 1 | kaataa |
| 58 | laskea | lasken | laski | **laskisi** | laskenee | laskekoon | laskenut | laskettiin | 9 | hakea, itkeä, kokea, koskea |
| 59 | tuntea | tunnen | tunsi | **tuntisi** | tuntenee | tuntekoon | tuntenut | tunnettiin | 1 | tuntea |
| 60 | lähteä | lähden | lähti (läksi) | **lähtisi** | lähtenee | lähteköön | lähtenyt | lähdettiin | 1 | lähteä |
| 61 | sallia | sallin | salli | **sallisi** | sallinee | sallikoon | sallinut | sallittiin | 32 | ehtiä, etsiä, hankkia, hiipiä |
| 62 | voida | voin | voi | **voisi** | voinee | voikoon | voinut | voitiin | 7 | imuroida, kopioida, remontoida, soida |
| 63 | saada | saan | sai | **saisi** | saanee | saakoon | saanut | saatiin | 3 | jäädä, myydä, saada |
| 64 | juoda | juon | joi | **joisi** | juonee | juokoon | juonut | juotiin | 4 | juoda, luoda, syödä, viedä |
| 65 | käydä | käyn | kävi | **kävisi** | käynee | käyköön | käynyt | käytiin | 1 | käydä |
| 66 | rohkaista | rohkaisen | rohkaisi | **rohkaisisi** | rohkaissee | rohkaiskoon | rohkaissut | rohkaistiin | 13 | julkaista, kiljaista, mutista, nielaista |
| 67 | tulla | tulen | tuli | **tulisi** | tullee | tulkoon | tullut | tultiin | 65 | ajatella, arvailla, arvostella, esitellä |
| 68 | tupakoida | tupakoin (tupakoitsen) | tupakoi (tupakoitsi) | **tupakoisi (tupakoitsisi)** | tupakoinee | tupakoikoon | tupakoinut | tupakoitiin | 0 | — |
| 69 | valita | valitsen | valitsi | **valitsisi** | valinnee | valitkoon | valinnut | valittiin | 9 | havaita, häiritä, mainita, merkitä |
| 70 | juosta | juoksen | juoksi | **juoksisi** | juossee | juoskoon | juossut | juostiin | 1 | juosta |
| 71 | nähdä | näen | näki | **näkisi** | nähnee | nähköön | nähnyt | nähtiin | 2 | nähdä, tehdä |
| 72 | vanheta | vanhenen | vanheni | **vanhenisi** | vanhennee | vanhetkoon | vanhennut | vanhettiin | 5 | lämmetä, pimetä, tarjeta, vaieta |
| 73 | salata | salaan | salasi | **salaisi** | salannee | salatkoon | salannut | salattiin | 50 | arvata, avata, grillata, haitata |
| 74 | katketa | katkean | katkesi | **katkeaisi (katkeisi)** | katkennee | katketkoon | katkennut | katkettiin | 11 | erota, inhota, kadota, kajota |
| 75 | selvitä | selviän | selvisi | **selviäisi** | selvinnee | selvitköön | selvinnyt | selvittiin | 5 | haluta, hävitä, levitä, selvitä |
| 76 | taitaa | taidan | taisi | **taitaisi** | taitanee tainnee | taitakoon | tainnut taitanut | taidettiin | 2 | taitaa, tietää |
| 77 | kumajaa | kumaji | kumajaisi | **—** | — | — | — | — | 0 | — |
| 78 | kaikaa | kaikaisi | — | **—** | — | — | — | — | 0 | — |

---

## Sources

**Primary — inflectional data**

- Kotimaisten kielten keskus (Institute for the Languages of Finland),
  *Nykysuomen sanalista*, version 1 (15 Dec 2006). 94,110 headwords with
  inflection type (1–51 nominal, 52–78 verb, 99 indeclinable) and consonant-
  gradation class (A–M); the accompanying `sanalistan-kuvaus.txt` carries the
  full model paradigms for every type and the gradation-class inventory.
  Released under the GNU LGPL. Obtained via the `hugovk/everyfinnishword` mirror
  and reduced to `tools/kotus.tsv` + `tools/kotus_models.json`.
  Type list also published at <https://kaino.kotus.fi/sanat/nykysuomi/taivutustyypit.php>.

**Primary — reference grammar**

- *Iso suomen kielioppi* (VISK), Kotimaisten kielten keskus, verkkoversio.
  <https://scripta.kotus.fi/visk/etusivu.php> — consulted for the definition of
  inflection types and stems (§53, §63, §65) and for syntax.

**Secondary — usage and pedagogy**

- Uusi kielemme, *Finnish Grammar* — <https://uusikielemme.fi/finnish-grammar>
  (partitive, conditional, object marking, participles, spoken language).
  Source of the explicit statement that the conditional is built on the strong
  stem, independently confirmed here against the Kotus paradigms for all 27 verb
  types.
- Jukka Korpela, *Handbook of Finnish* — <https://jkorpela.fi/finnish/>
  (cases, object marking, conditional).
- Panu Mäkinen, *Finnish Grammar* (University of Jyväskylä) —
  <https://users.jyu.fi/~pamakine/kieli/suomi/sijat/indexen.html> (stems).
- Wikipedia, *Finnish consonant gradation* —
  <https://en.wikipedia.org/wiki/Finnish_consonant_gradation> (gradation-pair
  inventory, cross-checked against the Kotus class list).

**Plain-language / graded-text norms for Finnish**

- Selkokeskus, *The Easy Finnish Indicator 2.0* —
  <https://selkokeskus.fi/in-english/easy-finnish/the-easy-finnish-indicator-2-0/>
- Selkokeskus, *Writing in Easy Finnish* —
  <https://selkokeskus.fi/in-english/easy-finnish/writing-in-easy-finnish/>

**Note on secondary sources.** Where a secondary source and the Kotus data
disagreed about a *form*, Kotus won. Several prose summaries consulted during
this research contained typos in Finnish examples (*astiioita* for *astioita*,
*rikas* miscopied, *järvea* for *järveä*), which is precisely why the paradigms in
this file are machine-derived from Kotus rather than transcribed from prose.
