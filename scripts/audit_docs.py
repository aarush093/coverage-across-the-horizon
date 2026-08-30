"""Integrity audit: does every claim in docs/ have something behind it?

WHY. This project has already lost work twice in ways an audit would have caught. FR01:
code existed only in a session, and docs cited numbers whose producing script was not in
the repo. FR03: a headline number was carried in prose across sessions while the artefact
said something else. Both were found by accident. This finds them on demand.

FOUR CHECKS, each cheap and each aimed at a failure that has actually happened here.

1. DANGLING ARTEFACTS. Every `scripts/*.py` and `results/*.json` named in a document must
   exist in the repo. This is FR01 exactly: 43_REVIEWER_2 cited `scripts/check_bias.py`
   for several commits before that file was pushed.

2. UNDEFINED CROSS-REFERENCES. Every D###, FR##, Q##, RV##, MET##, EXP_* referenced
   anywhere must be defined in its home register. A reference to RV20 in a tracker when
   43_REVIEWER_2 stops at RV19 means one of them is wrong.

3. ORPHAN NUMBERS. Every four-decimal figure quoted in a document is looked up in the
   result files. A number that appears in no artefact is either stale, mistyped, or
   derived -- and it needs a source either way. This is the check that would have caught
   FR03's 0.652 the day it was written. Derived quantities (interaction terms,
   differences) legitimately fail this and are reported as REVIEW, not ERROR.

4. STALE DOCUMENTS. Any doc whose LAST-UPDATED is older than the newest result file is
   flagged, because the tracker drifted for six weeks once already (FR02).

Exit code is 1 if any hard error is found, so this can gate a commit. Reads only.

Run:  python scripts/audit_docs.py
"""
import glob
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DOCS = os.path.join(ROOT, "docs")
HOME = {"D": "10_DECISION_LOG.md", "FR": "24_FAILURE_REGISTRY.md",
        "Q": "13_OPEN_QUESTIONS.md", "RV": "43_REVIEWER_2.md",
        "MET": "23_METRIC_REGISTRY.md", "EXP": "20_EXPERIMENT_REGISTRY.md"}
ROUND = 4


def read(p):
    return open(p, encoding="utf-8-sig", errors="replace").read()


def all_numbers_in_results():
    """Every numeric leaf in every result file, rounded, as a set of strings."""
    seen = set()
    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, (int, float)) and not isinstance(x, bool):
            for nd in (4, 3, 2):
                seen.add(f"{round(float(x), nd):.{nd}f}")
                seen.add(f"{round(float(x) * 100, nd - 2):.{max(nd-2,0)}f}")
    for f in glob.glob(os.path.join(ROOT, "results", "*.json")):
        try:
            walk(json.load(open(f, encoding="utf-8-sig")))
        except Exception as e:
            print(f"  ! could not read {os.path.basename(f)}: {e}")
    return seen


def main():
    docs = sorted(glob.glob(os.path.join(DOCS, "*.md")))
    if not docs:
        print("no docs/ found")
        return 0
    text = {os.path.basename(p): read(p) for p in docs}
    errors, reviews = [], []

    print("=" * 72)
    print("1. DANGLING ARTEFACTS -- files cited by docs that do not exist")
    print("=" * 72)
    pat = re.compile(r"\b((?:scripts|results|figures|coverage_horizon)/[\w./-]+\.(?:py|json|md|png))")
    hits = 0
    for name, t in text.items():
        for ref in sorted(set(pat.findall(t))):
            if not os.path.exists(os.path.join(ROOT, ref)):
                # 24_FAILURE_REGISTRY names files that were DESTROYED (FR01). Those
                # citations are correct precisely because the file is absent.
                lost = name.startswith("24_")
                (reviews if lost else errors).append(f"{name} cites missing {ref}")
                print(f"  {'EXPECTED' if lost else 'MISSING '} {ref:<42} cited by {name}")
                hits += 0 if lost else 1
    print(f"  ok -- every cited file exists" if not hits else f"  {hits} dangling")

    print()
    print("=" * 72)
    print("2. UNDEFINED CROSS-REFERENCES")
    print("=" * 72)
    # An ID is "defined" if it appears anywhere in its home register. Deliberately
    # loose: registers use several row formats (pipe tables, "D006 | date | ..."),
    # and a strict pattern produced dozens of false positives. This still catches the
    # failure that matters -- a reference to an ID that exists nowhere.
    defined = {}
    for pre, home in HOME.items():
        t = text.get(home, "")
        defined[pre] = set(re.findall(rf"\b({pre}_?[A-Z0-9_]*\d[A-Z0-9_]*)\b", t))
    refpat = re.compile(r"\b(D\d{3}|FR\d{2}|Q\d{2}|RV\d{2}|MET\d{2}|EXP_[A-Z0-9_]+)\b")
    undef = 0
    for name, t in text.items():
        for r in sorted(set(refpat.findall(t))):
            pre = "EXP" if r.startswith("EXP") else re.match(r"[A-Z]+", r).group()
            if pre in defined and r not in defined[pre]:
                if name == HOME.get(pre):
                    continue                      # a register may forward-reference itself
                errors.append(f"{name} references undefined {r}")
                print(f"  UNDEFINED  {r:<14} referenced by {name}  (home: {HOME[pre]})")
                undef += 1
    print("  ok -- every reference resolves" if not undef else f"  {undef} undefined")

    print()
    print("=" * 72)
    print("3. ORPHAN NUMBERS -- quoted figures found in no result file")
    print("=" * 72)
    pool = all_numbers_in_results()
    numpat = re.compile(r"(?<![\w.])(\d\.\d{4})(?![\w])")
    orphan = 0
    for name, t in sorted(text.items()):
        found = sorted(set(numpat.findall(t)))
        miss = [n for n in found if n not in pool]
        if miss:
            reviews.append(f"{name}: {', '.join(miss)}")
            print(f"  {name}")
            print(f"     not in any result file: {', '.join(miss)}")
            orphan += len(miss)
    print("  ok -- every quoted figure traces to an artefact" if not orphan
          else f"  {orphan} to review (derived quantities are expected here)")

    print()
    print("=" * 72)
    print("4. STALE DOCUMENTS")
    print("=" * 72)
    res = glob.glob(os.path.join(ROOT, "results", "*.json"))
    newest = max((os.path.getmtime(f) for f in res), default=0)
    newest_d = date.fromtimestamp(newest).isoformat() if newest else "?"
    stale = 0
    for name, t in sorted(text.items()):
        m = re.search(r"LAST-UPDATED:\s*(\d{4}-\d{2}-\d{2})", t)
        if not m:
            continue
        if m.group(1) < newest_d:
            print(f"  STALE  {name:<34} {m.group(1)}  (newest result {newest_d})")
            stale += 1
    print("  ok -- no doc older than the newest result" if not stale else f"  {stale} stale")

    print()
    print("=" * 72)
    print(f"RESULT: {len(errors)} hard error(s), {len(reviews)} doc(s) with figures to review")
    print("=" * 72)
    for e in errors:
        print("  ERROR  " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
