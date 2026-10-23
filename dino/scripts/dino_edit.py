#!/usr/bin/env python3
"""Editor jednotlivých hodnot savu Crazy Dino Park (jen stdlib).

  dino_edit.py catalog [--csv X]                      # katalog upravitelných hodnot + aktuální hodnoty z dumpu
  dino_edit.py show PATH_REGEX [--scope S]            # hodnoty z dumpu
  dino_edit.py patch FILE.json --set PATH=JSON ... [--edits e.json] [--allow-new] [--dry-run] [-o OUT]

patch pracuje s PŮVODNÍM JSON souborem savu (ne s CSV). Zálohuje, kontroluje existenci cesty
a shodu typu (int->int, bool->bool, str->str, null->cokoli), odmítá chráněné klíče (ID, GUID, hash, tokeny).
Hodnota v --set je JSON literál: --set 'save._CoinsNo=999999' --set 'save._PlayerChangedName=true'
"""
import argparse, csv, json, re, shutil, signal, sys, time
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "references" / "crazy-dino-park-values.csv"
PROTECTED = re.compile(r"(_Guid|_SaveId|_BranchId|_DinoId|_PlayerName|saveId|Login_|session|installation|token|Hash|_GUID$|_Valid3|_ValStat|ValidStatus|_TimeStamp$)", re.I)
INT32_MAX = 2147483647

# (skupina, regex nad path, poznámka)
GROUPS = [
    ("Měny a postup", r"^save\.(_CoinsNo|_BillsNo|_StonesNo|_LikesNo|_PiggyBank|_PiggyBankCollectedCoins|_BankLevel|_XPNum|_NumGoldenPickaxe|NumGoldenPickaxe|_FactoryResources\[0\]|_TicketBoothLevel)$",
     "int; strop pravděpodobně int32 (2 147 483 647). NumGoldenPickaxe je alias _NumGoldenPickaxe – měň obě."),
    ("Čítače a statistiky", r"^save\.(_GamesNoCounter|_IncubatedEggsNo|_DugBonesNo|_IncomeMax|_NumMultiplayerWins|_NumMultiplayerLost|_NumTournamentWins|NumTournamentWins|_ArenaMultiplayerRating|ArenaMultiplayerRating|_ArenaPlayerRank)$",
     "int; čistě statistiky, nižší riziko. Rating/Rank/Wins souvisí s online částí."),
    ("Odemčené funkce (bool)", r"^save\.\w+Unlocked$", "bool; true = odemčeno."),
    ("Kosti v truhlách", r"^save\._Chests\.\w+\._Bones\.", "int; počet kostí dané části (head/rib/small/extra). Rodina hodnot – viz šablona."),
    ("Dinosové – úroveň a boosty", r"^save\._Cages\.\w+\._Dinos\[\d+\]\._(Level|Special|BoostPower|BoostHP|BoostSpeed|BoostDefense)$",
     "Level v dumpu 1, 2, 3, 4, 6; Boost 0–50 (nad 50 neověřeno). Special bool. Rodina hodnot."),
    ("Klece", r"^save\._Cages\.\w+\._(CurrentLevel|GoldsNo|Ready|AutoShow|WasShown|NextEggCounter)$", "CurrentLevel v dumpu 2–3."),
    ("Vozidla", r"^save\._Vehicles(Ability|Buy)Counter\.", "int; Count/SumAll/_MaxSumAll u _Items drž konzistentní (SumAll = součet _Items)."),
    ("Vylepšení jídla", r"^save\._UpgradableTypesLevel\.", "int; v dumpu 5."),
    ("Multidig / Arena zdroje", r"^save\._(MultiDig2?(ToolsNo|PiggysNo|CoinsNo|GemsNo)|TrainingNumSpeedUps)$", "int."),
    ("Šatník (wardrobe-save)", r"^save_1\.m_vAvailableDecorations\.", "int; počet kusů dekorace (scope wardrobe-save, jiný soubor než game-save)."),
]
def norm(path):
    """Cesta -> šablona rodiny (DinoN, LocationN, [i], <druh>_<část>)."""
    n = re.sub(r"(Dino|Location|Vehicle)\d+", r"\1N", path)
    n = re.sub(r"\[\d+\]", "[i]", n)
    return re.sub(r"(_Bones\.)\w+_(head|rib|small|extra)$", r"\1<druh>_\2", n)


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_path(p):
    if not isinstance(p, str) or not re.fullmatch(r"[^.\[\]]+(?:\[\d+\]|\.[^.\[\]]+)*", p):
        raise ValueError("Neplatná nebo prázdná cesta")
    toks = []
    for m in re.finditer(r"\[(\d+)\]|([^.\[\]]+)", p):
        toks.append(int(m.group(1)) if m.group(1) is not None else m.group(2))
    return toks


def tname(v):
    return {bool: "bool", int: "int", float: "float", str: "str", type(None): "null", list: "array", dict: "object"}[type(v)]


def compatible(old, new):
    if old is None or new is None:
        return True
    if isinstance(old, bool) or isinstance(new, bool):
        return isinstance(old, bool) and isinstance(new, bool)
    if isinstance(old, (int, float)):
        return isinstance(new, (int, float)) and (isinstance(old, float) or isinstance(new, int))
    return type(old) is type(new)


