# MMRL-specific notes

Precedence: where this file differs from `webui-x-reference.md` or `mmrl-ops-build.md` (which cite current mmrl.dev docs), those two win. This file keeps the older `window.ksu` bridge strategy.

MMRL (Magisk Module Repo Loader, by DerGoogler) can open a module's WebUI and exposes the `window.ksu` bridge (the bridge name is historical). MMRL also ships extra capabilities in its own "WebUI X" implementation; treat them as optional and feature-detect.

## Compatibility strategy
1. Write against `window.ksu` (the bridge MMRL injects).
2. Optionally enhance when MMRL-only objects exist (check for their presence at runtime; do not hard-depend on them).
3. Keep `webroot/index.html` self-contained so any manager can open it.

## Repository metadata (for publishing in an MMRL-compatible repo)
- `module.prop` fields: `id, name, version, versionCode, author, description`.
- Optional `updateJson=<https url>` pointing to a JSON like:
```json
{
  "version": "v1.2.0",
  "versionCode": 120,
  "zipUrl": "https://example.com/mymodule-v1.2.0.zip",
  "changelog": "https://example.com/changelog.md"
}
```
- Repo index formats (`modules.json`, `track.json`) are defined by the repository software you use (e.g. MMRL's own Repo/"magisk-modules-repo" tooling). Check that project's docs for the current schema before generating them: the schema evolves.

## Verification note
Details of MMRL-only interfaces and the repo index schema change between releases and could not be verified offline when this skill was written. If the task depends on them, consult the current MMRL docs/source (github.com/MMRLApp, DerGoogler) before relying on specifics.
