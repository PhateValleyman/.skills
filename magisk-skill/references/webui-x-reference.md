# WebUI X: konfigurace, API, design a ladění

Tato reference shrnuje oficiální dokumentaci MMRL/WebUI X; verzní podrobnosti ověř před použitím v cílovém hostu.

## Struktura a konfigurace

WebUI modulu obvykle obsahuje `webroot/index.html`, související styly, skripty, ikony/assets a volitelný `webroot/config.json` nebo `webroot/config.mmrl.json`. Dokumentace MMRL uvádí obě cesty. Neodhaduj precedence při současném výskytu: zkontroluj aktuální host a zachovej formát, který používá daný projekt. `config.mmrl.json` je výslovně požadován pro domovskou zkratku v aktuálním návodu.

Mezi doložené vlastnosti konfigurace patří:

| Klíč | Význam / poznámka |
|---|---|
| `modId` | Modul ID; identifikace musí odpovídat pravidlům hosta. |
| `require.packages` | Požadavky na balíčky a případná pomocná zpráva/link. |
| `permissions` | Pole stringů oprávnění WebUI X; seznam konkrétních hodnot čti z aktuálního API podle hosta. Dokumentovaný příklad obsahuje `wx.permission.ROOT_PATH`; neoprávňuj na základě domněnky. |
| `historyFallback`, `historyFallbackFile` | Volitelný fallback pro SPA routing. |
| `title`, `icon` | Název/ikona UI či zkratky; ikona je relativní k `webroot`. |
| `windowResize` | Resize/keyboard behavior; default v docs `true`. Nastav `false` jen pokud to vyžaduje layout/keyboard CSS. |
| `backHandler`, `backInterceptor` | Způsob práce s tlačítkem zpět; `backInterceptor` může přebít default. |
| `refreshInterceptor`, `pullToRefresh` | Obsluha obnovy/pull-to-refresh. Ověř podle hostu a UI designu. |
| `exitConfirm`, `autoStatusBarsStyle` | Potvrzení odchodu a styl systémových status barů; ověř defaulty v cílové verzi. |
| `dexFiles` | Dynamické načítání DEX/APK a Java interface; vysoce privilegovaná/advanced možnost, nepoužívat bez konkrétní potřeby a ověřeného artefaktu. |
| `killShellWhenBackground` | Životní cyklus shell procesů podle dokumentace (od určité verze). |
| `contentSecurityPolicy` | CSP; docs popisují default i merge novější MX Engine. Zachovej přísné policy a rozšiř pouze o konkrétní nutný origin. |
| `caching`, `cachingMaxAge` | Cache webových zdrojů; při ladění stale UI ověř cache. |

Vždy generuj validní JSON bez komentářů (pokud host nepodporuje JSONC), neznámé hodnoty vynechej a při nové konfiguraci preferuj pouze klíče nutné pro funkci. Nespouštěj shell/file/network API z konfigurace jen proto, že jsou dostupné.

## Příklady safe defaults

Šablona balíčku obsahuje minimal `config.mmrl.json.example`: pokud není potřeba API, žádné permissions nejsou nutné. Klíčové UI může být plně statické. Jestli je potřeba persistovat nastavení, zvol podle hostu aktuálně dokumentovaný způsob; nespoléhej na `localStorage` jako trvalé úložiště po odinstalaci manažeru. KernelSU dokumentace výslovně uvádí, že `localStorage` se po odinstalaci manageru ztratí.

## Vzhled a safe area

