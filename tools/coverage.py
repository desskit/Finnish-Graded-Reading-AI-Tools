#!/usr/bin/env python3
"""Grade a draft lesson against what Jacob ACTUALLY knows.

Supersedes the deck.py that indexed All Decks.txt. That file lists every note
regardless of study state, so it counted never-studied words as known. This
builds the index from the .colpkg and labels every surface form with the tier
of its note (see anki.py):

  A          mature recognition card (>=21d)      -> known
  B          young recognition card (<21d)         -> probably known
  C-taught   never shown by Anki, but from a course deck Jacob worked through
             in class or another app                -> probably known
  C-backlog  never shown by Anki, from a genuine backlog deck -> unknown
  D          absent from the collection             -> genuinely new

Two coverage figures are reported:
  strict   A+B            — what Anki alone can vouch for
  working  A+B+C-taught   — the honest estimate, and the one to steer by
The gap between them is Anki bookkeeping, not knowledge.

Usage:
    COLPKG=/path/to/collection.colpkg python3 coverage.py draft.txt
"""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anki import load
from decline import full_paradigm, realise
from conjugate import conjugate
from function_words import FUNCTION_WORDS

WORD_RE = re.compile(r"[A-Za-zÅÄÖåäö]+(?:'[A-Za-zÅÄÖåäö]+)?")
TIER_RANK = {"A": 0, "B": 1, "C-taught": 2, "C-backlog": 3, "D": 4}

def _verb_forms(w):
    d = conjugate(w)
    if d.get("status") != "ok":
        return []
    f = {k: v.split()[0].strip("()") for k, v in d["forms"].items()}
    h = d["harmony"]
    out = set(f.values())
    p1 = f.get("pres 1sg", "")
    if p1.endswith("n"):
        st = p1[:-1]
        out |= {st + x for x in ("n", "t", "mme", "tte")} | {st}
    for base in ("cond 3sg", "past 3sg"):
        b = f.get(base, "")
        if b:
            out |= {b + x for x in ("", "n", "t", "mme", "tte",
                                    "vät" if h == "front" else "vat")}
    nut = f.get("NUT-part", "")
    if nut.endswith(("ut", "yt")):
        out.add(nut[:-2] + "eet")
    pp = f.get("pass past", "")
    m = re.match(r"^(.*?)(t+)(ii)n$", pp)
    if m:
        out.add(m.group(1) + m.group(2) + ("ä" if h == "front" else "a") + "isiin")
    if p1.endswith("n"):
        st = p1[:-1]
        ma = "mä" if h == "front" else "ma"
        out |= {st + ma + x for x in (realise("An", h), realise("AssA", h),
                                      realise("AstA", h), realise("AllA", h))}
    return [x for x in out if x]

def build_index(recs):
    idx, stats = {}, collections.Counter()
    # single-word notes first, so a phrase card cannot downgrade a word that has
    # its own note; and within each pass the STRONGEST tier wins.
    singles = [r for r in recs if " " not in r["front"] and "-" not in r["front"]]
    phrases = [r for r in recs if r not in singles]
    for r in phrases:
        for tok in WORD_RE.findall(r["front"].lower()):
            if tok not in idx or TIER_RANK[r["tier"]] < TIER_RANK[idx[tok]]:
                idx[tok] = r["tier"]
        stats["phrase"] += 1
    for r in singles:
        fi, tier = r["front"], r["tier"]
        w = fi.lower()
        forms = [w]
        isverb = bool(re.match(r"^to\s", r["back"].lower()))
        if isverb:
            forms += _verb_forms(w)
        if len(forms) <= 1:
            d = full_paradigm(w)
            if d.get("status") == "ok":
                for _, s, p in d["paradigm"]:
                    forms += [x.strip("()") for x in (s + " " + p).split()]
                h = d["harmony"]
                nsa = "nsa" if h == "back" else "nsä"
                for base in (d.get("strong_stem"), d.get("sg_stem"), d.get("pl_stem")):
                    if base:
                        forms += [base + s for s in ("ni", "si", nsa, "mme", "nne")]
        stats[tier] += 1
        for v in forms:
            v = v.lower()
            if v and v != "—":
                # a form claimed by two notes takes the STRONGER tier
                if v not in idx or TIER_RANK[tier] < TIER_RANK[idx[v]]:
                    idx[v] = tier
    return idx, stats

def grade(text, idx):
    toks = [t.lower() for t in WORD_RE.findall(text)]
    per = collections.Counter()
    unknown = collections.defaultdict(list)
    for t in toks:
        tier = "A" if t in FUNCTION_WORDS else idx.get(t, "D")
        per[tier] += 1
        if tier in ("C-taught", "C-backlog", "D"):
            unknown[tier].append(t)
    n = len(toks) or 1
    sents = [s.strip() for s in re.split(r"[.!?…]+", text) if s.strip()]
    lens = [len(WORD_RE.findall(s)) for s in sents]
    return {"tokens": len(toks), "per": per,
            "coverage_strict": 100.0 * (per["A"] + per["B"]) / n,
            "coverage_working": 100.0 * (per["A"] + per["B"] + per["C-taught"]) / n,
            "unknown_Ct": sorted(set(unknown["C-taught"])),
            "unknown_Cb": sorted(set(unknown["C-backlog"])),
            "unknown_D": sorted(set(unknown["D"])),
            "sentences": len(sents),
            "mean_len": sum(lens) / len(lens) if lens else 0,
            "max_len": max(lens) if lens else 0}

if __name__ == "__main__":
    col = os.environ.get("COLPKG", "")
    if not col:
        print("set COLPKG=/path/to/collection.colpkg"); sys.exit(1)
    recs = load(col)
    idx, stats = build_index(recs)
    print(f"surface forms indexed: {len(idx)}")
    print(f"  A={stats['A']} B={stats['B']} C-taught={stats['C-taught']} "
          f"C-backlog={stats['C-backlog']} phrases={stats['phrase']}")
    if len(sys.argv) > 1:
        r = grade(open(sys.argv[1], encoding="utf-8").read(), idx)
        p = r["per"]
        print(f"\ntokens {r['tokens']}")
        n = r["tokens"]
        for k, lab in (("A", "A mature"), ("B", "B young"),
                       ("C-taught", "C-taught (Anki gap)"),
                       ("C-backlog", "C-backlog (unknown)"),
                       ("D", "D not in collection")):
            print(f"  {lab:<24}{p[k]:>4}  {100*p[k]/n:5.1f}%")
        print(f"\n  COVERAGE strict  (A+B)          = {r['coverage_strict']:.1f}%")
        print(f"  COVERAGE working (A+B+C-taught) = {r['coverage_working']:.1f}%"
              f"   <- steer by this; target 95-98%")
        print(f"  sentences {r['sentences']}  mean {r['mean_len']:.1f}  max {r['max_len']}")
        print(f"\n  C-taught (Anki gap, probably fine): {', '.join(r['unknown_Ct'])}")
        print(f"\n  C-backlog (TREAT AS UNKNOWN): {', '.join(r['unknown_Cb'])}")
        print(f"\n  D (not in collection): {', '.join(r['unknown_D'])}")
