# Module Guide: layout, scripts, Zygisk, WebUI basics, pitfalls

Detailed reference for Magisk modules (Magisk v20 and newer). Read the
sections relevant to the task rather than the whole file.

## Contents

- Overview of supported managers (below)
- 1 Canonical directory layout / ZIP layout
- 2 module.prop rules; 2a platform compatibility
- 3 customize.sh; 4 boot scripts; 5 system/ injection; 6 system.prop; 7 sepolicy.rule
- 8 Version and ABI patterns; 9 Zygisk and Zygisk Next
- 10 update.json and repositories; 11 WebUI (basic); 12 action.sh
- 13 Packaging; 14 Pitfalls; 15 Minimal template
- 16 Bootloop recovery and on-device testing; 17 Play Integrity safety
- Official documentation links

Conflict rule: if this file disagrees with the current upstream documentation
(Magisk Guides), upstream wins; report the difference to the user.

## Overview

This guide covers **installable Magisk modules**. A module is a ZIP that Magisk
installs to `/data/adb/modules/$MODID` and applies with magic mount (bind mounts
over `/system`), boot scripts, `system.prop` and `sepolicy.rule`.

## 1. Canonical Directory Layout

Always generate the **full** directory tree. Never omit required files.

```
$MODID/
├── module.prop           <- REQUIRED — module identity
├── customize.sh          <- optional — runs at install time (sourced, not exec'd)
│
├── system/               <- files overlaid onto /system at boot
│   ├── app/
│   ├── bin/
│   ├── etc/
│   └── ...
│
├── zygisk/               <- Zygisk native libs (only if the module uses Zygisk)
│   ├── arm64-v8a.so
│   ├── armeabi-v7a.so
│   ├── x86.so
│   └── x86_64.so
│
├── post-fs-data.sh       <- blocking early-boot script (use sparingly)
├── service.sh            <- non-blocking late-start script (preferred)
├── action.sh             <- runs when user taps "Action" button in manager UI
├── uninstall.sh          <- cleanup script run on module removal
│
├── system.prop           <- system properties loaded via resetprop
└── sepolicy.rule         <- one SELinux policy statement per line
```

### ZIP layout for installation

```
module.zip
├── META-INF/com/google/android/
│   ├── update-binary     <- copy of module_installer.sh (Magisk recovery flash)
│   └── updater-script    <- must contain exactly: #MAGISK
├── customize.sh
├── module.prop
├── system/
│   └── ...
└── ... (all other module files)
```

---

## 2. module.prop — Required Fields & Rules

```properties
id=my_module_id
name=My Module Name
version=v1.0.0
versionCode=1
author=YourName
description=Short single-line description of what this module does
updateJson=https://example.com/update.json   # optional
```

### Hard rules (enforce all of these):

- `id` **must** match `/^[a-zA-Z][a-zA-Z0-9._-]+$/` — never start with digit or dash.
- `versionCode` **must** be an integer (no quotes, no `v` prefix).
- Every value is a **single line** — no newlines inside values.
- File **must** use **Unix LF** line endings (`\n`), never CRLF or CR.
- Never change `id` after publishing — it is the module's permanent identity.

---

## 2a. Platform Compatibility Reference

| Android version | Magisk |
|---|---|
| 4.2-4.3 | Legacy only |
| 4.4-8.x | Yes |
| 9-16 | Yes |

Set an API floor in `customize.sh` that matches what the module really needs
(see `customize-api.md` for the API table). Verify the current Magisk release
notes before promising support for a new Android version.

## 3. customize.sh — Installation Script

`customize.sh` is **sourced** (not executed) by the installer.

### Critical rules:

- **Never call `exit`** — use `abort "message"` for fatal errors.
- **Never hardcode module paths** — always use `MODDIR=${0%/*}` or `$MODPATH`.
- **Never add a file named `install.sh`** — reserved and will break things.
- `SKIPUNZIP=1` at the top gives you full control; you must then handle all
  file extraction yourself.

For the full variable and function reference, see `references/customize-api.md`.

### Install-time environment checks

```sh
ui_print "- Magisk $MAGISK_VER ($MAGISK_VER_CODE)"
ui_print "- Android API $API, arch $ARCH"
```

Use `MAGISK_VER_CODE` for a minimum Magisk version guard, for example
`[ "$MAGISK_VER_CODE" -ge 24000 ] || abort "! Magisk 24.0 or newer required"`.

### Removing files via REMOVE variable

```sh
REMOVE="
/system/app/Bloatware
/system/fonts/NotoSerif.ttf
"
```

### Replacing directories via REPLACE variable

```sh
# Magisk: creates a .replace file inside the dir
REPLACE="
/system/app/YouTube
"
```

---

## 4. Boot Scripts - Execution Stages

