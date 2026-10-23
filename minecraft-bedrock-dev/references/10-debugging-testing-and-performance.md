# Debugging, testing, performance

## Common failure classes
- Invalid JSON or unsupported `format_version`
- Duplicate or regenerated UUIDs breaking pack identity/dependencies
- Missing manifest module/dependency
- Wrong directory name, path case, or identifier namespace
- Stable/Preview API mismatch
- Missing resource references, malformed geometry, texture/UV mismatch
- Pack stacking conflicts
- Script exception during initialization or event handling
- Content requiring a new world or experimental toggle
- Unsupported feature on Android or a particular retail build

## Debug sequence
1. Reproduce on a copied world with only the target packs enabled.
2. Validate JSON syntax and inspect manifest dependencies.
3. Check logs/content errors if the platform exposes them.
4. Disable unrelated packs and test priority/stacking.
5. Reduce the project to the smallest failing example.
6. Test the smallest fix; then regression-test existing behavior.

## Static checks
- Parse every JSON file.
- Search for referenced identifiers and asset paths.
- Verify UUID uniqueness within the project.
- Check archive contents for unexpected nesting such as `MinecraftAddon/MinecraftAddon/manifest.json`.
- Check for duplicate files, absolute paths, secrets, and oversized assets.

## Performance
- Measure on the actual target device.
- Limit per-tick scans, entities, particles, and block writes.
- Cache reusable lookups when safe.
- Batch large world changes and offer progress/cancel where feasible.
- Test memory use and world load/save behavior on mobile.
