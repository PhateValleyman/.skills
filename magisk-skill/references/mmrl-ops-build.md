# MMRL: správa repozitáře, údržba a build

Rozlišuj správu **repozitáře modulů** od konfigurace WebUI modulu a od sestavení Android aplikace.

## 1. Repo MMRL a metadata modulů

MMRL načítá moduly z repozitářů. Aktuální návody MMRL-Util popisují `config.json` repozitáře, indexy/tracks a `common/repo.json` metadata modulu.

### Repo konfigurace

- `id` je podle aktuálního dokumentu povinné od 1. 1. 2026 a stabilní; `name` a `base_url` jsou povinné.
- `base_url` musí končit lomítkem.
- `website`, `support`, `donate`, `submission`, `description`, `max_num`, `enable_log`, `log_dir` jsou volitelné podle schématu.
- Nezaměňuj `config.json` repozitáře za `webroot/config.json` modulu.
- Proveď validaci URL, JSON a HTTPS; nepublikuj tajné údaje v repo configu.

### MMRL-Util

Oficiální instalace uvádí `pip3 install mmrl-util`. Před příkazy nejdřív použij `mmrl-util --help` a nápovědu konkrétní podcommand verze; CLI se může měnit. Oficiální command families zahrnují `config`, `track`, `github`, `sync`, `index`, `check` a `sitemap`. V CI pinuj a aktualizuj verzi záměrně, logy nenechávej obsahovat tokeny.

Doporučený tok repo maintaineru:

1. Otevři existující repo a zachovej jeho pevné `id`/URL.
2. Zkontroluj module ZIP, stabilní `module.prop` ID, verzi a aktualizované track/release URL.
3. Ověř metadata přes aktuální `mmrl-util check`; index aktualizuj nástrojem podle `mmrl-util index --help`.
4. Použij `sync`/`track`/`github` pouze podle záměru; před destruktivním přepisem ověř diff a vytvoř zálohu.
5. Spusť pipeline v test branch, ověř publikovaný index a odkazy přes HTTP GET.
6. Verifikuj z MMRL, že se repo načte, metadata odpovídají, ZIP stáhne a track nabízí správnou verzi.

### Metadata modulu a track

- Modulová MMRL metadata patří podle guide do `common/repo.json` (JSON nebo YAML). Může obsahovat support/donate/cover/icon/license/readme/homepage/screenshots/categories/devices/arch/require a manager-specific constraints. Ověř přesný název pole a podporu podle aktuální verze.
- `category` je označena jako nepodporovaná v MMRL V4+; používej `categories` pouze pokud je povolena repo whitelistem.
- `devices`, `arch` a `require` mohou přepsat manager-specific nastavení. Nestanovuj omezení bez ověřeného důvodu; můžeš tím uživatele vyloučit z instalace.
- Pokud upravíš metadata, zvýš module `versionCode` dle MMRL guide, aby se změna propsala do repozitáře.
- `antifeatures` patří do `track.json`; označ odpovídající skutečné charakteristiky (např. Ads, Tracking, NonFreeNet, KnownVuln, Obfuscation, UnaskedRemoval, LLM) a nehádej.
- Popis modulu / readme je samostatný od installer terminal output a WebUI `config.json`.

## 2. Build MMRL nebo WebUI X: Portable aplikace

Oficiální projekty jsou Kotlin/Android Gradle repozitáře:

- [MMRL](https://github.com/MMRLApp/MMRL)
- [WebUI X: Portable](https://github.com/MMRLApp/WebUI-X-Portable)

Před buildem prohlédni `README.md`, Gradle wrapper, version catalog, build logic, Android Gradle Plugin, požadavky JDK/SDK, flavors, signing config a GitHub Actions. Nepřidávej libovolné dependency versions ani `local.properties`/keystore do repozitáře. Build environment zjisti z kódu/CI, ne ze zastaralé webové quick-start věty.

Bezpečný build workflow:

1. Clone/fetch pouze oficiální upstream, prohlédni branch/tag/commit a working tree. Pracuj na branch, zachovej upstream license.
2. Ověř JDK, Android SDK, Gradle wrapper a projektové build variants z repository files. Wrapper používej místo globální Gradle, ledaže project docs říkají jinak.
3. `./gradlew tasks` (Windows: `gradlew.bat tasks`) zjistí dostupné tasky. Pak spusť relevantní unit tests/lint a debug build task podle project variants (např. `assembleDebug`, pokud je skutečně nakonfigurován).
4. Při chybě nejdřív odlišíš JDK/SDK, download dependency, plugin compatibility a zdrojový kód. Nevymazávej Gradle cache, signing files ani user changes bez potřeby.
5. Ověř výstup APK, application id, version, podpis (debug ≠ release), ABI a instalaci pouze v testovacím/emulovaném zařízení. Neoznač debug APK za release-ready.
6. Pro release použij jen oficiálně oprávněný signing workflow. Nevyžaduj ani nevkládej soukromý keystore do sdíleného ZIPu.

Dokumentace MMRL potvrzuje Android Studio/Gradle build jako obecný postup, ale konkrétní verze a tasky zjisti z aktuálního checkoutu. Návody mohou zaostávat za zdrojovým stromem.

## 3. Sestavení WebUI modulu

- Statické UI může být bez bundleru: `webroot/index.html`, `styles.css`, `app.js`, lokální assety.
- Pokud framework potřebuje bundling, nejdřív ověř Node/npm verzi a scripts v `package.json`; commitni lockfile a build assety vlož do module `webroot` podle očekávání repozitáře.
- Pro kompatibilitu/offline režim minimalizuj externí CDN, fonty a runtime network calls. Pokud jsou nutné, dokumentuj origin a nastav CSP minimálně potřebně.
- Validuj JSON pomocí parseru, HTML/CSS/JS build/lint nástrojů projektu a zkontroluj všechny odkazy vůči skutečné cestě uvnitř ZIPu.
- Sestav vlastní Magisk ZIP samostatně. Aplikace MMRL/WebUI X APK build není totéž co WebUI asset bundling nebo Magisk module ZIP.

## Zdroje

- [MMRL GitHub](https://github.com/MMRLApp/MMRL)
- [WebUI X: Portable GitHub](https://github.com/MMRLApp/WebUI-X-Portable)
- [MMRL-Util guide](https://mmrl.dev/guide/mmrl-util/)
- [Repo `config.json`](https://mmrl.dev/guide/mmrl-util/config-json)
- [Module `repo.json`](https://mmrl.dev/guide/mmrl-util/repo-json)
- [Track JSON](https://mmrl.dev/guide/mmrl-util/track-json)
- [MMRL anti-features](https://mmrl.dev/guide/antifeatures)
- [Module card behavior](https://mmrl.dev/guide/how-a-module-card-works)