| Script | Mode | Blocking | When |
|---|---|---|---|
| `post-fs-data.sh` | post-fs-data | YES (40 s max) | Before modules mount, before Zygote |
| `service.sh` | late_start | NO | After boot, parallel to system |
| `action.sh` | on-demand | - | User taps Action in Magisk app |
| `uninstall.sh` | on removal | - | Module uninstalled |

### Script best practices

```sh
#!/system/bin/sh
# Always derive MODDIR dynamically - never hardcode
MODDIR=${0%/*}

# Use resetprop, NOT setprop (setprop deadlocks in post-fs-data)
resetprop -n ro.debuggable 1

# Always use MODDIR for relative paths
cp "$MODDIR/myfile" /data/local/tmp/
```

BusyBox is at `/data/adb/magisk/busybox`. Magisk scripts already run with it in
PATH in its standalone mode; reference the absolute path only when needed.

### post-fs-data.sh - use only when truly necessary

```sh
#!/system/bin/sh
# BLOCKING - keep this script fast
# WARNING: setprop DEADLOCKS here - use resetprop -n instead
MODDIR=${0%/*}
resetprop -n persist.sys.timezone "Africa/Nairobi"
```

### service.sh - preferred for most use cases

```sh
#!/system/bin/sh
# NON-BLOCKING - safe to do heavier work here
MODDIR=${0%/*}
# Wait for boot to complete if needed (add a timeout for production modules)
while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 1
done
# Your logic here
```

## 5. system/ Directory - File Injection Rules

Magisk magic mount bind-mounts files in `system/` over their counterparts.

- To **replace a directory entirely**: create a `.replace` file inside it (the `REPLACE` variable does this for you).
- To **delete** a file: `mknod $MODPATH/system/path/to/file c 0 0` (whiteout), or use the `REMOVE` variable.
- A module with no `system/` content and no need for mounting should contain an empty `skip_mount` file.

### Vendor / product / system_ext

```
system/vendor/...     -> /vendor
system/product/...    -> /product
system/system_ext/... -> /system_ext
```

Verify the actual partition layout on the target device before placing files.

## 6. system.prop

```properties
# Loaded via resetprop at boot
# Format identical to build.prop
ro.adb.secure=0
persist.sys.usb.config=mtp,adb
debug.sf.hw=1
```

Rules:
- One `key=value` per line, Unix LF.
- Use `ro.` prefix for read-only props; use `persist.` for persistent props.
- Props here are set with `resetprop -n` (pre-Zygote) and again with `resetprop`
  (no `-n`) post-boot. The `-n` flag skips native property callbacks.

---

## 7. sepolicy.rule

```
# One policy statement per line
# Uses magiskpolicy syntax (supolicy language)
allow untrusted_app shell_exec:file execute
allow system_server myservice:unix_stream_socket connectto
```

Useful references:
- `allow <source> <target>:<class> <permission>`
- `auditallow`, `dontaudit`, `neverallow` follow same syntax.
- Test rules with: `magiskpolicy --test --apply sepolicy.rule`

---

## 8. Version and ABI Patterns

### Pattern: ABI-conditional install

```sh
# customize.sh
case "$ARCH" in
    arm64) ABI_DIR="arm64-v8a" ;;
    arm)   ABI_DIR="armeabi-v7a" ;;
    x64)   ABI_DIR="x86_64" ;;
    x86)   ABI_DIR="x86" ;;
esac
ui_print "- Installing $ARCH ($ABI_DIR) binaries"
cp "$TMPDIR/libs/$ABI_DIR/libmymod.so" "$MODPATH/system/lib64/"

# API level guard - adjust the floor to match your module
if [ "$API" -lt 29 ]; then
    abort "! Android 10 (API 29) or higher required"
fi
```

### Pattern: logging from service.sh

```sh
#!/system/bin/sh
MODDIR=${0%/*}
echo "[mymod] service started" >> /data/local/tmp/mymod.log
```

Keep logs under `$MODDIR`, `/data/local/tmp/` or your own `/data/<namespace>/`
directory. Never log secrets.

## 9. Zygisk

Place compiled `.so` libraries under `zygisk/`:

```
zygisk/
├── arm64-v8a.so
├── armeabi-v7a.so
├── x86.so
├── x86_64.so
└── unloaded     <- create this file to mark libs as incompatible/disabled
```

Build against the upstream Zygisk module sample, match the ABIs you ship, and
check symbols, linker dependencies and NDK version. Never ship an empty `.so`.
Document that Zygisk must be enabled in Magisk settings.

### Zygisk Next

