---
name: dino
description: Referenční znalost o uložených datech hry Crazy Dino Park (Unity, Android) – struktura game-save, wardrobe-save, local-json a PlayerPrefs, význam klíčů (_CoinsNo, _BillsNo, _StonesNo, _Cages, _Chests, _LocationsData, _DiscoveredIDs ...) katalog upravitelných hodnot a editor jednotlivých hodnot savu (save editor). Použij vždy, když uživatel zmíní Crazy Dino Park, dino park, dino save, crazy-dino-park-values.csv, hodnoty/klíče savu, hledání nebo analýzu položek ve savu, úpravu/editaci hodnot ve hře (mince, bankovky, kameny, kosti, dinosové, boosty, odemčené funkce) – i když výslovně neřekne "skill dino".
---

# Crazy Dino Park – data uložené hry

Skill popisuje strukturu a význam hodnot ve výpisu `references/crazy-dino-park-values.csv`
(7 159 řádků, sloupce `scope,path,type,value`). Citlivé hodnoty (ID, GUID, jméno hráče,
tokeny) jsou v dumpu nahrazeny `[REDACTED]` (type `redigováno`) – nikdy je nedoplňuj ani nehádej.

## Rychlý postup

1. Nejdřív zjisti, o co jde: čtení/analýza dumpu, nebo plánovaná úprava hodnot.
2. Pro dotazy nečti CSV celé (449 kB). Použij `scripts/dino_query.py`; pro úpravy hodnot `scripts/dino_edit.py`.
3. Strukturu a význam klíčů hledej v `references/save-schema.md`.
4. Význam označený "pravděpodobně" je odvozen z názvů a hodnot, ne z dokumentace hry – řekni to uživateli.

## Nástroj

```bash
python3 scripts/dino_query.py summary                 # počty řádků po scope a top-level klíčích
python3 scripts/dino_query.py get '_CoinsNo|_BillsNo' # regex nad path (výchozí scope: všechny)
python3 scripts/dino_query.py get '^save\._Cages\.Dino1\.' --scope game-save
python3 scripts/dino_query.py cages                   # tabulka klecí: dino ID, počet, level, boosty
python3 scripts/dino_query.py --csv /cesta/k/jinemu.csv summary
```

Skript používá jen standardní knihovnu Pythonu (běží i v Termuxu). Rychlý pohled bez Pythonu:
`grep -F 'save._CoinsNo' references/crazy-dino-park-values.csv`.

## Editor hodnot (hlavní use-case)

Katalog všech upravitelných hodnot s aktuálními hodnotami z dumpu: `references/editable-values.md`
(vygenerováno `python3 scripts/dino_edit.py catalog`). Obsahuje měny, čítače, odemčené funkce, kosti,
dinosy (Level/Special/Boosty), klece, vozidla, vylepšení jídla, Multidig zdroje a šatník.

```bash
python3 scripts/dino_edit.py show '_CoinsNo|_BillsNo'                # co je v dumpu
python3 scripts/dino_edit.py patch save.json --dry-run \
    --set 'save._CoinsNo=1000000' --set 'save._Cages.Dino1._Dinos[0]._BoostPower=50'
python3 scripts/dino_edit.py patch save.json --set 'save._FbLiked=false' -o save.new.json
```

`patch` pracuje s **původním JSON souborem savu** (ne s CSV): hodnota je JSON literál (`true`, `42`, `"text"`),
cesta musí v souboru existovat (`--allow-new` jen vědomě), typ musí odpovídat původnímu, int nad int32 se odmítne,
chráněné klíče (ID, GUID, `_Valid3`, `_ValStat`, `ValidStatus`, hashe, tokeny) se neupraví. Úpravy se aplikují
všechny, nebo žádná; při přepisu stejného souboru vznikne záloha `*.bak-<čas>`. Skript je otestován jen na
JSON rekonstruovaném z dumpu – skutečný formát souboru (kódování, případné šifrování/obálka) je potřeba ověřit
na originálu; pokud soubor JSON není, skript ho nezpracuje a je nutné nejdřív zjistit formát.
Nepodporováno: `local-pref` (Unity PlayerPrefs XML) a `local-json`/`wardrobe-save` jsou jiné soubory – u wardrobe
funguje `patch` na jeho JSON stejně (kořen `save_1.`).

