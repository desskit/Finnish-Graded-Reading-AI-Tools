#!/usr/bin/env python3
"""Finnish consonant gradation (astevaihtelu), Kotus classes A-M.

Grade is decided phonologically: build the STRONG-grade form, syllabify it,
find the syllable whose ONSET is the last consonant of the gradation cluster,
and switch to the weak grade iff that syllable is CLOSED.

Known exception implemented: the singular illative ending (-Vn / -hVn / -seen)
never triggers the weak grade  (katto : kattoon, aurinko : aurinkoon).

Class inventory: Kotus, "Nykysuomen sanalista" sanalistan-kuvaus.txt (2006).
"""
VOWELS = "aeiouyäö"
# All Finnish diphthongs occur in the FIRST syllable. In non-initial syllables
# only the i-final and u/y-final ones do; ie, uo, yö never do. This matters for
# gradation: tak-ki-en (not *tak-kien), so the -kk- syllable is open -> strong.
DIPH_INITIAL = {"ai","ei","oi","ui","yi","äi","öi","au","eu","iu","ou","ey","iy",
                "äy","öy","ie","uo","yö"}
DIPH_NONINITIAL = {"ai","ei","oi","ui","yi","äi","öi","au","eu","iu","ou","ey","iy","äy","öy"}

PAIRS = {
 "A": ("kk","k"), "B": ("pp","p"), "C": ("tt","t"), "D": ("k",""),
 "E": ("p","v"),  "F": ("t","d"),  "G": ("nk","ng"), "H": ("mp","mm"),
 "I": ("lt","ll"),"J": ("nt","nn"),"K": ("rt","rr"), "L": ("k","j"),
 "M": ("k","v"),
}

def syllabify(w):
    """Finnish syllabification. Returns list of syllables covering w exactly."""
    w = w.lower()
    out, i, n = [], 0, len(w)
    cur = ""
    while i < n:
        first = not out
        # onset: consonants (at most the one that starts this syllable)
        while i < n and w[i] not in VOWELS:
            cur += w[i]; i += 1
        if i >= n:
            break
        # nucleus
        cur += w[i]; i += 1
        if i < n and w[i] in VOWELS:
            pair = cur[-1] + w[i]
            allowed = DIPH_INITIAL if first else DIPH_NONINITIAL
            if pair in allowed or pair[0] == pair[1]:
                cur += w[i]; i += 1
        # coda: consonants, but leave the LAST one as onset of next syllable
        j = i
        cons = ""
        while j < n and w[j] not in VOWELS:
            cons += w[j]; j += 1
        if j >= n:
            cur += cons                     # word-final consonants stay in coda
            i = j
        else:
            if len(cons) > 1:
                cur += cons[:-1]            # all but last -> coda
                i = j - 1                   # last consonant -> next onset
            else:
                i = j - len(cons)           # single consonant -> next onset
        out.append(cur); cur = ""
    if cur:
        out.append(cur)
    return out

def _closed(s):
    return bool(s) and s[-1] not in VOWELS

def apply_gradation(strong_form, av, stem_len=None, is_illative=False):
    if not av or av not in PAIRS or is_illative:
        return strong_form
    strong, weak = PAIRS[av]
    lw = strong_form.lower()
    # Confine the search to the STEM: an identical cluster inside the ENDING
    # (kattoi+tta) must not be mistaken for the gradation site. A cluster that
    # merely straddles the junction still starts inside the stem, so it is found.
    limit = stem_len if stem_len else len(lw)
    idx = lw.rfind(strong, 0, limit)
    # gradation never touches a word-initial consonant (tainnut, not *dainnut)
    if idx <= 0:
        return strong_form
    onset_pos = idx + len(strong) - 1
    pos = 0
    for s in syllabify(lw):
        if pos <= onset_pos < pos + len(s):
            return (strong_form[:idx] + weak + strong_form[idx+len(strong):]) \
                   if _closed(s) else strong_form
        pos += len(s)
    return strong_form

def strengthen(weak_form, av, stem_len=None):
    """Weak -> strong, for inverse-gradation types (opas : oppaan).

    Replaces the LAST occurrence of the weak cluster inside the stem.
    Class D (k : zero) has no anchor in the weak grade, so it is refused.
    """
    if not av or av not in PAIRS:
        return weak_form, True
    strong, weak = PAIRS[av]
    if weak == "":
        return weak_form, False          # cannot locate an elided k -- refuse
    lw = weak_form.lower()
    limit = stem_len if stem_len else len(lw)
    idx = lw.rfind(weak, 0, limit)
    if idx < 0:
        return weak_form, False
    return weak_form[:idx] + strong + weak_form[idx+len(weak):], True


if __name__ == "__main__":
    # syllabification sanity
    for w, exp in [("laatikkojen",["laa","tik","ko","jen"]),
                   ("katossa",["ka","tos","sa"]),
                   ("kattoon",["kat","toon"]),
                   ("aurinko",["au","rin","ko"]),
                   ("opiskelija",["o","pis","ke","li","ja"]),
                   ("takkien",["tak","ki","en"]),
                   ("kattoihin",["kat","toi","hin"]),
                   ("tiedän",["tie","dän"])]:
        got = syllabify(w)
        print(("ok  " if got==exp else "FAIL"), w, got, "" if got==exp else f"expected {exp}")
    print()
    tests = [
      ("katto","C",False,"katto"),("katton","C",False,"katon"),("kattoa","C",False,"kattoa"),
      ("kattossa","C",False,"katossa"),("kattona","C",False,"kattona"),
      ("kattoksi","C",False,"katoksi"),("kattot","C",False,"katot"),
      ("kattojen","C",False,"kattojen"),("kattoja","C",False,"kattoja"),
      ("kattoihin","C",False,"kattoihin"),("kattoilla","C",False,"katoilla"),
      ("kattoon","C",True,"kattoon"),
      ("laatikkojen","A",False,"laatikkojen"),("laatikkon","A",False,"laatikon"),
      ("laatikkoon","A",True,"laatikkoon"),
      ("aurinkoon","G",True,"aurinkoon"),("aurinkon","G",False,"auringon"),
      ("aurinkossa","G",False,"auringossa"),("aurinkoja","G",False,"aurinkoja"),
      ("takkin","A",False,"takin"),("takkiin","A",True,"takkiin"),
      ("pakon","D",False,"paon"),("sukun","M",False,"suvun"),("sopun","E",False,"sovun"),
      ("satun","F",False,"sadun"),("iltan","I",False,"illan"),("iltaan","I",True,"iltaan"),
      ("henton","J",False,"hennon"),("virtan","K",False,"virran"),
      ("kumpin","H",False,"kummin"),("arkin","L",False,"arjin"),("kaappin","B",False,"kaapin"),
    ]
    bad=0
    for form,av,ill,exp in tests:
        got=apply_gradation(form,av,is_illative=ill)
        if got!=exp: bad+=1; print(f"FAIL {form:<14}{av} ill={ill} -> {got}  expected {exp}")
    print(f"gradation: {len(tests)-bad}/{len(tests)} passed")
    print()
    for weakf, av, exp in [("rikaan","A","rikkaan"),("opaan","B","oppaan"),
                           ("porraan","K","portaan"),("kateen","C","katteen"),
                           ("sivellimen","I","siveltimen"),("aikeen","D",None)]:
        got, ok = strengthen(weakf, av)
        print(("ok  " if (got==exp or (exp is None and not ok)) else "FAIL"),
              f"strengthen {weakf:<12}{av} -> {got}  ok={ok}  expected {exp}")
