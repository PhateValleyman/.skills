# Build Reference — Packaging a Module ZIP

## Ordinary module ZIP

Use `scripts/pack-module.sh <module-dir> [out.zip]` for a reviewed source ZIP. It validates module metadata, shell syntax and line endings, rejects common credential/local-config files and symlinks, and refuses to overwrite an existing output or write into its source tree. Review the archive contents. It does **not** install or flash the module.

## Recovery-flashable ZIPs

A recovery-flashable package may require manager-specific `META-INF` files, but the correct installer and format depend on the current Magisk release and target recovery. Do not download `module_installer.sh` from a moving `master` branch or run fetched code. Use current official Magisk documentation/source for a pinned release or commit, verify provenance and contents, and review the files before packaging. If exact compatibility cannot be established, label the artifact as an ordinary source ZIP, not recovery-flashable.

## Safe build practices

- Keep signing keys, `.env` files, access tokens, local build properties and private certificates outside the module source/archive.
- Pin tool/source versions where possible; do not embed install-time network fetches by default.
- Packaging success is not evidence that a module is safe or device-compatible.
- Installation, rebooting, bootloader changes and flashing are separate high-impact actions that require explicit approval for the exact device.