## Scope (4 zdroje dat)

| scope | co to je | řádků |
|---|---|---|
| `game-save` | hlavní save, kořen `save.` (verze formátu `_SaveVersion` = 2.32) | 6 764 |
| `wardrobe-save` | šatník dinosů, kořen `save_1.` | 84 |
| `local-json` | lokální JSON: `SummaryFullDinoMarkerCounter`, `PhotoBoothSaveData[]` | 243 |
| `local-pref` | Unity PlayerPrefs (hodnoty jsou v dumpu jako stringy v uvozovkách) | 68 |

## Pravidla pro práci s daty

- Cesta je zploštělý JSON: tečka = vnořený objekt, `[n]` = index pole. Klíče s mezerou
  (`trash SPECIAL 02`) a s URL-kódováním v `local-pref` (`%20`, `%2F`) jsou legitimní.
- Typy sleduj podle sloupce `type`; `NoneType` = `null`, `array`/`object` s hodnotou `[]`/`{}` = prázdný kontejner.
- Časy jsou stringy ve formátu `MM/DD/YYYY HH:MM:SS` (game-save `_ExitTime`, `_UnderConstructionTime`)
  nebo `M/D/YYYY h:mm:ss AM` (`_UpgradableTypesExitDate`, `_ExpeditionSuccessDate`); `_TimeStamp` je Unix čas.
- Duplicitní/aliasové klíče bez podtržítka (`NumCages`, `NumGoldenPickaxe`, `TournamentID`,
  `ArenaMultiplayerRating`, `MultidigLocal`, `WinterSantaLevel`, `ValidStatus`)
  zrcadlí `_`-varianty; při úpravě měň obě, jinak hra může hodnotu přepsat.

## Bezpečnost úprav

Dump je jen plochý výpis, který hra nečte; originály (cesty, název balíčku) v něm nejsou – zeptej se uživatele, nehádej.
Před zásahem vždy:
1. zálohovat originály,
2. neměnit `[REDACTED]` pole ani chráněné klíče (viz výše),
3. držet konzistenci čítačů (`_TotalDinosNo` nesmí být menší než počet `_Dinos[]`, `NumCages` = počet klecí,
   `Count`/`SumAll` u `_Items`, alias klíče bez podtržítka měnit spolu s `_` variantou),
4. upozornit, že PlayerPrefs mají kontrolní hash (`TimeStampHash`) a save pole `_Valid3`/`_ValStat`/`ValidStatus` –
   hra může změnu detekovat nebo save zahodit; online části (Arena multiplayer, žebříčky, Google Play Games sync)
   mohou být vázané na server a úprava je nemusí přežít.

## Údržba skillu

Když přibude nová verze dumpu (jiná `_SaveVersion`), porovnej `summary` s tímto popisem a
aktualizuj `references/save-schema.md`; nepřepisuj platné poznatky bez důkazu.

## Přenositelnost a ochrana dat
Spouštěj skripty přes dostupný Python 3 s cestou odvozenou od tohoto SKILL.md; pracovní adresář není garantován. Kontrola SIGPIPE je podmíněná kvůli Windows. Zálohy jsou unikátní i při více úpravách ve stejné sekundě a existující odlišný výstup se nepřepisuje. Editor neověřuje všechny herní invarianty automaticky; aliasy a čítače musíš zkontrolovat před zápisem. Nepoužívej jej na živém savu nebo serverových žebříčcích. V cestách CSV byly případné UUID nahrazeny konzistentními anonymními značkami; jde o referenční data, nikoli platné identifikátory originálního savu.
