# Structures, worlds, and maps

## Distinguish deliverables
- `.mcstructure`: a region/structure for supported Bedrock import/use workflows.
- `.mcworld`: world archive/import package.
- `.mctemplate`: world template package where supported.
- `.mcpack` / `.mcaddon`: pack or combined add-on import archive, not a world save.
- Raw world folders may contain LevelDB data and metadata; do not edit live databases casually.

## Structure workflow
1. Establish source format, dimensions, origin, block palette, entities, and target game version.
2. Back up the world and build the structure in a test world.
3. Use structure blocks or a known-compatible editor/tool to export.
4. Inspect dimensions and placement origin; document rotation/mirroring and air handling.
5. Put a `.mcstructure` in a BP `structures/` path when it is intended for add-on placement, and use the correct identifier/path in commands or scripts.
6. Test import in a disposable world. Check missing blocks, custom block dependencies, entities, and version differences.

## Large builds and procedural maps
- Plan a coordinate system, bounding box, origin, height limits, palette, and chunk boundaries.
- Generate in stages: terrain, shell, interior, lighting, details, loot, and spawn points.
- Use commands/functions or Script API for repeatable placement; chunk work into batches to avoid tick stalls.
- For structures such as a 45×45 volcano, define footprint, height, interior cavity, lava containment, safe routes, treasure room, and palette before generating.
- Use structure templates or a catalog registry for reusable builds.

## World editing safety
- Duplicate the world before bulk edits.
- Stop Minecraft before modifying raw world files.
- Avoid hand-editing LevelDB unless the schema and backup/restore procedure are known.
- Preserve `level.dat`, world identifiers, and player data unless the goal explicitly requires changing them.
- Validate the final archive with a file listing and a test import.
