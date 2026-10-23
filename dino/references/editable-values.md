# Katalog upravitelných hodnot (z dumpu)

## Měny a postup
int; strop pravděpodobně int32 (2 147 483 647). NumGoldenPickaxe je alias _NumGoldenPickaxe – měň obě.

- `save._CoinsNo` (int) = 505000
- `save._BillsNo` (int) = 99984712
- `save._PiggyBank` (int) = 1022
- `save._LikesNo` (int) = 2812
- `save._StonesNo` (int) = 10001137
- `save._FactoryResources[0]` (int) = 999999
- `save._XPNum` (int) = 115
- `save._PiggyBankCollectedCoins` (int) = 999999
- `save._BankLevel` (int) = 15
- `save._TicketBoothLevel` (int) = 7
- `save._NumGoldenPickaxe` (int) = 99
- `save.NumGoldenPickaxe` (int) = 99

## Čítače a statistiky
int; čistě statistiky, nižší riziko. Rating/Rank/Wins souvisí s online částí.

- `save._GamesNoCounter` (int) = 547
- `save._IncubatedEggsNo` (int) = 108
- `save._DugBonesNo` (int) = 207
- `save._ArenaPlayerRank` (int) = 54
- `save._ArenaMultiplayerRating` (int) = 596
- `save._IncomeMax` (int) = 591189
- `save._NumTournamentWins` (int) = 0
- `save._NumMultiplayerWins` (int) = 3
- `save._NumMultiplayerLost` (int) = 0
- `save.ArenaMultiplayerRating` (int) = 596
- `save.NumTournamentWins` (int) = 0

## Odemčené funkce (bool)
bool; true = odemčeno.

- `save._TopPanelUnlocked` (bool) = true
- `save._ExpeditionUnlocked` (bool) = true
- `save._IncubatorUnlocked` (bool) = true
- `save._TrashBestiaryUnlocked` (bool) = true
- `save._MultiDigUnlocked` (bool) = true
- `save._MultiDigSpecialUnlocked` (bool) = true
- `save._ArenaTournamentUnlocked` (bool) = true
- `save._DressRoomUnlocked` (bool) = true
- `save._ArenaUnlocked` (bool) = true
- `save._ArenaMultiplayerUnlocked` (bool) = true
- `save._PhotoBoothUnlocked` (bool) = true
- `save._UndegroundUnlocked` (bool) = true
- `save._FactoryUnlocked` (bool) = true
- `save._ArenaTrainingCampUnlocked` (bool) = true
- `save.m_vEmoticonsUnlocked` (array) = []

## Kosti v truhlách
int; počet kostí dané části (head/rib/small/extra). Rodina hodnot – viz šablona.

- šablona `save._Chests.DinoN._Bones.<druh>_small` – 928 hodnot, int; v dumpu: 993, 999, 1000, 1002; příklad `save._Chests.Dino1._Bones.Amonit_small`
- šablona `save._Chests.DinoN._Bones.<druh>_head` – 992 hodnot, int; v dumpu: 998, 999, 1000; příklad `save._Chests.Dino1._Bones.Amonit_head`
- šablona `save._Chests.DinoN._Bones.<druh>_rib` – 960 hodnot, int; v dumpu: 989, 992, 996, 999, 1000, 1001, 1002; příklad `save._Chests.Dino1._Bones.Gallimimus_rib`
- šablona `save._Chests.DinoN._Bones.<druh>_extra` – 800 hodnot, int; v dumpu: 997, 999, 1000; příklad `save._Chests.Dino1._Bones.Pterodactyl_extra`

## Dinosové – úroveň a boosty
Level v dumpu 1, 2, 3, 4, 6; Boost 0–50 (nad 50 neověřeno). Special bool. Rodina hodnot.

- šablona `save._Cages.DinoN._Dinos[i]._Level` – 57 hodnot, int; v dumpu: 1, 2, 3, 4, 6; příklad `save._Cages.Dino1._Dinos[0]._Level`
- šablona `save._Cages.DinoN._Dinos[i]._Special` – 57 hodnot, bool; v dumpu: true, false; příklad `save._Cages.Dino1._Dinos[0]._Special`
- šablona `save._Cages.DinoN._Dinos[i]._BoostPower` – 57 hodnot, int; v dumpu: 0, 11, 50; příklad `save._Cages.Dino1._Dinos[0]._BoostPower`
- šablona `save._Cages.DinoN._Dinos[i]._BoostHP` – 57 hodnot, int; v dumpu: 0, 16, 50; příklad `save._Cages.Dino1._Dinos[0]._BoostHP`
- šablona `save._Cages.DinoN._Dinos[i]._BoostSpeed` – 57 hodnot, int; v dumpu: 0, 16, 50; příklad `save._Cages.Dino1._Dinos[0]._BoostSpeed`
- šablona `save._Cages.DinoN._Dinos[i]._BoostDefense` – 57 hodnot, int; v dumpu: 0, 7, 50; příklad `save._Cages.Dino1._Dinos[0]._BoostDefense`

