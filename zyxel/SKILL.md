---
name: zyxel
description: Safe administration and legacy ARMv5/soft-float/uClibc build guidance for a ZyXEL NSA320 running Fonz Fun Plug (FFP). Use when the user explicitly identifies an NSA320, FFP, /ffp, or a matching device profile in the conversation. Do not trigger on generic “server” or “NAS” requests. Confirm the current host, user, key and requested access before any device/network operation; do not infer a target or credential from this reference.
---
# ZyXEL NSA320 / FFP

## Kdy a jak začít

Použij pouze pro výslovně určený NSA320/FFP. Všechny historické parametry ověř na skutečném cíli. Nevybírej vzdálené zařízení, host, uživatele ani SSH klíč podle názvu tohoto skillu. Nejprve použij autorizační a device-selection postup dostupný v hostitelském prostředí.

1. Zjisti přesný cíl, rozsah a požadovaný výsledek; odliš čtení od změny.
2. Ověř identitu, architekturu, ABI, kernel, libc, dostupné nástroje a aktivní konfiguraci.
3. Načti odpovídající části `references/administration-reference.md` podle tabulky níže.
4. Zaznamenej stav, zazálohuj měněné soubory a navrhni nejmenší vratnou změnu.
5. Proveď pouze autorizovanou změnu, ověř skutečný běh a popiš návratový postup.

## Technické hranice

NSA320 je historicky ARMv5/Feroceon, soft-float, FFP 0.7.0, uClibc a starý kernel. Jde o pracovní výchozí profil, ne výsledek aktuálního měření. Nezaměňuj jej za běžný moderní Linux. Nepředpokládej systemd, glibc, nový Bash nebo moderní GNU/iproute2 příkazy. Ověř kompatibilitu binárky, dynamického linkeru, knihoven i minimálního kernelu. Používej `/ffp/bin/bash` jen pokud skutečně existuje; cesty k přibalené referenci odvozuj od tohoto SKILL.md.

## Bezpečnost před každou změnou

- Neodstraňuj, neformátuj a nepřerozděluj disky ani RAID bez souhlasu s konkrétní operací a ověřené obnovy. Názvy zařízení ani mountpointy nehádej.
- Neupravuj firmware, bootloader, kernel či systémové knihovny jako diagnostickou zkratku. Opatrně s rekurzivními právy, vlastnictvím a broad deletion.
- Před cleanup ověř přesné cesty, účel, vlastníka, závislé služby a zálohu. Velikost není důvod ke smazání.
- Nikdy nevypisuj soukromé klíče, tokeny ani hesla. Neoslabuj SSH autentizaci či ověření hostitele.
- Nepřepisuj Git práci, konfiguraci ani release klíče bez konkrétní autorizace. Žádný automatický reset, force-push či hromadné odstraňování.
- Nepoužívej nekonečné boot-blocking retry smyčky, neomezenou paralelizaci buildů nebo zbytečné root služby. Plánované úlohy musí mít limity, zámek a bezpečný failure path.
- Před restartem ověř uloženou konfiguraci, mounty, aktivní přenosy, správný startup a možnost návratu přes SSH. Samotný exit code 0 není ověření výsledku.

## Kterou část podrobné reference načíst

Všechny následující části jsou v `references/administration-reference.md`; čti podle potřeby, nikoli automaticky celou referenci.

| Úkol | Části |
|---|---|
| První diagnostika, shell a SSH | 2–6 |
| FFP balíčky a ARMv5/Go buildy | 7–9, 18 |
| Úložiště, cleanup, zálohy | 10–12 |
| Služby, síť, porty, logy, zdroje | 13–17 |
| Cron a SSHFS/MeshFS | 19–20 |
| Git a změna aktivní konfigurace | 21–22 |
| Ověření, restart, firmware, zabezpečení | 23–26 |
| Dokončení, rozhodovací strom, rychlý přehled | 27–31 |

## Předání výsledku

Uveď pozorovaný stav, přesnou změnu, skutečně provedený test, perzistenci (proces/restart/reboot), potřebu rebootu, rollback a neověřené předpoklady. Návrh příkazu neoznačuj za vykonaný příkaz. Při chybě či nejistotě zastav změny a nejdřív získej důkaz.
