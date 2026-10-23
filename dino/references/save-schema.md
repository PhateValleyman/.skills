# Schéma uložených dat – Crazy Dino Park (save verze 2.32)

Obsah: 1. Měny a postup · 2. Klece a dinosové · 3. Truhly a kosti · 4. Lokace a výkopy ·
5. Odemčené funkce · 6. Objevené položky a achievementy · 7. Čas a události · 8. Multidig, Arena, výpravy ·
9. wardrobe-save · 10. local-json · 11. local-pref

Pozn.: "pravděpodobně" = odvozeno z názvu/hodnoty, není potvrzeno.

## 1. Měny a postup (`save.*`, skalární int)
| klíč | význam |
|---|---|
| `_CoinsNo` | mince (základní měna) |
| `_BillsNo` | bankovky – pravděpodobně prémiová měna |
| `_StonesNo` | kameny – pravděpodobně další měna (stavba/vylepšení) |
| `_LikesNo` | lajky |
| `_PiggyBank`, `_PiggyBankCollectedCoins`, `_PiggyBankDestroyedCounter` | pokladnička: obsah, nasbírané mince, kolikrát rozbita |
| `_BankLevel` | úroveň banky (pravděpodobně kapacita pokladničky) |
| `_FactoryResources[0]` | zdroje továrny |
| `_XPNum`, `_ProcessedXPNum` | zkušenosti |
| `_NumGoldenPickaxe` | zlaté krumpáče (alias `NumGoldenPickaxe`) |
| `_TicketBoothLevel`, `_TicketBoothClickTime` | pokladna se vstupenkami |
| `_GamesNoCounter`, `_IncubatedEggsNo`, `_DugBonesNo` | čítače: hry, inkubovaná vejce, vykopané kosti |
| `_IncomeStats._Items.<n>`, `_IncomeMax` | statistiky příjmu (klíč pravděpodobně den/pořadí, hodnota příjem) |
| `_SellBonesFirstDay`, `_SellBonesExtraValue` | prodej kostí (den začátku, bonus) |

## 2. Klece a dinosové (`save._Cages.<DinoN>.*`)
Jedna klec na druh (`Dino1`..`Dino34`, `Dino50`, `Dino51`; v dumpu 36 klecí = `NumCages`).
Pořadí zobrazení: `save._DinoCagesOrder[]`.

Pole klece: `_DinoID`, `_UnderConstructionTime` (kdy postavena), `_Ready`, `_NextSleepBeginTime` (null),
`_AutoShow`, `_TotalDinosNo`, `_CurrentLevel` (úroveň klece), `_FirstTime`, `_WasShown`,
`_NextEggCounter`, `_GoldsNo`, `_Poos[]`, `_EpicPoos[]`.

Jednotlivý dino: `_Dinos[i]._GUID` (UUID – klíč pro wardrobe-save), `_ID`, `_Level` (v dumpu 1–6),
`_Special` (bool), `_FirstTime`, `_ArenaRebornTime`, `_TrainingCompletedDate`, `_TrainingBoostActiveDate`
(časy nebo null), `_BoostPower`, `_BoostHP`, `_BoostSpeed`, `_BoostDefense` (v dumpu 0, 11 nebo 50).

Konzistence (ověřeno na dumpu, 36 klecí): `_TotalDinosNo` se rovná počtu `_Dinos[]` u 23 klecí a je větší u 13; nikdy není menší. Pravděpodobně se ne každý dino ukládá jednotlivě (proč, z dumpu nejde poznat) – při úpravě proto počet `_Dinos[]` nikdy nezvyšuj nad `_TotalDinosNo`.

## 3. Truhly a kosti (`save._Chests.<DinoN>.*`)
Pro každý druh:
- `_Bones.<Druh>_<část>` – počet kostí, části: `head`, `rib`, `small`, `extra` (v dumpu typicky 999),
- `_ReconstructionBonesIndex.<Druh>_<část>` – index rekonstrukce,
- `_ReconstructedDinoBones.<Druh>_<část>` – pole poskládaných kostí (`[]` = nic),
- `_FirstTime` (bool).
Názvy druhů v kostech jsou anglické (Trex, Stegosaur, Triceratops, Pterodactyl, Smilodon ...),
klíč truhly je `DinoN`; mapování N→druh si z dumpu odvoď jen tam, kde je v cestě obojí, jinak nehádej.

## 4. Lokace a výkopy
- `_Locations[]` – pořadí lokací: `LocationEPIC1-5`, `LocationUnderground1-6`, `Location1-14`,
  `LocationMine_Sand/_Ice/_Silicon/_Swamp`. `SelectedLocationID` / `_SelectedLocationID` = aktuální (v dumpu `Location14`).
- `_LocationsData.<Lokace>._ID`, `._Price`, `._BonesNo._Items.<DinoN>` – kosti nalezené v lokaci.
- `_LocationVisitCounter._Items.<LocationN>` – počet návštěv.
- `_LocationBoneQueues.<Lokace>._Queue[]` – fronta kostí k vykopání (čísla).
- `_Trashe._Items.<trash ...>`, `_CollectedTrashCounters.<Lokace>._Items.<trash ...>`, `_PrevTrashID.<Lokace>` – odpad/sběratelské předměty.
- `_VehiclesAbilityCounter`, `_VehiclesBuyCounter` (`_Items.VehicleN`, `Count`, `SumAll`, `_MaxSumAll`),
  `_Vehicles[]`, `_SelectedVehicleID`.

