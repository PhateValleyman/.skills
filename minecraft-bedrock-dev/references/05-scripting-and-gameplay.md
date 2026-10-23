# Script API and gameplay systems

## Before coding
- Check current stable Script API documentation for the exact target version.
- Confirm module dependency names/versions in `manifest.json`.
- Separate stable APIs from beta/experimental APIs.
- Avoid relying on undocumented internals or assumptions from older versions.

## Design principles
- Use event-driven logic where possible rather than expensive polling.
- Keep tick handlers short; batch block operations and add limits/cooldowns.
- Guard optional APIs and invalid entities/blocks; handle unloaded chunks and dimension changes.
- Use namespaces and small modules; avoid a single giant `main.js`.
- Persist only necessary state and document reset/migration behavior.
- Use player forms for supported menus/dialogues; check cancellation and invalid player/session state.
- Do not assume client-only UI or local state is authoritative in multiplayer.

## Typical systems
- Custom tools and interactions
- Structure placement/move/remove previews
- Teleport/waypoint systems
- Quest and dialogue systems
- Custom progression, loot, and economy
- NPC interactions and scripted events
- Procedural building and world scanning
- Scoreboard-based state, where appropriate
- Admin/debug commands with permission checks

## Reliability
- Log initialization and caught errors with actionable context.
- Avoid swallowing exceptions silently.
- Validate all user-controlled inputs and coordinate ranges.
- Test with two players when multiplayer semantics matter.