## Klece
CurrentLevel v dumpu 2–3.

- šablona `save._Cages.DinoN._Ready` – 36 hodnot, bool; v dumpu: true; příklad `save._Cages.Dino1._Ready`
- šablona `save._Cages.DinoN._AutoShow` – 36 hodnot, bool; v dumpu: true; příklad `save._Cages.Dino1._AutoShow`
- šablona `save._Cages.DinoN._CurrentLevel` – 36 hodnot, int; v dumpu: 2, 3; příklad `save._Cages.Dino1._CurrentLevel`
- šablona `save._Cages.DinoN._WasShown` – 36 hodnot, bool; v dumpu: true; příklad `save._Cages.Dino1._WasShown`
- šablona `save._Cages.DinoN._NextEggCounter` – 36 hodnot, int; v dumpu: 0, 72, 163, 173, 220, 254, 266, 279 …; příklad `save._Cages.Dino1._NextEggCounter`
- šablona `save._Cages.DinoN._GoldsNo` – 36 hodnot, int; v dumpu: 0, 3; příklad `save._Cages.Dino1._GoldsNo`

## Vozidla
int; Count/SumAll/_MaxSumAll u _Items drž konzistentní (SumAll = součet _Items).

- `save._VehiclesAbilityCounter._Items.Vehicle1` (int) = 0
- `save._VehiclesAbilityCounter._Items.Vehicle2` (int) = 533
- `save._VehiclesAbilityCounter._Items.Vehicle3` (int) = 138
- `save._VehiclesAbilityCounter._MaxSumAll` (int) = 1500
- `save._VehiclesAbilityCounter.Count` (int) = 3
- `save._VehiclesAbilityCounter.SumAll` (int) = 671
- `save._VehiclesBuyCounter._Items.Vehicle1` (int) = 3
- `save._VehiclesBuyCounter._Items.Vehicle2` (int) = 37
- `save._VehiclesBuyCounter._Items.Vehicle3` (int) = 7
- `save._VehiclesBuyCounter._MaxSumAll` (int) = 47
- `save._VehiclesBuyCounter.Count` (int) = 3
- `save._VehiclesBuyCounter.SumAll` (int) = 47

## Vylepšení jídla
int; v dumpu 5.

- `save._UpgradableTypesLevel.HotDog` (int) = 5
- `save._UpgradableTypesLevel.Dumplings` (int) = 5
- `save._UpgradableTypesLevel.Cola` (int) = 5
- `save._UpgradableTypesLevel.Ice` (int) = 5
- `save._UpgradableTypesLevel.Pizza` (int) = 5
- `save._UpgradableTypesLevel.Sushi` (int) = 5

## Multidig / Arena zdroje
int.

- `save._MultiDigToolsNo` (int) = 0
- `save._MultiDigPiggysNo` (int) = 0
- `save._MultiDigCoinsNo` (int) = 0
- `save._MultiDigGemsNo` (int) = 0
- `save._MultiDig2ToolsNo` (int) = 0
- `save._MultiDig2PiggysNo` (int) = 0
- `save._MultiDig2CoinsNo` (int) = 0
- `save._MultiDig2GemsNo` (int) = 0
- `save._TrainingNumSpeedUps` (int) = 0

## Šatník (wardrobe-save)
int; počet kusů dekorace (scope wardrobe-save, jiný soubor než game-save).

- `save_1.m_vAvailableDecorations.Hat_23` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_22` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_21` (int) = 6
- `save_1.m_vAvailableDecorations.Hat_20` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_15` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_13` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_14` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_12` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_11` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_10` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_9` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_8` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_7` (int) = 0
- `save_1.m_vAvailableDecorations.Glasses_4` (int) = 6
- `save_1.m_vAvailableDecorations.Tie_6` (int) = 0
- `save_1.m_vAvailableDecorations.Tie_2` (int) = 6
- `save_1.m_vAvailableDecorations.Hat_19` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_24` (int) = 0
- `save_1.m_vAvailableDecorations.Hat_6` (int) = 0
- `save_1.m_vAvailableDecorations.Tie_1` (int) = 0
- `save_1.m_vAvailableDecorations.Tie_12` (int) = 0
- `save_1.m_vAvailableDecorations.Glasses_3` (int) = 0
- `save_1.m_vAvailableDecorations.Glasses_13` (int) = 1

## Chráněné (patch je odmítne) – 108 cest v dumpu, např.: `save._DinoId`, `save._PlayerName`, `save._Guid`, `save._SaveId`, `save._BranchId`, `save._Valid3`
