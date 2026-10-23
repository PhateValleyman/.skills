# Project layout and manifests

## Common pack types
- **Resource Pack (RP):** textures, models, render controllers, animations, sounds, particles, localization, and supported UI assets.
- **Behavior Pack (BP):** entities, blocks/items behavior, recipes, loot tables, spawn rules, functions, world generation definitions, and scripts.
- **Skin pack:** player skins plus pack metadata and skin geometry/metadata as required by the format.
- **World/template:** world save or template content; not interchangeable with a pack.
- **Structure:** a reusable region, often `.mcstructure`, not a complete world.

## Typical layout
```text
MyAddon/
├── behavior_pack/
│   ├── manifest.json
│   ├── entities/
│   ├── blocks/
│   ├── items/
│   ├── recipes/
│   ├── loot_tables/
│   ├── spawn_rules/
│   ├── structures/
│   ├── functions/
│   └── scripts/main.js
└── resource_pack/
    ├── manifest.json
    ├── textures/
    ├── models/
    ├── entity/
    ├── animations/
    ├── animation_controllers/
    ├── render_controllers/
    ├── particles/
    ├── sounds/
    └── texts/
```
This is illustrative; omit unused folders and follow the target format's exact folder names.

## Manifest review
- Check `format_version`, header name/description/UUID/version, module UUID/type/version, minimum engine version, dependencies, and module entry points.
- Use unique UUIDs; preserve UUIDs when updating an existing pack.
- BP/RP dependencies must point at the correct pack UUID and compatible version.
- Do not use Preview-only manifest schema in stable unless the target explicitly supports it.
- Check whether script modules require `language`, `entry`, and dependency declarations for the selected Script API version.
- JSON is case-sensitive in paths on some tooling; match filenames exactly.

## Pack stacking
Inspect active packs and priority. A higher-priority RP may override a texture or asset from a lower-priority pack. Diagnose conflicts by checking identifiers, dependencies, and pack order before rewriting files.
