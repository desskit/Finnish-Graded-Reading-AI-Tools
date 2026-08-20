#!/usr/bin/env python3
"""Finnish verb principal parts, derived by alignment to the Kotus model verb.

Same method as decline.py: Kotus gives eight principal parts for each of the
27 verb types (52-78); align the target to the model, re-harmonise, apply
gradation phonologically.

Note the conditional: it is built on the STRONG grade, unlike the 1sg present
(pitää : pidän but pitäisi; huutaa : huudan but huutaisi). That falls out of
the model paradigms rather than being stipulated here.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kotus_lookup import lookup, _dedupe
from decline import archi, realise, harmony, _lcp, MODELS, neutral_only
from gradation import apply_gradation, strengthen

# Verb types whose 1st INFINITIVE carries the weak grade (inverse gradation):
# the contracted -tA verbs.  tavata : tapaan,  levätä : lepään,  rohjeta : rohkenen
INVERSE_VERB_TYPES = {72, 73, 74, 75}
# ...and, for those, the slots built on the STRONG vowel stem.
INVERSE_STRONG_SLOTS = {"pres 1sg", "past 3sg", "cond 3sg"}
# Slots where the ending never triggers the weak grade is decided
# phonologically, so no list is needed for the direct types.

VSLOTS = ["1st inf","pres 1sg","past 3sg","cond 3sg","pot 3sg","imper 3sg",
          "NUT-part","pass past"]
PERSON = {"pres": ["-n","-t","-∅","-mme","-tte","-vat/-vät"]}

def _grade_verb(stem, suf, av):
    """Build stem+suffix in the strong grade, then let the syllable rule decide.

    The gradation site may sit in the stem (ottaa : otan), straddle the
    stem/suffix junction (ymmärtää : ymmärrän) or lie wholly in the suffix
    material (huutaa : huudan), so the search window is the stem plus one
    character. If the strong cluster is nowhere to be found the stem itself is
    in the weak grade (ajatella : ajattelen) and is strengthened first.
    """
    from gradation import PAIRS
    if not av or av not in PAIRS:
        return stem + suf
    strong, weak = PAIRS[av]
    form = stem + suf
    if form.rfind(strong, 0, len(stem) + 1) < 0 and weak:
        st2, okk = strengthen(stem, av, stem_len=len(stem))
        if okk:
            stem, form = st2, st2 + suf
    return apply_gradation(form, av, stem_len=len(stem) + 1)


def conjugate(word, tn=None, av=None):
    w = word.strip().lower()
    match_kind, matched = "given", w
    if tn is None:
        r = _dedupe(lookup(w))[0]
        if r["match"] == "unknown" or not r["type"]:
            return {"word": word, "status": "NOT IN KOTUS LIST — verify manually"}
        tn, av, match_kind, matched = r["type"], r["gradation"], r["match"], r["matched_on"]
    tn_i = int(tn)
    if not 52 <= tn_i <= 78:
        return {"word": word, "type": tn, "status": "not a verb type"}
    m = MODELS.get(str(tn))
    if not m or not m["forms"]:
        return {"word": word, "type": tn, "status": "no model paradigm"}
    forms = [f.split(": ", 1)[1] for f in m["forms"]]
    # The model verb may itself gradate (huutaa : huudan), which would bake the
    # WRONG class into the suffix material for a target of another class
    # (ymmärtää is rt:rr, not t:d). Undo the model's own gradation first.
    model_av = ""
    r0 = _dedupe(lookup(prim0 := forms[0].split()[0].strip("()")))
    for rr in r0:
        if rr.get("type") == str(tn) and rr.get("gradation"):
            model_av = rr["gradation"]; break
    if model_av:
        forms = [" ".join(strengthen(x.strip("()"), model_av)[0]
                          .join(("(", ")")) if x.startswith("(")
                          else strengthen(x, model_av)[0] for x in f.split())
                 for f in forms]
    prim = [f.split()[0].strip("()") for f in forms]
    lcp = _lcp(prim)
    h = harmony(w)
    align = realise(archi(prim[0][len(lcp):]), h)
    # Types 63/64: the stem vowel itself varies (saada/myydä; juoda/viedä),
    # which literal alignment cannot reach. Build them from the vowel directly.
    if tn_i == 63 and len(w) > 3 and w[-2] == "d" and w[-3] == w[-4]:
        st, V = w[:-4], w[-3]
        A = realise("A", h); O = realise("O", h)
        return {"word": word, "type": tn, "gradation": av, "model": prim[0],
                "match": match_kind, "matched_on": matched, "harmony": h,
                "neutral_only": neutral_only(w), "status": "ok",
                "forms": {"1st inf": f"{st}{V}{V}d{A}", "pres 1sg": f"{st}{V}{V}n",
                          "past 3sg": f"{st}{V}i", "cond 3sg": f"{st}{V}isi",
                          "pot 3sg": f"{st}{V}{V}nee",
                          "imper 3sg": f"{st}{V}{V}k{O}{O}n",
                          "NUT-part": f"{st}{V}{V}n{'yt' if h=='front' else 'ut'}",
                          "pass past": f"{st}{V}{V}t{'ii'}n"}}
    if tn_i == 64 and len(w) > 3 and w[-2] == "d" and w[-4:-2] in ("uo","yö","ie"):
        st, D = w[:-4], w[-4:-2]
        V2 = D[1]                       # juo->joi, syö->söi, vie->vei
        A = realise("A", h); O = realise("O", h)
        return {"word": word, "type": tn, "gradation": av, "model": prim[0],
                "match": match_kind, "matched_on": matched, "harmony": h,
                "neutral_only": neutral_only(w), "status": "ok",
                "forms": {"1st inf": f"{st}{D}d{A}", "pres 1sg": f"{st}{D}n",
                          "past 3sg": f"{st}{V2}i", "cond 3sg": f"{st}{V2}isi",
                          "pot 3sg": f"{st}{D}nee", "imper 3sg": f"{st}{D}k{O}{O}n",
                          "NUT-part": f"{st}{D}n{'yt' if h=='front' else 'ut'}",
                          "pass past": f"{st}{D}tiin"}}
    geminate = None
    if align and not w.endswith(align):
        # Type 67 (tulla) forms its infinitive by geminating the stem-final
        # consonant: tul+la, men+nä, pur+ra. Align on that consonant instead.
        if tn_i == 67 and len(w) > 3 and w[-2] == w[-3]:
            geminate, align = w[-2], w[-2:]
        else:
            return {"word": word, "type": tn,
                    "status": f"CANNOT ALIGN to model '{prim[0]}' (expects ending -{align})"}
    stem = w[:len(w)-len(align)] if align else w
    if tn_i == 67:
        geminate = geminate or (stem[-1] if stem else None)
    out = {}
    for slot, f in zip(VSLOTS, forms):
        vs = []
        for v in f.split():
            paren = v.startswith("(")
            v = v.strip("()")
            if not v.startswith(lcp):
                vs.append(("?"+v, paren)); continue
            suf = realise(archi(v[len(lcp):]), h)
            if geminate and suf[:1] == lcp[-1:]:      # tul|la -> men|nä, pur|ra
                suf = geminate + suf[1:]
            if tn_i in INVERSE_VERB_TYPES:
                # contracted -tA verbs: the strong/weak split is lexical, not
                # phonological (tapaan is strong though -paan is a closed syllable)
                built = stem + suf
                if slot in INVERSE_STRONG_SLOTS and av:
                    built, okk = strengthen(built, av, stem_len=len(stem))
                    if not okk:
                        built += "(?)"
            else:
                built = _grade_verb(stem, suf, av)
            vs.append((built, paren))
        out[slot] = " ".join(f"({x})" if p else x for x, p in vs)
    return {"word": word, "type": tn, "gradation": av, "model": prim[0],
            "match": match_kind, "matched_on": matched, "harmony": h,
            "neutral_only": neutral_only(w), "status": "ok", "forms": out}

def show(word):
    d = conjugate(word)
    if d.get("status") != "ok":
        return f"{word}: {d['status']}"
    head = (f"{word}  [Kotus {d['type']} ~ {d['model']}"
            + (f", gradation {d['gradation']}" if d.get("gradation") else ", no gradation")
            + (f", via head '{d['matched_on']}'" if d["match"] == "compound" else "") + "]")
    lines = [head] + [f"    {s:<10} {d['forms'][s]}" for s in VSLOTS]
    if d["neutral_only"]:
        lines.append("    !! stem has only e/i — check vowel harmony by hand")
    return "\n".join(lines)

if __name__ == "__main__":
    for w in sys.argv[1:]:
        print(show(w)); print()
