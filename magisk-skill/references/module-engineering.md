# Magisk modul: struktura, instalátor, sestavení a ověření

Používej tento dokument spolu s aktuálními pravidly [Magisk Guides](https://topjohnwu.github.io/Magisk/guides.html). Pokud se zde informace liší od aktuálního upstreamu, řiď se upstreamem a popiš rozdíl.

## 1. Rozvržení projektu

Základní zdrojový adresář modulu má například tuto podobu:

```text
my-module/
├── module.prop              # povinné
├── customize.sh             # pouze je-li potřeba instalační logika
├── service.sh               # pouze je-li potřeba pozdní start
├── post-fs-data.sh          # pouze když je nutná raná blokující fáze
├── action.sh                # pouze pro tlačítko Action
├── uninstall.sh             # pouze pro vlastní cleanup
├── system/                  # soubory k systemless overlay, volitelné
├── system.prop               # systémové vlastnosti, volitelné
├── sepolicy.rule             # minimální policy pravidla, volitelné
└── zygisk/                   # ABI knihovny, pouze při implementaci Zygisk API
```

Nezahrnuj prázdné složky, placeholdery ani soubory, které modul nepotřebuje. `module.prop` musí být přímo v kořeni modulu.

## 2. Metadata a update JSON

Povinné položky: `id`, `name`, `version`, `versionCode`, `author`, `description`. Každá hodnota je na jednom řádku; `versionCode` je integer. Nepoužívej mezery v `id`; `id` po vydání neměň. `updateJson` je volitelný a musí ukazovat na existující JSON ve formátu vyžadovaném aktuální dokumentací Magisku. Pokud neexistuje hostovaný update endpoint, toto pole vynech.

## 3. Instalátor

- ZIP instalovaný přes aplikaci Magisk může obsahovat soubory modulu přímo. Obnovovací instalace potřebuje strukturu `META-INF/com/google/android/` s aktuálním upstream `module_installer.sh` přejmenovaným na `update-binary` a podporovaným `updater-script` (aktuálně konvenčně jediný řádek `#MAGISK`).
- Nekopíruj starý `update-binary` z náhodného repozitáře. Magisk Manager ho při některých instalačních cestách nahrazuje aktuálním instalátorem; nespoléhej na vlastní logiku uvnitř něj.
- `customize.sh` je shellový fragment, který installer načte. Nepoužívej `exit`; fatální stav ukonči podporovanou funkcí `abort`. `SKIPUNZIP=1` používej jen tehdy, když vlastní extrakce je nutná a plně implementovaná.
- Používej pouze proměnné/funkce dokumentované pro konkrétní cílovou Magisk verzi. Vlastnosti jako `MAGISK_VER`, `API`, `ARCH`, `MODPATH`, `TMPDIR`, `set_perm`, `REMOVE` a `REPLACE` předpokládej jen v odpovídající instalační fázi.

## 4. Boot skripty

| Soubor | Použití | Rozhodovací pravidlo |
|---|---|---|
| `post-fs-data.sh` | Před mountem modulů a před Zygote | Blokující. Jen nezbytné rychlé operace; nepoužívat `setprop`. |
| `service.sh` | Pozdní start po bootu | Preferovaná fáze pro většinu běžných úloh. Čekej na readiness jen pokud je to nutné, s limitem/timeoutem. |
| `action.sh` | Uživatelská akce z manageru | Musí být bezpečná při opakovaném spuštění; poskytnout jasný výstup. |
| `uninstall.sh` | Odinstalace | Čisti pouze soubory vytvořené modulem; neodstraňuj uživatelská data bez výslovného zadání. |

Každý skript začínej Android shell shebangem a odvozuj `MODDIR=${0%/*}`. Cituj proměnné v cestách, kontroluj návratové kódy a loguj jen potřebné údaje. Nevkládej tajné tokeny do skriptů/logů. Magisk `resetprop` ani shell builtiny nepředpokládej v libovolném externím shellu.

## 5. Systemless overlay a bezpečnost

- Cesty pod `system/` se mapují na Android systémový strom (např. `system/vendor/...`); ověř skutečný target/partition a souborovou cestu na cílovém Androidu.
- `.replace`, `REMOVE`, whiteout zařízení a změny vlastníka/SELinux kontextu mohou odstavit systémové komponenty. Preferuj přidání/úpravu jen nezbytných souborů; destruktivní přepis proveď pouze pokud zadání jasně požaduje tento efekt.
- `system.prop` používej jen pro deklarované vlastnosti; každá řádka je `key=value`. Zvaž, zda je vlastnost stále platná v aktuálním Androidu.
- `sepolicy.rule` obsahuje pouze úzká pravidla odpovídající konkrétním AVC chybám. Neřeš problém plošným povolením nebo vypnutím SELinuxu. Ověř syntaxi aktuálními nástroji (`magiskpolicy` dle dostupnosti) a analyzuj `dmesg`/audit logy.
- Pro Zygisk použij upstream API a build sample, odpovídající ABI (`arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64` dle cílení). Zkontroluj symboly, architekturu, linker závislosti a podporované NDK; nikdy nevydávej prázdnou `.so` za implementaci.

## 6. Vytvoření instalačního ZIPu

Obsah ZIPu má mít soubory modulu v archivu v kořeni, nikoli další složku projektu navíc. Příklad POSIX příkazu z adresáře projektu:

```sh
cd my-module
zip -r ../my-module.zip . -x '*/.git/*' '*/.DS_Store'
```

Při podpoře recovery přidej správnou `META-INF/...` strukturu. Zachovej execute bit runtime skriptů (`chmod 0755 *.sh`, jen pro existující skripty) a používej LF. Nepřidávej debug buildy, klíče, cache, `.git`, `local.properties` ani soukromé soubory.

## 7. Kontrolní seznam

1. `unzip -t module.zip` projde bez chyby.
2. `unzip -l` ukazuje `module.prop` v ZIP rootu a žádný nadbytečný obalový adresář.
3. `module.prop` splňuje regex `id`, celé `versionCode`, jednořádkové hodnoty a stabilní verzi.
4. JSON validuj parserem; shell skripty kontroluj `sh -n` a podle potřeby ShellCheck, ale ověř zvlášť Android/BusyBox kompatibilitu.
5. Zkontroluj LF (`file`, `dos2unix`/Python), režimy spustitelných skriptů a že ZIP neobsahuje tokeny ani nečekané binárky.
6. Pro změny systemless mountu, Zygisku, boot skriptů nebo SELinux pravidel nejprve testuj na záložním zařízení/emulátoru a měj připravenou recovery/safe-mode cestu. Před reálnou instalací nebo restartem respektuj uživatelův rozsah oprávnění.
7. Po startu ověř mounty, logcat/`dmesg`, záměrnou funkčnost i běžné funkce zařízení. Zaznamenej přesnou verzi manageru, Android API a architekturu.

## Zdroje

- [Magisk Guides: Modules, module.prop, Installer, boot scripts, Zygisk](https://topjohnwu.github.io/Magisk/guides.html)
- [Magisk Tools: magiskpolicy](https://topjohnwu.github.io/Magisk/tools.html)
- [Zygisk Module Sample](https://github.com/topjohnwu/zygisk-module-sample)
- [Magisk source and installer](https://github.com/topjohnwu/Magisk/blob/master/scripts/module_installer.sh)