def cmd_catalog(a):
    rows = [r for r in load(a.csv) if r["scope"] in ("game-save", "wardrobe-save")]
    used = set()
    print("# Katalog upravitelných hodnot (z dumpu)\n")
    for name, rx, note in GROUPS:
        r_ = re.compile(rx)
        hits = [r for r in rows if r_.search(r["path"]) and r["type"] != "redigováno"]
        if not hits:
            continue
        print(f"## {name}\n{note}\n")
        groups = {}
        for r in hits:
            used.add(r["path"])
            groups.setdefault(norm(r["path"]), []).append(r)
        for n, lst in groups.items():
            if len(lst) <= 3:
                for r in lst:
                    print(f"- `{r['path']}` ({r['type']}) = {r['value']}")
                continue
            vals = sorted({r["value"] for r in lst}, key=lambda x: (len(x), x))
            ex = lst[0]
            print(f"- šablona `{n}` – {len(lst)} hodnot, {ex['type']}; v dumpu: {', '.join(vals[:8])}{' …' if len(vals) > 8 else ''}; příklad `{ex['path']}`")
        print()
    prot = [r["path"] for r in rows if PROTECTED.search(r["path"])]
    print(f"## Chráněné (patch je odmítne) – {len(prot)} cest v dumpu, např.: " + ", ".join(f"`{p}`" for p in prot[:6]))


def cmd_show(a):
    rx = re.compile(a.pattern)
    for r in load(a.csv):
        if (not a.scope or r["scope"] == a.scope) and rx.search(r["path"]):
            print(f"{r['scope']}\t{r['path']}\t{r['type']}\t{r['value']}")


def walk(root, toks, create=False):
    """Vrátí (rodič, klíč) pro poslední token."""
    cur = root
    for t in toks[:-1]:
        if isinstance(t, int):
            if not isinstance(cur, list) or t >= len(cur):
                raise KeyError(f"index [{t}] neexistuje")
            cur = cur[t]
        else:
            if not isinstance(cur, dict) or t not in cur:
                if create and isinstance(cur, dict):
                    cur[t] = {}
                else:
                    raise KeyError(f"klíč '{t}' neexistuje")
            cur = cur[t]
    return cur, toks[-1]


def apply_edit(root, path, value, allow_new):
    if isinstance(value, int) and not isinstance(value, bool) and not (-2147483648 <= value <= INT32_MAX):
        raise ValueError("Hodnota přesahuje int32")
    if PROTECTED.search(path):
        raise ValueError("chráněný klíč (ID/GUID/hash/token) – neupravuji")
    toks = parse_path(path)
    # kořen: soubor může začínat 'save' nebo mít obsah rovnou uvnitř
    if toks and isinstance(root, dict) and toks[0] not in root and len(toks) > 1:
        if toks[0] in ("save", "save_1"):
            toks = toks[1:]
    parent, key = walk(root, toks, create=allow_new)
    exists = (isinstance(key, int) and isinstance(parent, list) and key < len(parent)) or (isinstance(key, str) and isinstance(parent, dict) and key in parent)
    if not exists:
        if not allow_new:
            raise KeyError("cesta v souboru neexistuje (použij --allow-new jen vědomě)")
        parent[key] = value
        return None, value
    old = parent[key]
    if not compatible(old, value):
        raise TypeError(f"typ {tname(value)} neodpovídá původnímu {tname(old)} ({json.dumps(old)})")
    if isinstance(value, int) and not isinstance(value, bool) and abs(value) > INT32_MAX:
        raise ValueError(f"{value} přesahuje int32 – hra (Unity/C#) pravděpodobně přeteče")
    parent[key] = value
    return old, value


def cmd_patch(a):
    src = Path(a.file)
    root = json.loads(src.read_text(encoding="utf-8"))
    edits = {}
    if a.edits:
        edits.update(json.loads(Path(a.edits).read_text(encoding="utf-8")))
    for s in a.set or []:
        p, _, v = s.partition("=")
        try:
            edits[p] = json.loads(v)
        except json.JSONDecodeError:
            sys.exit(f"Hodnota není platný JSON literál: {s} (řetězce dej do uvozovek: 'path=\"text\"')")
    if not edits:
        sys.exit("Žádné úpravy (--set / --edits).")
    ok = bad = 0
    for p, v in edits.items():
        try:
            old, new = apply_edit(root, p, v, a.allow_new)
            print(f"OK   {p}: {json.dumps(old)} -> {json.dumps(new)}")
            ok += 1
        except (KeyError, TypeError, ValueError) as e:
            print(f"FAIL {p}: {e}", file=sys.stderr)
            bad += 1
    if bad:
        sys.exit(f"{bad} úprav selhalo, nic nezapsáno (celé nebo žádné).")
    if a.dry_run:
        print(f"[dry-run] {ok} úprav by bylo zapsáno.")
        return
    out = Path(a.output) if a.output else src
    if out.exists() and out.resolve() != src.resolve():
        raise FileExistsError("Výstup již existuje; zvol novou cestu")
    if out.resolve() == src.resolve():
        bak = src.with_name(src.name + time.strftime(".bak-%Y%m%d-%H%M%S-") + str(time.time_ns()))
        shutil.copy2(src, bak)
        print(f"Záloha: {bak}")
    out.write_text(json.dumps(root, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    json.loads(out.read_text(encoding="utf-8"))  # kontrola platnosti
    print(f"Zapsáno {ok} úprav -> {out}")


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL) if hasattr(signal, "SIGPIPE") else None
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("catalog")
    s = sub.add_parser("show"); s.add_argument("pattern"); s.add_argument("--scope")
    p = sub.add_parser("patch"); p.add_argument("file"); p.add_argument("--set", action="append")
    p.add_argument("--edits"); p.add_argument("--allow-new", action="store_true")
    p.add_argument("--dry-run", action="store_true"); p.add_argument("-o", "--output")
    a = ap.parse_args()
    {"catalog": cmd_catalog, "show": cmd_show, "patch": cmd_patch}[a.cmd](a)


if __name__ == "__main__":
    main()
