# World generation, functions, commands, and automation

## Commands and functions
- Use commands for quick prototypes and repeatable administrative actions.
- Use `.mcfunction` files for reusable command sequences; verify exact folder naming and function permission/cheat requirements.
- Keep long command chains bounded and test them in a copy of the world.
- Use selectors carefully and constrain affected dimensions/regions.

## World generation
- Separate feature definitions from feature rules where the format requires it.
- Verify target-version support for custom terrain, ores, structures, vegetation, and biome-related content.
- Test generation in newly created chunks; existing chunks may not regenerate.
- Document whether a world must be newly created and which experimental toggles are needed.

## Procedural builds
- Convert high-level plans into deterministic coordinate transforms and a block palette.
- Define origin, rotation, mirror behavior, and chunk-safe batches.
- Support dry-run or preview when feasible.
- Avoid loading huge numbers of blocks synchronously in one tick.
