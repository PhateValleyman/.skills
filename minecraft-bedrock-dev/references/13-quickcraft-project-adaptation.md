# QuickCraft project adaptation notes

Use this guide only when the active project is the user's custom QuickCraft version. Inspect the actual supplied repository/archive before relying on these notes; paths and APIs may have changed.

## Known prior project context
- The user uses a custom-modified QuickCraft add-on for Bedrock/PE.
- A prior target baseline was Minecraft Bedrock 1.21.80 with `@minecraft/server` 2.0.0 and `@minecraft/server-ui` 2.0.0; **verify against the actual project and game version before using**.
- Previously discussed structure path: `pack/behavior_pack/QuickCraft/structures/`.
- Previously discussed catalog: `pack/behavior_pack/QuickCraft/scripts/catalog.js`.
- Previously discussed control icon: `./QuickCraft/pack/resource_pack/QuickCraft/textures/items/qc_menu.png`; retain transparency and existing visual style unless the user asks otherwise.
- Existing features mentioned include structure loading/scanning, instance metadata, `qc:control`, move-preview raycast behavior, and WAYpoint-like camera teleport. Verify current code before editing.

## Preservation rules
- Inspect archive/repository and map architecture before making changes.
- Preserve existing move/remove functionality and UI appearance unless explicitly requested.
- Add new structures through the existing catalog/registration mechanism instead of inventing a parallel system.
- Check structure identifiers, script paths, namespaces, and pack dependencies.
- Test place/move/remove and teleport workflows separately.
- Never assume a previous target version remains current.