- Aktuální guide importuje `https://mui.kernelsu.org/internal/insets.css` a `https://mui.kernelsu.org/internal/colors.css`; staré `/mmrl/` cesty jsou deprecated.
- Při fixed/absolute elementech na horním/dolním okraji použij `var(--window-inset-top)` / `var(--window-inset-bottom)`; nepřidávej insets znovu běžnému scrollovacímu kontejneru.
- Pro barvy používej semantické tokeny Material You (`--background`, `--onBackground`, `--surface`, `--onSurface`, `--primary` apod.) a testuj light/dark režim.
- Je-li klávesnice relevantní, dokumentace uvádí `--window-keyboard-height`; použij fallback k bottom inset a ověř `windowResize` chování.
- Externí stylesheet znamená síťovou závislost; pokud je žádoucí offline/deterministické UI, zabal lokální kopii licencovaných assetů a ověř CSP.

## API a kompatibilita

- Aktuální [TypeDoc](https://docs.mmrl.dev/) publikuje `webuix` balíček a `wxu` utility plugin. Zkontroluj konkrétní export, typ, verzi knihovny i host, než napíšeš JS bridge.
- Historické npm `mmrl` knihovny či staré MMRL API příklady nejsou automaticky kompatibilní s WebUI X. Používej jen pokud projekt a aktuální host výslovně potvrzují danou variantu.
- Dokumentovaný WebUI X event systém (`WXEventHandler`) je stále ve vývoji a jeho podpora se liší: MMRL od v33661; podle guide ji nepodporuje WebUI X Portable. Znovu ověř aktuální stav, než na něm postavíš navigaci.
- Legacy Installer API odstraněno v MMRL v33870. Pro instalátor vyhledej současný Installer V2 API; staré broadcast akce nepřebírej z legacy příručky.

## DevTools a diagnostika

1. V WebUI X: Portable/MRRL otevři modul přes host, následně použij integrovaný DOM inspector, console history a network monitor.
2. Zkontroluj první load a stav po refresh/back; sleduj konkrétní JS exception, 404/CSP chyby a chybějící assety.
3. Ověř test hostu a verzi včetně root/non-root režimu; WXP nabízí file explorer/editor, ale host-side config/patche mohou být v jiném úložišti než `webroot` projektu.
4. Pro SPA ověř historii a `historyFallback`; pro fixed UI zkontroluj status/navigation bar insets; pro form input otestuj výšku klávesnice.
5. Testuj privilegované akce v izolovaném/neprodukčním prostředí. Když chyba zmizí až po vypnutí CSP nebo přidání širokého permission, nepovažuj to za opravu — najdi přesnou příčinu a omez scope.

## Patching WebUI X: Portable

Oficiální guide pro Portable popisuje host-side patch adresář `/data/adb/.config/<id>/` s `style/patch.css`, `js/head/` a `js/body/`. `.js`/`.cjs` se načítají jako klasické skripty a `.mjs` jako ES moduly. To jsou patche host UI instance, ne soubory, které se automaticky instalují z kořene modulu. Před přepisem živých patchů vytvoř zálohu; ověř ID adresáře a cílovou instanci. Tuto strukturu použij pouze pro WebUI X: Portable podle aktuálního návodu.

## Domovská zkratka

MMRL guide popisuje `title` a `icon` v `config.mmrl.json` a `createShortcut()` z module interface; potřebuje launcher podporující pinované zkratky. Ikona musí být uvnitř `webroot`. Ověř aktuální implementaci metody a vyvaruj se použití neověřeného globálního jména API.

## Zdroje

- [WebUI X overview](https://mmrl.dev/guide/webuix/)
- [Index setup](https://mmrl.dev/guide/webuix/index-setup)
- [CSS / theme / insets](https://mmrl.dev/guide/webuix/css-setup)
- [config.json](https://mmrl.dev/guide/webuix/config)
- [Events](https://mmrl.dev/guide/webuix/events)
- [Patching in WebUI X Portable](https://mmrl.dev/guide/webuix/patching)
- [Shortcuts](https://mmrl.dev/guide/webuix/shortcuts)
- [WebUI X JavaScript TypeDoc](https://docs.mmrl.dev/)
- [MMRL WebUI X: Portable](https://github.com/MMRLApp/WebUI-X-Portable)
