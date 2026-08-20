#!/usr/bin/env python3
"""Read an Anki .colpkg directly and report what Jacob actually knows.

The plain-text export lists every note regardless of study state, which makes
never-studied words look like known vocabulary. The collection package carries
the scheduler state, so knowledge can be measured instead of assumed.

A .colpkg is a zip holding `collection.anki21b`, a zstd-compressed SQLite file.
No zstd Python module is installable here, so libzstd is called through ctypes
(see zstd_ctypes.py).

Card directions: the "Basic (and reversed card)" note type makes two cards per
note. ord=0 is Finnish->English (RECOGNITION) and ord=1 is English->Finnish
(production). Graded reading is a recognition task, so ord=0 is what counts.

Tiers, keyed on the recognition card:
  A  mature      interval >= 21 days      -> assume known, do not gloss
  B  young       studied, interval < 21d  -> probably known, gloss if load-bearing
  C  unseen      never studied in Anki    -> split by deck, see below
  D  absent      not in the collection    -> genuinely new
  L  leech       >= 4 lapses (overlay)    -> deliberately recycle

"Never studied in Anki" does NOT mean "never learned". Jacob worked through the
Suomen Mestari books in class and in another app; some of those chapters were
simply never folded back into Anki review. So tier C is split by deck policy:

  C-taught   unstudied, but from a course deck he has actually worked through
             -> treat close to tier B: probably known, gloss only if the
                sentence turns on it
  C-backlog  unstudied, from a deck that is a genuine backlog (media words
             carded but never drilled) -> treat as unknown

DECK_POLICY below encodes which is which. It is Jacob-specific and he is the
authority on it — ask before assuming a new deck belongs in either group.
"""
import os, sys, zipfile, sqlite3, tempfile, collections, json, signal
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # allow piping into head
except (AttributeError, ValueError):
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zstd_ctypes import decompress

MATURE_DAYS = 21
LEECH_LAPSES = 4

# prefix -> policy for notes in that deck that Anki has never shown.
#   "taught"  = covered in class / another app; unstudied here is a bookkeeping
#               gap, not a knowledge gap  (confirmed by Jacob, 2026-08-20)
#   "backlog" = carded from media but never actually drilled
DECK_POLICY = [
    ("Suomen Mestari", "taught"),
    ("My Words",       "taught"),
    ("Ilman Sua",      "taught"),
    ("Harry Potter",   "backlog"),
    ("Animals",        "backlog"),
]
DEFAULT_POLICY = "backlog"          # unknown decks are assumed unlearned

def deck_policy(deck):
    for prefix, pol in DECK_POLICY:
        if deck.startswith(prefix):
            return pol
    return DEFAULT_POLICY

def open_colpkg(path):
    """Return (sqlite3.Connection, tmpdir). Handles both .anki21b and .anki2."""
    z = zipfile.ZipFile(path)
    names = z.namelist()
    tmp = tempfile.mkdtemp(prefix="colpkg_")
    if "collection.anki21b" in names:
        raw = z.read("collection.anki21b")
        db = os.path.join(tmp, "collection.sqlite")
        with open(db, "wb") as f:
            f.write(decompress(raw))
    elif "collection.anki21" in names:
        db = z.extract("collection.anki21", tmp)
    elif "collection.anki2" in names:
        db = z.extract("collection.anki2", tmp)
    else:
        raise RuntimeError(f"no collection database inside {path}")
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con, tmp

def load(path):
    """One record per note: front, back, deck, tier, interval, lapses, reps."""
    con, _ = open_colpkg(path)
    decks = {r["id"]: r["name"].replace("\x1f", "::")
             for r in con.execute("select id,name from decks")}
    out = []
    for r in con.execute("""
            select n.id nid, n.flds, c.did, c.type, c.queue, c.ivl,
                   c.factor, c.reps, c.lapses
            from notes n join cards c on c.nid = n.id and c.ord = 0"""):
        flds = r["flds"].split("\x1f")
        front = (flds[0] if flds else "").strip()
        back = (flds[1] if len(flds) > 1 else "").strip()
        if not front:
            continue
        deck = decks.get(r["did"], "?")
        if r["type"] == 0:
            tier = "C-taught" if deck_policy(deck) == "taught" else "C-backlog"
        elif r["type"] == 2 and r["ivl"] >= MATURE_DAYS:
            tier = "A"
        else:
            tier = "B"                      # young, learning or relearning
        out.append({"front": front, "back": back,
                    "deck": deck, "tier": tier,
                    "ivl": r["ivl"], "reps": r["reps"], "lapses": r["lapses"],
                    "leech": r["lapses"] >= LEECH_LAPSES,
                    "suspended": r["queue"] == -1})
    return out

def summary(recs):
    t = collections.Counter(r["tier"] for r in recs)
    n = len(recs)
    lines = [f"notes: {n}"]
    for k, label in (("A", "A mature   (>=21d, assume known)"),
                     ("B", "B young    (studied, <21d)"),
                     ("C-taught", "C-taught  (Anki gap, learned elsewhere)"),
                     ("C-backlog", "C-backlog (never actually learned)")):
        lines.append(f"  {label:<42}{t[k]:>5}  {100*t[k]/n:5.1f}%")
    lines.append(f"  {'leeches (>=4 lapses)':<42}{sum(r['leech'] for r in recs):>5}")
    known = t["A"] + t["B"]
    lines.append(f"  {'known for reading (A+B)':<42}{known:>5}  {100*known/n:5.1f}%")
    lines.append(f"  {'+ likely known (A+B+C-taught)':<42}"
                 f"{known+t['C-taught']:>5}  {100*(known+t['C-taught'])/n:5.1f}%")
    return "\n".join(lines)

def by_deck(recs):
    d = collections.defaultdict(collections.Counter)
    for r in recs:
        d[r["deck"]][r["tier"]] += 1
    rows = []
    for deck in sorted(d):
        c = d[deck]; t = sum(c.values())
        cu = c["C-taught"] + c["C-backlog"]
        rows.append((deck, t, c["A"], c["B"], cu, deck_policy(deck),
                     100*(c["A"]+c["B"])/t))
    return rows

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("COLPKG", "")
    if not path:
        print(__doc__); sys.exit(1)
    recs = load(path)
    print(summary(recs)); print()
    print(f"  {'deck':<26}{'total':>6}{'A':>6}{'B':>6}{'unseen':>8}"
          f"{'policy':>10}{'drilled%':>10}")
    for deck, t, a, b, cu, pol, pct in by_deck(recs):
        print(f"  {deck:<26}{t:>6}{a:>6}{b:>6}{cu:>8}{pol:>10}{pct:>9.1f}%")
    if "--leeches" in sys.argv:
        print("\nleeches (deliberate recycling targets):")
        for r in sorted((r for r in recs if r["leech"]), key=lambda r: -r["lapses"]):
            print(f"  {r['lapses']:>2} lapses  {r['front'][:30]:<32}{r['back'][:44]}")