[Zygisk Next](https://github.com/Dr-TSNG/ZygiskNext) is a standalone module that
provides the Zygisk API as a replacement for Magisk's built-in Zygisk. Users who
run it keep Magisk's own Zygisk switched off.

- The `zygisk/` directory layout of your module is identical in both cases; no
  changes are needed in your module.
- State in `module.prop` description and in the README whether your module needs
  Zygisk, and that it works with either built-in Zygisk or Zygisk Next.
- Do not enable both providers at once; document this for users.
- Verify the current Zygisk Next requirements and release notes upstream before
  promising compatibility with a specific version.

## 10. Update JSON and Module Repository Publishing

### update.json (OTA self-update)

```json
{
    "version": "v1.2.0",
    "versionCode": 120,
    "zipUrl": "https://example.com/releases/mymod-v1.2.0.zip",
    "changelog": "https://example.com/releases/changelog.md"
}
```

Reference this URL in `module.prop`:
```
updateJson=https://example.com/mymod/update.json
```

### Publishing via MMRL-compatible repositories

The Magisk online module repository is inactive. Active repositories as of 2025:

| Repository | URL | Notes |
|---|---|---|
| MMRL module repo (Androidacy AMR) | https://repo.androidacy.com | Most widely used; MMRL default |
| MMAR (Magisk Module Alt Repo) | https://github.com/Magisk-Modules-Alt-Repo | GitHub-based; open submissions |
| MMRL itself | https://github.com/MMRLApp/MMRL | The app; hosts a repo index |

To submit to MMAR: fork the repo, add your module entry to the index JSON, and open a pull request. MMRL will pick it up automatically from the index.

For Androidacy AMR, follow the submission process at `https://www.androidacy.com/module-repository/`.

---

## 11. WebUI (optional)

A module can ship a web settings page that MMRL opens in its module view.

```
$MODID/
└── webroot/
    ├── index.html       <- entry point
    ├── style.css        <- optional
    └── main.js          <- optional
```

For the bridge API, Promise wrappers, WebUI X `config.json`, permissions, CSP
and troubleshooting, use `webui-bridge-api.md`, `webui-patterns.md`,
`webui-x-reference.md` and `webui-troubleshooting.md`. Scaffold with
`scripts/scaffold-webui.sh`.

Rules:
- Use relative URLs and bundle all assets locally.
- Feature-detect the bridge; the page must degrade gracefully when it is absent
  (desktop browser, host without WebUI).
- Always check the exit code of a command and show stderr to the user.

## 12. Action Button (action.sh and WebUI trigger)

`action.sh` runs when the user taps the "Action" button in the Magisk app.
Use it for one-shot operations: toggle a feature, force-apply settings, clear
a cache, or run a diagnostic.

### action.sh patterns

```sh
#!/system/bin/sh
# Runs as root when user taps Action in the manager UI
MODDIR=${0%/*}

# Pattern 1: Toggle a flag file
FLAG="$MODDIR/flags/feature_enabled"
if [ -f "$FLAG" ]; then
    rm "$FLAG"
    # Output is shown in the Magisk app's action output
    echo "Feature disabled."
else
    mkdir -p "$MODDIR/flags"
    touch "$FLAG"
    echo "Feature enabled."
fi

# Pattern 2: Apply a setting immediately without reboot
resetprop ro.example.setting 1
echo "Property applied."

# Pattern 3: Collect a diagnostic log and place it where the user can find it
LOGFILE="/sdcard/mymod-diag-$(date +%Y%m%d-%H%M%S).txt"
{
    echo "=== My Module Diagnostic ==="
    echo "Date: $(date)"
    echo "Magisk: $MAGISK_VER"
    getprop | grep "ro.build"
    cat /proc/mounts | grep "$MODID"
} > "$LOGFILE"
echo "Log saved to $LOGFILE"
```

### Triggering action.sh from WebUI

Use the `exec()` Promise wrapper from `webui-bridge-api.md`:

```javascript
document.getElementById("run-action").addEventListener("click", async () => {
  const r = await exec("sh /data/adb/modules/my_module/action.sh");
  showMessage(r.errno === 0 ? r.stdout.trim() : "Action failed: " + r.stderr.trim());
});
```

**Notes:**
- Keep `action.sh` output short, one or two lines.
- Do not run long-blocking operations in `action.sh`. For heavy work, spawn a
  background process and return immediately.
- Never depend on execution order between `action.sh` and `service.sh`.

---

## 13. Packaging the ZIP

For an ordinary source ZIP, use `scripts/pack-module.sh <module-dir> [out.zip]`. It does not overwrite an existing archive, package obvious local credentials, or install/flash a device. A recovery-flashable ZIP is a separate, version-sensitive format; follow current official Magisk documentation and use reviewed, pinned installer files. Do not fetch a moving `master` installer during a build. See `references/build-reference.md`.

---

## 14. Common Pitfalls & Forbidden Patterns

| Don't do this | Do this instead |
|---|---|
| `exit 1` in customize.sh | `abort "reason"` |
| `echo "msg"` in install scripts | `ui_print "msg"` |
| Hardcode `/data/adb/modules/mymod` | Use `$MODDIR` or `$MODPATH` |
| `setprop` in post-fs-data | `resetprop -n key value` |
| Create `install.sh` in ZIP | Use `customize.sh` only |
| Modify `update-binary` with custom logic | It gets overwritten by Magisk app |
| Mix CRLF line endings in scripts | Always use LF (`\n`) |
| `id` starting with a digit or dash | Must match `^[a-zA-Z][a-zA-Z0-9._-]+$` |
| Call `su` from inside module scripts | Scripts already run as root |
| Use `/sbin` paths for Magisk tmpfs | Use `${MAGISKTMP}` in rc scripts |
| Module has no system/ folder but no skip_mount flag | Create an empty file named `skip_mount` at the module root |

---

## 15. Minimal Module Template

A plain module may need only `module.prop` and the module payload. Add installer or boot scripts only when the feature requires them; a no-op `customize.sh` or `service.sh` is not a requirement.

### module.prop
```properties
id=my_module
name=My Module
version=v1.0.0
versionCode=1
author=Author
description=What this module does
```

For an installer, use the Magisk-supported `customize.sh` API and never call `exit` from the sourced script. For a boot-time action, add the appropriate script only when necessary, derive its directory from `$0`, keep it idempotent and non-blocking, and document recovery/uninstall behavior.

---

## 16. Bootloop Recovery and On-Device Testing

Bootloops are the most common failure mode for module hobbyists. Always include
this information in any generated README.

### Disabling a broken module without boot

If a module causes a bootloop, the user can disable it before Android finishes
booting:

```
Method 1 - Volume key safe mode (Magisk):
  Hold Volume Down while the boot animation plays. Magisk will disable all
  modules for that boot only.

Method 2 - Create a disable file:
  Boot into TWRP or another recovery. Create an empty file at:
  /data/adb/modules/<MODID>/disable
  Magisk will skip loading that module on next boot.

Method 3 — Delete the module folder:
  Boot into recovery. Delete /data/adb/modules/<MODID>/ entirely.
```

Always document Method 2 in your module's README so users can recover without
wiping.

### Testing a module on-device before releasing

The commands below are for a device and module the user is authorized to test. Confirm the exact device/serial, test data, and expected data-loss/reboot implications first. Do not run them against a personal, production, or third-party device without explicit scoped approval; skip on-device testing if not authorized.

```sh
# Install directly via Magisk CLI (no app UI needed)
magisk --install-module /path/to/module.zip

# Watch Magisk and module-related logs during boot
adb logcat -s Magisk | tee /tmp/magisk-boot.log

# Check if your module is loaded
ls /data/adb/modules/

# Verify bind-mount is active (Magisk magic mount)
cat /proc/mounts | grep "$MODID"

# Verify resetprop changes took effect
getprop ro.debuggable

# Check for SELinux denials caused by your module
adb logcat | grep "avc: denied"
```

### Safe test cycle before publishing

1. Flash the module ZIP in the manager app.
2. Reboot and capture `adb logcat -s Magisk` for the full boot sequence.
3. Verify your target files are present under the bind-mount tree.
4. Test intended functionality (the actual reason for the module).
5. Verify no unexpected SELinux denials in logcat.
6. Test uninstall: remove the module, reboot, confirm clean state.
7. Test on a second device or Android version if possible.

---

## 17. App/service integrity and compatibility

Systemless modifications, root access, property changes, injected code, or boot-image changes can affect app/service integrity decisions, banking/payment apps, updates, DRM, and device security. Results vary by app and Android/device version; do not promise that a configuration will pass checks.

This guide does not provide instructions or dependencies for spoofing device identity/attestation, hiding root from apps, defeating anti-cheat, or bypassing payment, licensing, or integrity controls. Do not write to Google Play Services data. For legitimate module development, test only on an authorized device/account, document the exact tested build and observed limitations, and use vendor-supported test configurations where available.

---

## References

### Official documentation

- Magisk Developer Guides: https://topjohnwu.github.io/Magisk/guides.html
- Magisk module_installer.sh: https://github.com/topjohnwu/Magisk/blob/master/scripts/module_installer.sh
- Zygisk Module Sample: https://github.com/topjohnwu/zygisk-module-sample
- Zygisk Next: https://github.com/Dr-TSNG/ZygiskNext
- MMRL App: https://github.com/MMRLApp/MMRL
- Magisk Modules Alt Repo (MMAR): https://github.com/Magisk-Modules-Alt-Repo

### Skill references

- `customize-api.md` — variable and function reference for customize.sh
- `build-reference.md` — hardened build script with dependency checks
- `module-recipes.md` — templates for common module archetypes
- `module-engineering.md` — Magisk-first engineering and verification checklist
