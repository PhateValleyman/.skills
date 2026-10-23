---
name: magisk-skill
description: "Magisk module lifecycle and MMRL/WebUI X work: design, implement, debug, and package Magisk modules; module.prop, installer/boot scripts, systemless overlays, ZIPs, recovery, and WebUI. Use for these requested tasks or MMRL repository/build work. Do not use for general Android app development, standalone Xposed/LSPosed, other root managers, or kernel compilation."
license: MIT
---

# Magisk Modules and MMRL WebUI

One skill for the whole module lifecycle: design, scaffold, implement, package,
verify, publish, plus the WebUI that ships inside a module.

## 1. Classify the request first

| The user wants... | Branch | Read |
|---|---|---|
| A module that changes files, props, SELinux, boot behavior | **Module** | `references/module-guide.md`, `references/module-engineering.md` |
| A known archetype (props only, debloater, font, audio, performance) | **Module recipe** | `references/module-recipes.md` |
| Variables/functions inside customize.sh | **Installer API** | `references/customize-api.md` |
| ZIP creation, `META-INF`, build script | **Packaging** | `references/build-reference.md`, `scripts/pack-module.sh` |
| A settings page / GUI inside a module (`webroot/`) | **WebUI** | section 4 below |
| MMRL repo index, `MMRL-Util`, publishing, building the MMRL/WebUI X app | **MMRL ops** | `references/mmrl-ops-build.md` |
| A module that bootloops, fails to install, or breaks Play Integrity | **Debug** | `references/module-guide.md` sections 14, 16, 17 |

A request can span branches (module plus WebUI). Do the module branch first, then WebUI.

## 2. Workflow

1. **Scope.** Establish: minimum Magisk version, Android API floor, ABI, whether Zygisk is needed, what the module changes (files, props, SELinux, runtime script), and whether to only build a ZIP or also install.
2. **Inspect existing work.** If a project exists, keep its `id`, structure and conventions. Do not claim device testing that did not happen.
3. **Choose the smallest design.** Prefer systemless overlay, a script, or declarative files. Do not add `sepolicy.rule`, `system.prop`, Zygisk libraries or binaries without a stated need. Never disable SELinux as a shortcut. Route archetypes through `module-recipes.md` and add only the files the recipe lists.
4. **Scaffold.** Start from `assets/module-minimal/` (plain module) or `assets/webui-starter/` (module with WebUI, via `scripts/scaffold-webui.sh`). Omit optional scripts that are not needed.
5. **Implement** under the hard rules in section 3.
6. **Verify.** Run `scripts/pack-module.sh <dir>`; it checks metadata, line endings, shell syntax, `webroot/index.html`, likely credential files/symlinks, and ZIP root layout; it will not overwrite an existing ZIP. Then walk the pitfalls table (`module-guide.md` section 14).
7. **Hand over.** State target manager and version, what the module changes, how to disable or uninstall it (bootloop recovery, `module-guide.md` section 16), and what was not tested. Building a ZIP is not permission to flash or reboot a device. Never leave a generic root-shell or arbitrary-command WebUI in a deliverable.

## 3. Hard rules

- Verify variables, hooks and version assumptions against current upstream docs (Magisk Guides, mmrl.dev) before relying on them. Upstream wins over this skill; report differences.
- `module.prop` is required: `id` matches `^[a-zA-Z][a-zA-Z0-9._-]+$`, `versionCode` is an integer, one line per value, LF endings. Never change a published `id`.
- `customize.sh` is sourced: use `ui_print` and `abort`, never `exit`. Never create `install.sh`. Never put custom logic in `update-binary`.
- Boot scripts: derive `MODDIR=${0%/*}`; never hardcode `/data/adb/modules/<id>`. Prefer `service.sh`. `post-fs-data.sh` is blocking and early: keep it short and use `resetprop -n`, never `setprop`.
- Destructive overlay features (`.replace`, `REPLACE`, `REMOVE`, whiteouts) only when the request clearly needs them. Debloaters use `REMOVE`, not `mknod`.
- Do not implement or recommend attestation spoofing, root-hiding, or bypasses of integrity/anti-cheat controls. Never write to GMS data paths; document compatibility limitations without evasion steps.
- ZIP root contains the module files directly (no wrapping project folder). Keep execute bits on scripts. No `.git`, keys, tokens, cache or `local.properties` inside the ZIP.
- Target Magisk only. If the user asks for another root manager, say it is out of scope for this skill.

## 4. WebUI branch (webroot)

Identify the host first: MMRL WebUI X or WebUI X Portable. Do not treat a plain Android WebView and MMRL WebUI X as identical.

1. Scaffold: `scripts/scaffold-webui.sh` with a module directory, ID, and display name (uses `assets/webui-starter/`, a static, inert browser-preview page). For a static page without any bridge use `assets/webui-static/` (adds MMRL insets/colors CSS and a `config.mmrl.json.example`).
2. Implement. Bridge API and Promise wrappers: `references/webui-bridge-api.md`. Recipes (config read/write, service toggle, logs, shell quoting): `references/webui-patterns.md`. WebUI X `config.json`, permissions, CSP, themes, events, DevTools, Portable patching: `references/webui-x-reference.md`. MMRL bridge compatibility: `references/mmrl-compat-notes.md`.
3. Test statically (JSON/HTML/JS), then in a desktop browser as a static page, then in the real host. Symptom table: `references/webui-troubleshooting.md`.
4. Package with `scripts/pack-module.sh`.

WebUI rules:
- Entry point is `webroot/index.html`; use relative URLs, bundle assets locally, assume no internet.
- Quote every user-supplied value in shell commands (`shq()` in `webui-patterns.md`); use allowlists; never build commands from raw UI text.
- Request the minimum WebUI X permissions; keep default CSP; do not widen either just to silence an error.
- Show stderr and exit code to the user; confirm destructive actions.
- Persist user data under `/data/adb/<id>/`, not inside the module directory and not in `localStorage` alone.
- Use `https://mui.kernelsu.org/internal/` CSS paths (the older `/mmrl/` paths are deprecated; the host name is historical); apply safe-area insets only to fixed or absolute edge elements.
- Feature-detect bridge members (`window.ksu?.fullScreen`) and WebUI X events; support varies by host and version.

## 5. MMRL ops and app builds

Repo `config.json` (repo level) is not `webroot/config.json` (module level). Use `mmrl-util --help` before commands since the CLI changes. Building the MMRL or WebUI X Portable APK is a Gradle task, separate from module ZIP packaging; follow `references/mmrl-ops-build.md` and never include keystores in shared archives.

## 6. Deliverables

- Give the final ZIP (and sources if requested) with a short install and test note: flash in the manager, reboot if boot scripts or overlay changed, open the WebUI from the manager.
- List files changed, compatibility, permissions requested, and untested parts.
- `references/qa-checklist.md` is the quality checklist for this skill and its output; consult it when reviewing or extending the skill.

## Resource map

- `references/module-guide.md` - full module reference (17 sections, includes bootloop recovery and Play Integrity)
- `references/module-engineering.md` - Magisk-first engineering and verification checklist
- `references/module-recipes.md`, `customize-api.md`, `build-reference.md`
- `references/webui-x-reference.md`, `webui-bridge-api.md`, `webui-patterns.md`, `webui-troubleshooting.md`, `mmrl-compat-notes.md`, `mmrl-ops-build.md`
- `scripts/scaffold-webui.sh`, `scripts/pack-module.sh`
- `assets/module-minimal/`, `assets/webui-starter/`, `assets/webui-static/`
