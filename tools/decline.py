#!/usr/bin/env python3
"""Derive Finnish nominal paradigms by ALIGNMENT to the Kotus model word.

Method (deliberately not "generation from pattern memory"):
  1. Look the word up in the Kotus word list  -> inflection type + gradation class.
  2. Take that type's model paradigm VERBATIM from Kotus.
  3. Strip the invariant prefix shared by the model's own forms; what remains
     is the type's suffix material, stored archiphonemically (A = a/ä, O = o/ö,
     U = u/y) so it can be re-harmonised.
  4. Substitute the target word's stem, realise the suffix under the target's
     own vowel harmony.
  5. Apply consonant gradation phonologically (gradation.py).
Anything that cannot be aligned is reported, not guessed.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kotus_lookup import lookup, _dedupe
from gradation import apply_gradation, strengthen

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = json.load(open(os.path.join(HERE, "kotus_models.json"), encoding="utf-8"))
SLOTS = ["sg nom","sg gen","sg part","sg illat","pl nom","pl gen","pl part","pl illat"]
ILLATIVE_SLOTS = {"sg illat", "pl illat"}   # the illative never takes the weak grade

# Types whose NOMINATIVE SG carries the weak grade (inverse / käänteinen
# astevaihtelu): the strong grade appears in the inflected (vowel) stem.
INVERSE_TYPES = {32,33,34,35,36,37,41,43,44,45,46,47,48,49}
# Of those, the ones whose nominative ends in a consonant: any variant that
# still begins with the full nominative is a consonant-stem form and stays weak
# (kytkin : kytkimen but kytkinten;  onneton : onnettoman but onnetonten).
CONS_NOM_INVERSE = {32,33,34,35,36,37,41,43,44,45,46,47,49}
WEAK_SLOTS_INVERSE = {"sg nom", "sg part"}

BACK, FRONT = "aou", "äöy"
_ARCHI = {"a":"A","ä":"A","o":"O","ö":"O","u":"U","y":"U"}
_REAL  = {"back": {"A":"a","O":"o","U":"u"}, "front": {"A":"ä","O":"ö","U":"y"}}

def harmony(word):
    """Back/front from the last non-neutral vowel (handles compounds)."""
    w = word.lower()
    for ch in reversed(w):
        if ch in BACK:  return "back"
        if ch in FRONT: return "front"
    return "front"          # only e/i -> front by default (see caveat below)

def neutral_only(word):
    return not any(c in BACK + FRONT for c in word.lower())

def archi(s):
    return "".join(_ARCHI.get(c, c) for c in s)

def realise(s, h):
    m = _REAL[h]
    return "".join(m.get(c, c) for c in s)

def _lcp(strings):
    if not strings: return ""
    s1, s2 = min(strings), max(strings)
    i = 0
    while i < len(s1) and s1[i] == s2[i]: i += 1
    return s1[:i]

def model_parts(tn):
    m = MODELS.get(str(tn))
    return [f.split(": ", 1)[1] for f in m["forms"]] if m and m["forms"] else None

# Types 17-22 have a long vowel / diphthong at the stem end. Literal suffix
# alignment to the model fails there (maa vs kuu), so they get an explicit
# paradigm keyed on the stem's own final vowel.
LONGV_TYPES = {17: "seen", 18: "hVn", 20: "seen"}   # 19 (suo:soi-) aligns correctly to its model

# Type 41 (vieras) lengthens the vowel that precedes its final -s, and that
# vowel is part of the word, not the type: vieras : vieraan but kaunis : kauniin.
# Literal alignment to the model would give *kaunian, so type 41 is built here.
# Genuinely irregular lexemes, entered only with a checked source. meri has
# MIXED harmony: back in the singular consonant-stem forms (merta), front in the
# plural (meriä). No rule derives this, so it is stored, not computed.
# "h" is the harmony used to expand the remaining cases; forms listed here
# override it. meri is FRONT everywhere except the consonant-stem partitive
# singular merta (cf. meressä, merellä, merissä).
IRREGULAR = {
 # aika/poika: class-D gradation after an i-diphthong yields j, not zero
 # (aika : ajan, poika : pojan) -- but lika : lian and reikä : reiän do NOT.
 # No source consulted states the conditioning rule, so these are stored, not derived.
 # Verified against cooljugator.com/fin/aika and /fin/poika, 2026-08-20.
 "aika":  {"h": "back",
           "forms": {"sg nom": "aika", "sg gen": "ajan", "sg part": "aikaa",
                     "sg illat": "aikaan", "pl nom": "ajat", "pl gen": "aikojen",
                     "pl part": "aikoja", "pl illat": "aikoihin"}},
 "poika": {"h": "back",
           "forms": {"sg nom": "poika", "sg gen": "pojan", "sg part": "poikaa",
                     "sg illat": "poikaan", "pl nom": "pojat", "pl gen": "poikien",
                     "pl part": "poikia", "pl illat": "poikiin"}},
 "meri": {"h": "front",
          "forms": {"sg nom": "meri", "sg gen": "meren", "sg part": "merta",
                    "sg illat": "mereen", "pl nom": "meret",
                    "pl gen": "merien merten", "pl part": "meriä",
                    "pl illat": "meriin"}},
}

def _longvowel(w, tn_i, h):
    V = next((c for c in reversed(w) if c in "aeiouyäö"), None)
    if V is None:
        return None
    A = realise("A", h)
    plstem = w[:-1] + "i" if w[-1] in "aeiouyäö" else w + "i"
    illat = (w + "h" + V + "n") if LONGV_TYPES[tn_i] == "hVn" else (w + "seen")
    pl_illat = plstem + ("hin" if LONGV_TYPES[tn_i] == "hVn" else "siin")
    return {"sg nom": w, "sg gen": w + "n", "sg part": w + "t" + A,
            "sg illat": illat, "pl nom": w + "t",
            "pl gen": plstem + "den " + plstem + "tten",
            "pl part": plstem + "t" + A, "pl illat": pl_illat}


def derive(word, tn=None, av=None):
    w = word.strip().lower()
    matched, match_kind = w, "given"
    if tn is None:
        r = _dedupe(lookup(w))[0]
        if r["match"] == "unknown" or not r["type"]:
            return {"word": word, "status": "NOT IN KOTUS LIST — verify manually"}
        tn, av = r["type"], r["gradation"]
        matched, match_kind = r["matched_on"], r["match"]
    tn_i = int(tn)
    if not 1 <= tn_i <= 51:
        return {"word": word, "type": tn, "status": "not a nominal type"}
    if tn_i == 99:
        return {"word": word, "type": tn, "status": "indeclinable"}
    forms = model_parts(tn)
    if not forms:
        return {"word": word, "type": tn, "status": "no model paradigm"}

    if w in IRREGULAR:
        irr = IRREGULAR[w]
        return {"word": word, "type": tn, "gradation": "", "model": "(irregular)",
                "match": match_kind, "matched_on": matched, "inverse": False,
                "harmony": irr["h"], "neutral_only": neutral_only(w),
                "flags": ["irregular lexeme — principal parts are stored from a "
                          "checked source, not derived"],
                "status": "ok", "forms": dict(irr["forms"])}
    h0 = harmony(w)
    if tn_i == 41 and len(w) > 2 and w[-1] == "s" and w[-2] in "aeiouyäö":
        A = realise("A", h0)
        base = w[:-1] + w[-2]                        # viera+a, kauni+i
        if av:
            base, okk = strengthen(base, av, stem_len=len(base))
        pl = base[:-1] + "i"
        return {"word": word, "type": tn, "gradation": av, "model": "vieras",
                "match": match_kind, "matched_on": matched, "inverse": True,
                "harmony": h0, "neutral_only": neutral_only(w),
                "flags": ([] if not av or okk else
                          [f"could not place the strong grade (class {av}) — check by hand"]),
                "status": "ok",
                "forms": {"sg nom": w, "sg gen": base + "n", "sg part": w + "t" + A,
                          "sg illat": base + "seen", "pl nom": base + "t",
                          "pl gen": pl + "den " + pl + "tten",
                          "pl part": pl + "t" + A, "pl illat": pl + "siin"}}
    if tn_i in LONGV_TYPES:
        f2 = _longvowel(w, tn_i, h0)
        if f2:
            return {"word": word, "type": tn, "gradation": av,
                    "model": model_parts(tn)[0], "match": match_kind,
                    "matched_on": matched, "inverse": False, "harmony": h0,
                    "neutral_only": neutral_only(w), "flags": [], "status": "ok",
                    "forms": f2}
    if tn_i == 50:                       # compound: only the head inflects
        head = _dedupe(lookup(w))[0].get("matched_on") or ""
        for i in range(1, len(w) - 1):
            tail = w[i:]
            r2 = _dedupe(lookup(tail))[0]
            if r2["match"] == "exact" and r2["type"] and int(r2["type"]) != 50:
                d2 = derive(tail)
                if d2.get("status") == "ok":
                    pre = w[:i]
                    return dict(d2, word=word, type=f"50 (head '{tail}' = {d2['type']})",
                                forms={k: " ".join(pre + x for x in v.split())
                                       for k, v in d2["forms"].items()})
        return {"word": word, "type": tn,
                "status": "type 50 compound — head not resolvable; check by hand"}
    if tn_i == 51:
        return {"word": word, "type": tn,
                "status": "type 51 — BOTH parts inflect (nuoripari : nuorenparin); derive by hand"}

    prim = [f.split()[0].strip("()") for f in forms]
    lcp  = _lcp(prim)
    align_a = archi(prim[0][len(lcp):])          # model nominative's suffix, archiphonemic
    h = harmony(w)
    align = realise(align_a, h)
    if align and not w.endswith(align):
        # (a) type 19 also covers the ie-diphthong (tie : teiden), which no
        #     harmony mapping reaches from the model suo.
        if tn_i == 19 and w.endswith("ie"):
            st = w[:-2]
            return {"word": word, "type": tn, "gradation": av, "model": prim[0],
                    "match": match_kind, "matched_on": matched, "inverse": False,
                    "harmony": h, "neutral_only": neutral_only(w), "flags": [],
                    "status": "ok",
                    "forms": {"sg nom": w, "sg gen": w+"n", "sg part": w+"tä",
                              "sg illat": w+"hen", "pl nom": w+"t",
                              "pl gen": st+"eiden "+st+"eitten",
                              "pl part": st+"eitä", "pl illat": st+"eihin"}}
        # (b) plurale tantum (markkinat, hautajaiset): Kotus gives the SINGULAR
        #     type; rebuild the singular, then report the plural half.
        pl_suffix = prim[4][len(lcp):]
        pl_suffix = realise(archi(pl_suffix), h)
        if w.endswith(pl_suffix) and pl_suffix:
            sg = w[:len(w) - len(pl_suffix)] + align
            d2 = derive(sg, tn=tn, av=av)
            if d2.get("status") == "ok":
                d2["word"] = word
                d2.setdefault("flags", []).append(
                    f"PLURALE TANTUM — dictionary form is plural; the singular "
                    f"'{sg}' is listed above for reference but is not normally used")
                return d2
        # (c) consonant-final loanword given a vowel-stem type (golf : golfin):
        #     the stem vowel is simply added before every ending.
        if w[-1] not in "aeiouyäö" and align and align[-1] in "aeiouyäö":
            d2 = derive(w + align, tn=tn, av=av)
            if d2.get("status") == "ok":
                d2["forms"]["sg nom"] = w
                d2["word"] = word
                d2.setdefault("flags", []).append(
                    f"consonant-final stem: the type-{tn} stem vowel -{align} is "
                    f"inserted before every ending")
                return d2
        return {"word": word, "type": tn, "gradation": av,
                "status": f"CANNOT ALIGN to model '{prim[0]}' (expects ending -{align})"}
    stem = w[:len(w) - len(align)] if align else w
    inverse = tn_i in INVERSE_TYPES

    out, flags = {}, []
    for slot, f in zip(SLOTS, forms):
        parts = []
        for v in f.split():
            paren = v.startswith("(")
            v = v.strip("()")
            if not v.startswith(lcp):
                parts.append(("?" + v, paren)); continue
            suffix = realise(archi(v[len(lcp):]), h)
            built  = stem + suffix
            if inverse:
                keep_weak = (slot in WEAK_SLOTS_INVERSE) or (
                    tn_i in CONS_NOM_INVERSE and built.startswith(w))
                # If the model's own suffix material already supplies the
                # strong grade at the stem/suffix junction (onneton : onnet+toman),
                # concatenation has produced it -- do not double it again.
                already = False
                if av:
                    from gradation import PAIRS
                    sg = PAIRS[av][0]
                    j = built.find(sg, max(0, len(stem) - len(sg)), len(stem) + 1)
                    already = j >= 0
                if keep_weak or not av or already:
                    graded = built
                else:
                    graded, ok = strengthen(built, av, stem_len=len(stem))
                    if not ok:
                        graded = built + "(?)"
                        flags.append(f"{slot}: could not place the strong grade "
                                     f"(class {av}) — check by hand")
            else:
                graded = apply_gradation(built, av, stem_len=len(stem),
                                         is_illative=(slot in ILLATIVE_SLOTS))
                if (av == "D" and graded != built and
                        stem[:len(stem)-1].endswith(("ai", "oi", "ui", "ei", "äi", "öi"))
                        and w not in IRREGULAR):
                    dflag = ("class-D gradation after an i-diphthong: the weak "
                             "grade may be j (aika : ajan) or nothing "
                             "(reikä : reiän) — CHECK THIS FORM BY HAND")
                    if dflag not in flags:
                        flags.append(dflag)
            parts.append((graded, paren))
        out[slot] = " ".join(f"({x})" if p else x for x, p in parts)
    return {"word": word, "type": tn, "gradation": av, "model": prim[0],
            "match": match_kind, "matched_on": matched, "inverse": inverse,
            "harmony": h, "neutral_only": neutral_only(w), "flags": flags,
            "status": "ok", "forms": out}

def show(word):
    d = derive(word)
    if d.get("status") != "ok":
        return f"{word}: {d['status']}"
    head = (f"{word}  [Kotus {d['type']} ~ {d['model']}"
            + (f", gradation {d['gradation']}" if d["gradation"] else ", no gradation")
            + (", INVERSE" if d["inverse"] else "")
            + (f", via head '{d['matched_on']}'" if d["match"] == "compound" else "") + "]")
    lines = [head]
    for s in SLOTS:
        lines.append(f"    {s:<10} {d['forms'][s]}")
    for fl in d.get("flags", []):
        lines.append(f"    !! {fl}")
    if d["neutral_only"]:
        lines.append("    !! stem has only e/i — vowel harmony must be checked by hand")
    return "\n".join(lines)

if __name__ == "__main__":
    for w in sys.argv[1:]:
        print(show(w)); print()


# --------------------------------------------------------------------------
# Full 15-case paradigm, expanded from the four principal parts.
# The singular vowel stem is (genitive sg - n); the plural oblique stem is
# recovered from the plural illative. Grade for every slot is then decided
# phonologically by gradation.apply_gradation, not stipulated.
# --------------------------------------------------------------------------
# (name, ending, grade)  -- grade "w" = built on the weak/genitive stem,
# "s" = built on the strong/illative stem. Words with a Kotus gradation class
# get apply_gradation on top, which decides by syllable weight.
CASE_ENDINGS = [
 ("inessive", "ssA", "w"), ("elative", "stA", "w"), ("adessive", "llA", "w"),
 ("ablative", "ltA", "w"), ("allative", "lle", "w"), ("essive", "nA", "s"),
 ("translative", "ksi", "w"), ("abessive", "ttA", "w"),
]

def _plural_stem(pl_illat, sg_stem=""):
    """Plural oblique stem = everything up to and including the plural -i-.

    The plural illative ending is -hin, -in or -siin, which can be ambiguous
    (naisiin -> nai+siin or naisi+in). Resolve by preferring the candidate that
    shares more with the singular stem, then the shorter one.
    """
    v = pl_illat.split()[0].strip("()")
    cands = []
    for end in ("siin", "hin", "in"):
        if v.endswith(end):
            s = v[:-len(end)]
            if s.endswith("i"):
                cands.append(s)
    if not cands:
        return None
    def score(s):
        n = 0
        for a, b in zip(s, sg_stem):
            if a != b: break
            n += 1
        return (-n, len(s))
    return sorted(cands, key=score)[0]


def _strong_sg_stem(sg_illat):
    """The singular illative is always strong: -seen / -hVn / -Vn."""
    v = sg_illat.split()[0].strip("()")
    if v.endswith("seen"):
        s = v[:-4]
        # only a long-vowel stem takes -seen (hamee+seen); naise+en is not one
        if len(s) >= 2 and s[-1] == s[-2] and s[-1] in "aeiouyäö":
            return s
    if len(v) > 3 and v[-3] == "h": return v[:-3]
    return v[:-2] if len(v) > 2 else None

def full_paradigm(word):
    d = derive(word)
    if d.get("status") != "ok":
        return d
    f, av, h = d["forms"], d.get("gradation", ""), d["harmony"]
    inverse = d.get("inverse")
    gen = f["sg gen"].split()[0].strip("()")
    weak_stem   = gen[:-1] if gen.endswith("n") else None
    strong_stem = _strong_sg_stem(f["sg illat"]) or weak_stem
    pl_stem = _plural_stem(f["pl illat"], strong_stem or "")
    rows = [("nominative", f["sg nom"], f["pl nom"]),
            ("genitive",   f["sg gen"], f["pl gen"]),
            ("partitive",  f["sg part"], f["pl part"]),
            ("illative",   f["sg illat"], f["pl illat"])]
    for name, end, grade in CASE_ENDINGS:
        base = strong_stem if grade == "s" else weak_stem
        s = p = "—"
        if base:
            b = base + realise(end, h)
            s = b if inverse else apply_gradation(b, av, stem_len=len(base))
        if pl_stem:
            bp = pl_stem + realise(end, h)
            p = bp if inverse else apply_gradation(bp, av, stem_len=len(pl_stem))
        rows.append((name, s, p))
    order = ["nominative","genitive","partitive","inessive","elative","illative",
             "adessive","ablative","allative","essive","translative","abessive"]
    d["paradigm"] = sorted(rows, key=lambda r: order.index(r[0]))
    d["sg_stem"], d["strong_stem"], d["pl_stem"] = weak_stem, strong_stem, pl_stem
    return d

def show_full(word):
    d = full_paradigm(word)
    if d.get("status") != "ok":
        return f"{word}: {d['status']}"
    out = [f"{word}  [Kotus {d['type']} ~ {d['model']}"
           + (f", gradation {d['gradation']}" if d.get("gradation") else ", no gradation")
           + (", INVERSE" if d.get("inverse") else "") + "]",
           f"    stems: sg weak {d['sg_stem']} / sg strong {d['strong_stem']} / plural {d['pl_stem']}",
           f"    {'case':<12}{'singular':<26}plural"]
    for n, s, p in d["paradigm"]:
        out.append(f"    {n:<12}{s:<26}{p}")
    for fl in d.get("flags", []):
        out.append(f"    !! {fl}")
    return "\n".join(out)
