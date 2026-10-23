# Packaging, distribution, and version control

## Packaging
- `.mcpack`: usually one pack; `.mcaddon`: usually one or more add-on packs; `.mcworld`: world archive; `.mcstructure`: structure data. Confirm current import conventions.
- Archive the *contents* at the correct root level; avoid accidental extra directory nesting.
- Use the required file extension only after confirming the internal structure.
- List archive contents and check for required manifests and assets.
- Import into a disposable world/device and verify the pack appears and activates.

## Versioning
- Keep stable pack UUIDs across updates.
- Increment pack version when releasing changes; update dependencies consistently.
- Maintain a changelog with breaking changes, API requirements, known limitations, and test platform.
- Use Git for text assets and source. Large binaries may need Git LFS or separate release assets; don't commit private world saves unless intended.

## Release checklist
- Clear name and description
- Unique IDs and valid dependencies
- License/attribution
- Supported game version stated
- Install/import steps
- Test report and known limitations
- No secrets, private saves, debug dumps, or unrelated files
