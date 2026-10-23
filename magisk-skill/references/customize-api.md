# customize.sh API Reference

Variables and functions available when `customize.sh` is sourced by the module
installer. All variables are read-only unless noted otherwise.

---

## Available variables

| Variable | Type | Description |
|---|---|---|
| `MODPATH` | path | Where module files should be installed |
| `TMPDIR` | path | Temporary scratch space |
| `ZIPFILE` | path | Path to the installer ZIP |
| `ARCH` | string | `arm`, `arm64`, `x86`, `x64` |
| `IS64BIT` | bool | `true` if arm64 or x64 |
| `API` | int | Android API level (e.g. `34` = Android 14) |
| `BOOTMODE` | bool | `true` if installed via manager app (not recovery) |
| `MAGISK_VER` | string | Magisk version string  |
| `MAGISK_VER_CODE` | int | Magisk version code  |

---

## Available functions

```sh
ui_print <msg>
# Print a message to the install console. Use this instead of echo.

abort <msg>
# Print an error message and stop installation immediately.
# Use this instead of exit for all fatal errors.

set_perm <target> <owner> <group> <perm> [context]
# Set ownership, permissions, and optional SELinux context on a file.

set_perm_recursive <dir> <owner> <group> <dirperm> <fileperm> [context]
# Recursively set ownership, permissions, and optional context on a directory.
```

---

## Android API level reference

Use these values in API guard checks. Always include the Android version name
in the `abort` message so users understand the requirement.

| API | Android version |
|---|---|
| 26 | Android 8.0 (Oreo) |
| 27 | Android 8.1 (Oreo MR1) |
| 28 | Android 9 (Pie) |
| 29 | Android 10 |
| 30 | Android 11 |
| 31 | Android 12 |
| 32 | Android 12L |
| 33 | Android 13 |
| 34 | Android 14 |
| 35 | Android 15 |
| 36 | Android 16 |

Example guard with correct message format:

```sh
if [ "$API" -lt 30 ]; then
    abort "! Android 11 (API 30) or higher required"
fi
```

---

## Notes

- `MODPATH` is the definitive install destination in customize.sh.
  Use `MODDIR=${0%/*}` in boot scripts, where `MODPATH` is not set.
