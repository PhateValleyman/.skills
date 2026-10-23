# Android, Termux, and APK-level research

## Android workflow
- Record Android version, device ABI, game package name/version, storage layout, root status, and install source.
- Prefer add-on/resource-pack methods before app modification.
- Paths vary by Android version, package name, and install channel. Discover paths on the actual device instead of assuming them.
- Keep backups outside the live game directory; verify available space before extracting large archives.

## APK investigation
For an APK the user owns or is authorized to inspect:
1. Record source, version, package ID, signature information, and SHA-256.
2. Preserve the original APK and work on a copy.
3. Inventory files and manifest; inspect DEX, resources, native libraries, assets, and embedded databases as relevant.
4. Determine whether the requested change belongs in an add-on, resource pack, configuration, or application code.
5. Rebuild/sign only when technically and legally appropriate; explain signature changes and update/install implications.
6. Test offline and online behavior separately when relevant.

## Boundaries
- Do not bypass DRM, payment, account protections, anti-cheat, or access controls.
- Do not extract or expose credentials, session tokens, or private user data.
- Do not present native APK edits as equivalent to supported add-ons.
- Native UI, rendering, physics, and networking changes may require code-level modification and can break with every update.

## Termux practices
- Detect tool availability before relying on it.
- Use safe temporary directories and quote paths.
- Avoid destructive wildcards; preview files before deletion or replacement.
- Explain each shell command with an English comment immediately above it.
- Keep scripts portable and avoid Docker.
