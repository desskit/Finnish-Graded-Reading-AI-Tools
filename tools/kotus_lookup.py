#!/usr/bin/env python3
"""
kotus_lookup.py -- authoritative Finnish inflection-type lookup.

Data: Kotimaisten kielten keskus (Institute for the Languages of Finland),
"Nykysuomen sanalista" v1 (2006), 94,110 entries, LGPL.
Each entry carries a Kotus inflection type number (tn) and, where relevant,
a consonant-gradation class (av).

Usage:
    python3 kotus_lookup.py sana [sana ...]
    python3 kotus_lookup.py --file words.txt
    from kotus_lookup import lookup, MODELS, GRADATION
"""
import os, sys, csv, json

HERE = os.path.dirname(os.path.abspath(__file__))
TSV  = os.path.join(HERE, "kotus.tsv")

# ---- Kotus model paradigms (verbatim from sanalistan-kuvaus.txt) -----------
# Nominals: sg nom, sg gen, sg part, sg illat, pl nom, pl gen, pl part, pl illat
# Verbs:    1st inf, pres 1sg, past 3sg, cond 3sg, pot 3sg, imper 3sg,
#           act past part (NUT), passive past
MODELS = json.load(open(os.path.join(HERE, "kotus_models.json"), encoding="utf-8")) \
         if os.path.exists(os.path.join(HERE, "kotus_models.json")) else {}

_TABLE = None
def _load():
    global _TABLE
    if _TABLE is not None:
        return _TABLE
    t = {}
    with open(TSV, encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            t.setdefault(row["word"], []).append(row)
    _TABLE = t
    return t

def lookup(word, allow_compound=True):
    """Return list of dicts describing the word's inflection type(s).

    'exact'    -- the word itself is in the Kotus list.
    'compound' -- only the final component is listed (Kotus omits the type
                  number for compounds whose head is listed separately);
                  the head's type governs the whole compound.
    'unknown'  -- not resolvable; DO NOT inflect from pattern memory.
    """
    t = _load()
    w = word.strip().lower()
    if not w:
        return []
    if w in t:
        out = [dict(r, match="exact", matched_on=w) for r in t[w]]
        if any(r["type"] for r in out):
            return out
        # listed but untyped => compound whose head is listed separately
        if not allow_compound:
            return out
    if allow_compound:
        # longest final component that is itself a listed, typed word
        for i in range(1, len(w) - 1):
            tail = w[i:]
            if len(tail) < 2:
                break
            if tail in t and any(r["type"] for r in t[tail]):
                return [dict(r, match="compound", matched_on=tail)
                        for r in t[tail] if r["type"]]
    return [{"word": w, "type": "", "gradation": "", "match": "unknown",
             "matched_on": ""}]

def _dedupe(res):
    seen, out = set(), []
    for r in res:
        k = (r.get("type"), r.get("gradation"), r.get("match"), r.get("matched_on"))
        if k in seen:
            continue
        seen.add(k); out.append(r)
    return out

def fmt(word):
    res = _dedupe(lookup(word))
    parts = []
    for r in res:
        if r["match"] == "unknown":
            parts.append("UNKNOWN -- verify manually before inflecting")
            continue
        m = MODELS.get(r["type"], {})
        model = m.get("model", "?")
        seg = f'type {r["type"]} ({model})'
        if r["gradation"]:
            seg += f' grad {r["gradation"]} [{GRADATION.get(r["gradation"],"?")}]'
        else:
            seg += " no gradation"
        if r["match"] == "compound":
            seg += f' <- head "{r["matched_on"]}"'
        for k, label in (("type_note", "type note"), ("grad_note", "grad note")):
            if r.get(k):
                seg += f' ({label}: {r[k]})'
        if m.get("forms"):
            seg += "\n      model paradigm: " + " | ".join(m["forms"])
        parts.append(seg)
    return f"{word}: " + "\n  ".join(parts)

GRADATION = {
 "A": "kk:k / k:kk",  "B": "pp:p / p:pp",  "C": "tt:t / t:tt",
 "D": "k:\u2013 / \u2013:k", "E": "p:v / v:p", "F": "t:d / d:t",
 "G": "nk:ng / ng:nk", "H": "mp:mm / mm:mp", "I": "lt:ll / ll:lt",
 "J": "nt:nn / nn:nt",  "K": "rt:rr / rr:rt", "L": "k:j / j:k",
 "M": "k:v / v:k",
}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(0)
    if args[0] == "--file":
        words = [l.strip() for l in open(args[1], encoding="utf-8") if l.strip()]
    else:
        words = args
    for w in words:
        print(fmt(w))
