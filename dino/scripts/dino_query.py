#!/usr/bin/env python3
"""Dotazy do CSV dumpu Crazy Dino Park (sloupce: scope,path,type,value). Jen stdlib."""
import argparse, csv, re, signal, sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "references" / "crazy-dino-park-values.csv"


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def top_key(row):
    m = re.match(r"^([^.\[]+(?:\.[^.\[]+)?)", row["path"])
    return m.group(1) if m else row["path"]


def cmd_summary(rows, _a):
    by_scope = Counter(r["scope"] for r in rows)
    print(f"Celkem řádků: {len(rows)}")
    for s, n in by_scope.most_common():
        print(f"\n[{s}] {n} řádků")
        keys = Counter(top_key(r) for r in rows if r["scope"] == s)
        for k, c in keys.most_common(15):
            print(f"  {c:5d}  {k}")
        if len(keys) > 15:
            print(f"  ... dalších {len(keys) - 15} klíčů")


def cmd_get(rows, a):
    rx = re.compile(a.pattern)
    n = 0
    for r in rows:
        if a.scope and r["scope"] != a.scope:
            continue
        if rx.search(r["path"]):
            print(f"{r['scope']}\t{r['path']}\t{r['type']}\t{r['value']}")
            n += 1
            if a.limit and n >= a.limit:
                print(f"... zkráceno na {a.limit} řádků (--limit 0 = bez limitu)", file=sys.stderr)
                break
    if n == 0:
        print("Nic nenalezeno.", file=sys.stderr)
        return 1


def cmd_cages(rows, _a):
    cages = defaultdict(lambda: {"dinos": defaultdict(dict)})
    for r in rows:
        if r["scope"] != "game-save":
            continue
        m = re.match(r"^save\._Cages\.(\w+)\.(.+)$", r["path"])
        if not m:
            continue
        cage, rest = m.groups()
        d = re.match(r"^_Dinos\[(\d+)\]\.(\w+)$", rest)
        if d:
            cages[cage]["dinos"][int(d.group(1))][d.group(2)] = r["value"].strip('"')
        else:
            cages[cage][rest] = r["value"].strip('"')

    def num(k):
        return int(re.sub(r"\D", "", k) or 0)

    print("cage\ttotal\tcageLvl\tdinoLevels\tspecial\tboosts(P/HP/Spd/Def)")
    for cage in sorted(cages, key=num):
        c = cages[cage]
        ds = [c["dinos"][i] for i in sorted(c["dinos"])]
        lv = ",".join(d.get("_Level", "?") for d in ds)
        sp = ",".join("S" if d.get("_Special") == "true" else "-" for d in ds)
        bo = ";".join("/".join(d.get(k, "?") for k in ("_BoostPower", "_BoostHP", "_BoostSpeed", "_BoostDefense")) for d in ds)
        print(f"{cage}\t{c.get('_TotalDinosNo','?')}\t{c.get('_CurrentLevel','?')}\t{lv}\t{sp}\t{bo}")
        # kontrola konzistence
        if c.get("_TotalDinosNo", "").isdigit() and int(c["_TotalDinosNo"]) < len(ds):
            print(f"  ! {cage}: _TotalDinosNo={c['_TotalDinosNo']} je menší než počet _Dinos[]={len(ds)}", file=sys.stderr)


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL) if hasattr(signal, "SIGPIPE") else None  # umožní '| head'
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", default=str(DEFAULT_CSV), help="cesta k CSV dumpu")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary")
    g = sub.add_parser("get")
    g.add_argument("pattern", help="regex nad sloupcem path")
    g.add_argument("--scope", choices=["game-save", "wardrobe-save", "local-json", "local-pref"])
    g.add_argument("--limit", type=int, default=200)
    sub.add_parser("cages")
    a = ap.parse_args()
    rows = load(a.csv)
    sys.exit({"summary": cmd_summary, "get": cmd_get, "cages": cmd_cages}[a.cmd](rows, a) or 0)


if __name__ == "__main__":
    main()