## 5. Odemčené funkce (bool, `save._…Unlocked`)
TopPanel, Expedition, Incubator, TrashBestiary, MultiDig, MultiDigSpecial, ArenaTournament, DressRoom,
Arena, ArenaMultiplayer, PhotoBooth, Undeground (sic), Factory, ArenaTrainingCamp. Dále
`_TutorialCompleted[]` (28 dokončených tutoriálů: Intro, TicketBooth, ... RaveParty).

## 6. Objevené položky a achievementy
- `_DiscoveredIDs[]` (156): `DinoN`, `DinoN_k`, `EggN`, `trash …`, `map …` ...; `_NewDiscoveredIDs[]` – ještě neshlédnuté.
- `_UnlockedAchievementsIDs[]` (115), `_AvailableAchievementsIDs[]`, `_AchievementGroupID`.
- `_ObjectSelectableTypesUnlocked.<Typ_…>` (Bench, Bush, Column, Entrance, Statue), `_SelectableTypesIndex`,
  `_SelectedSelectableTypesIndex` – výběr dekorací parku.
- `_UpgradableTypesLevel.<Jídlo>` (HotDog, Dumplings, Cola, Ice, Pizza, Sushi) + `_UpgradableTypesExitDate`.
- `_BattleCards._BattleCardsStatus_BattleCardsContainerAll` – vnořený JSON uložený jako string.

## 7. Čas a události
`_ExitTime` (poslední ukončení hry), `_NextDailyTaskTime`, `_TimeStamp` (Unix), `_LotteryDay`, `_PrevDayInRow`,
`_DaysInRow`, `_DayRewardConsumed`, `_MiniAchievement*`, `_Winter*` (zimní event), `_Rave*` (Rave Party),
`_SpecialOfferIAP`, `_SpecialOfferIAP_Active`, `_ActivePowerUps[]` (`_Type`: DigCost, Income ...; `_StartDate`, `_DueDate`),
`_PoliceOfficerStatus`, `_AnniversaryCollected`. Hodnoty `…Day` jsou pravděpodobně počty dnů od pevného data (v dumpu ~2650–2920).

## 8. Multidig, Arena, výpravy
- `_MultiDig*`/`_MultiDig2*` (`ToolsNo`, `PiggysNo`, `CoinsNo`, `GemsNo`, `RoomID`, `RoomIndex`, `GUID`),
  `_MultidigLocal`, `_MultidigKevin` (stav mapy, ostrov), `_Kevin*`.
- `_Arena*`: `_ArenaPlayerRank`, `_ArenaMultiplayerRating`, `…LostStrike`, `…CurrentBattleValue`,
  `…LeagueRange[]`, `_ArenaSelectedPlayerDinosID[]` (`_DinoID` -1 = prázdný slot), `_NumMultiplayerWins/Lost`,
  `_NumTournamentWins`, `_TournamentID`, `_TournamentRewards`, `_TrainingNumSpeedUps`.
- `_ExpeditionsData[i]`: `_IsActive`, `_ExpeditionTime`, `_ExpeditionPrice`, `_ExpeditionSuccessDate`; `_ExpeditionSendNumber`.
- `_Challenge*` – výzvy, v dumpu prázdné (null / `{}`).

## 9. wardrobe-save (`save_1.*`)
`m_vAvailableDecorations.<Hat_N|Glasses_N|Tie_N>` (počet kusů), `m_vUnlockedDecorations[]`,
`m_vDinoDecorations.<GUID dina>._Decorations.0..2` + `.NumDecorations`. GUID odpovídá
`save._Cages.<DinoN>._Dinos[i]._GUID`.

## 10. local-json
- `SummaryFullDinoMarkerCounter` – `Count`, `SumAll`, `_Items.DinoN` (0/1 označení v souhrnu).
- `PhotoBoothSaveData[i]` – prvek fotokoutku: `_PrefabName`, `_Pos[0..2]`, `_Scale`, `_Angle`, `_SortOrd`,
  `_FlipVertical`, `_FlipHorizontal`, `_JSonDeliveredClass`.

## 11. local-pref (Unity PlayerPrefs)
Většina hodnot jsou stringy v uvozovkách (`"3"`). Skupiny: reklamy (`Ads*`), Google Play Games
(`GPGS_*`, `sev_base_*`), přihlášení (`Login_*` – redigováno), park event (`ParkEvent*`), rekonstrukce
(`Reconstruction*`), Arena (`ArenaSeed`, `League_Season`), nastavení (`SelectedLanguage`, `Screenmanager …`),
systém (`OSVersion`, `EngineVersion`), integrita (`TimeStamp`, `TimeStampHash`) a Unity telemetrie (`unity*`, `UnityInstallationId`).
Hodnoty s `[REDACTED]` (session/installation/player ID, tokeny) nikdy nedopisuj.
