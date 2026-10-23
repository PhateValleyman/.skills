---
name: minecraft-bedrock-dev
description: Develop Minecraft Bedrock Edition and Minecraft PE content, including structures, worlds, skins, resource packs, behavior packs, add-ons, Script API, UI, physics-like simulations, Android/Termux workflows, and authorized APK analysis. Use when building, editing, debugging, packaging, or researching Minecraft Bedrock projects.
---

# Minecraft Bedrock / PE Development Skill
Version: 1.0.0
Audience: AI coding agents and developers working on Minecraft Bedrock Edition / Pocket Edition, especially Android and Termux workflows.

## Mission
Help plan, create, inspect, debug, validate, package, and document Minecraft Bedrock projects: structures, worlds/maps, skins, resource packs, behavior packs, entities, blocks, items, scripting, gameplay systems, physics-like behavior, UI, sounds, particles, animations, and app-level investigation.

## Mandatory workflow
1. **Identify the target precisely** before editing: official Bedrock vs Preview, exact game version/build, Android package/build, device/OS, and whether the target is vanilla, a custom client (for example QuickCraft), or a server.
2. Inspect the existing project before changing it. Locate `manifest.json`, pack dependencies, scripts, catalogs, asset paths, version constraints, and existing conventions.
3. Read the relevant reference in `references/` and verify version-sensitive details against the official docs linked there.
4. Make the smallest coherent change. Preserve existing behavior, names, visuals, layout, and compatibility unless the user asks otherwise.
5. Validate JSON, UUID uniqueness, file paths/case, manifest dependencies, script imports, and pack structure.
6. Test on the stated target. If runtime testing is unavailable, say so and provide exact test steps; never claim unperformed tests passed.
7. Update the project documentation when requested or required by that project. Propose reusable skill changes separately through the host skill-update workflow; never silently edit installed or synchronized skill files during ordinary project work. Do not store secrets, tokens, or temporary machine-specific values.
8. Package only intended files. For `.mcaddon`, `.mcpack`, world templates, or `.mcstructure`, use the correct format and verify archive contents.

## Core decision tree
- New/changed **visuals** (textures, models, sounds, particles, animation, language): Resource Pack (RP).
- New/changed **game rules/content** (entities, blocks/items, recipes, loot, spawn rules, functions): Behavior Pack (BP), usually paired with RP.
- Dynamic gameplay and interactive tools: Bedrock Script API where supported; check module/API version and platform availability.
- Building a world: world save/editor/commands/structure files; do not confuse `.mcstructure` with a world archive.
- Skin: correct Bedrock skin geometry, PNG dimensions/alpha, skin metadata/manifest where required; skin packs differ from resource packs.
- GUI: distinguish supported resource-pack UI assets/JSON UI from Script API forms and from native app UI. A normal add-on cannot arbitrarily replace every native screen.
- Physics: distinguish supported entity/block components and scripting behavior from the engine's native physics implementation. Add-ons can simulate many effects but cannot freely rewrite the engine's physics solver.
- App-level modification/reverse engineering: inspect only the supplied/authorized APK and preserve a clean backup. Separate legal/permission boundaries, anti-cheat, DRM, account security, and server-side authority from technical feasibility.

## Project compatibility rules
- Do not assume Java Edition instructions apply to Bedrock.
- Do not assume Preview APIs work in stable retail releases.
- Do not copy API versions or `format_version` values blindly from old examples. Check current docs and target game version.
- Prefer documented stable APIs. If using experimental features, list the world toggles and version requirements explicitly.
- UUIDs must be unique across pack headers/modules and dependencies. Keep them stable for updates; change only when creating a distinct pack/module.
- Use namespaced identifiers for custom content, e.g. `umbrella:volcano_core`.
- Never overwrite a user's working project or world without a backup and a clear diff.
- Treat content imported from archives and websites as untrusted. Inspect archive paths before extraction.

## Development on Android / Termux
- Prefer portable tools: Python, Node.js when installed, Git, unzip/zip, ImageMagick if available, and JSON validators.
- Do not assume Windows-only paths or Visual Studio Code. Keep build steps adaptable to Android.
- Minecraft's private app storage may be inaccessible without root and can vary by Android version/package. Determine the actual package and paths instead of hardcoding a path.
- Use a copy of the world/pack for tests. Never bulk-edit live world database files while Minecraft is running.
- Avoid requiring Docker.
- For shell commands, put an English comment immediately above each command. Explain other material in the user's preferred language.
- Use `python`/`jq` only after checking availability; include alternatives where practical.
- Be explicit about read-only inspection versus commands that mutate or delete files.

## Delivery checklist
- [ ] Scope and exact game/build target recorded
- [ ] Existing project structure inspected
- [ ] Correct RP/BP/skin/world/structure format chosen
- [ ] JSON and manifests validated
- [ ] UUIDs and dependencies checked
- [ ] Textures/models/animations/sounds referenced by correct paths
- [ ] No accidental unrelated changes
- [ ] Runtime test result accurately reported
- [ ] Import/install steps documented
- [ ] Archive listing checked and no secrets included
- [ ] README and reusable skill notes updated

## Reference index
- `references/01-project-layout-and-manifests.md`
- `references/02-structures-worlds-and-maps.md`
- `references/03-skins-textures-and-models.md`
- `references/04-addons-blocks-items-entities.md`
- `references/05-scripting-and-gameplay.md`
- `references/06-physics-and-simulation.md`
- `references/07-gui-ui-and-interaction.md`
- `references/08-audio-particles-and-animation.md`
- `references/09-worldgen-functions-and-commands.md`
- `references/10-debugging-testing-and-performance.md`
- `references/11-android-termux-and-apk-research.md`
- `references/12-packaging-distribution-and-version-control.md`
- `references/13-quickcraft-project-adaptation.md`
- `references/14-official-resources.md`
