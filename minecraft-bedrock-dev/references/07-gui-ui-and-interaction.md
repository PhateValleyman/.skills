# GUI, UI, menus, and interaction

## Three separate layers
1. **Script-driven UI:** forms/dialogs exposed by supported Script API modules.
2. **Resource-pack UI:** JSON UI and related assets, subject to version/platform constraints and possible breakage.
3. **Native application UI:** account login, settings, store, pause screens, and other engine-owned screens. Ordinary add-ons cannot freely replace all native UI.

## Workflow
- Clarify whether the target is an in-world menu, Script API form, HUD overlay, inventory UI, main menu, or native login screen.
- Prefer supported forms for reliable menus; use resource-pack UI only after checking target version and current constraints.
- Inspect existing JSON UI definitions and vanilla references for the exact target build.
- Preserve original identifiers and bindings unless the change specifically requires replacing them.
- Test resolution scaling, touch controls, controller input, localization, accessibility, and pack stacking.

## UI engineering
- Keep layout responsive; avoid fixed pixel assumptions across devices.
- Verify icon paths, atlas names, anchors, offsets, z-order, bindings, and visibility conditions.
- Add fallback behavior when a custom UI asset fails to load.
- Treat undocumented UI hooks as fragile and version-specific.
- Do not use UI modification to impersonate Microsoft sign-in or collect credentials.
