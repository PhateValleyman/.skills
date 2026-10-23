# Module Recipes — Canonical Templates for Common Archetypes

Route here from SKILL.md workflow when the user's request matches a known archetype.
Each recipe produces the minimum correct file set for that type. Do not add
files the archetype does not need.

---

## How to use this file

1. Identify the archetype from the user's request.
2. Use the recipe's file list — do not add `service.sh` or `post-fs-data.sh`
   unless the recipe includes them.
3. Fill in the recipe template, then apply all hard rules from module-guide.md §2–§7.
4. Run the pitfalls check (module-guide.md §14) before delivering output.

---

## Archetype 1 — Prop-Only Module

**What it does:** Changes system properties via `system.prop` only.
No file injection, no boot scripts.

**Files needed:** `module.prop`, `system.prop`
**Files NOT needed:** `customize.sh`, `service.sh`, `post-fs-data.sh`, `system/`

### module.prop
```properties
id=my_props_mod
name=My Props Module
version=v1.0.0
versionCode=1
author=Author
description=Patches system properties at boot
```

### system.prop
```properties
# Props set via resetprop at early boot
# One key=value per line; Unix LF only
ro.example.prop=value
persist.example.setting=1
```

**Notes:**
- Props in `system.prop` are applied with `resetprop -n` (pre-Zygote). They
  take effect before most services start.
- No `service.sh` or `post-fs-data.sh` is needed. The installer handles loading
  `system.prop` automatically.
- If a prop needs to be set after boot (e.g., requires a service to exist),
  use `service.sh` with `resetprop key value` instead.

---

## Archetype 2 — Debloater Module

**What it does:** Removes or replaces system apps and files without touching
the real filesystem (systemless).

**Files needed:** `module.prop`, `customize.sh`
**Files NOT needed:** `service.sh`, `system.prop`, `post-fs-data.sh`

### module.prop
```properties
id=my_debloater
name=My Debloater
version=v1.0.0
versionCode=1
author=Author
description=Removes selected system apps systemlessly
```

### customize.sh
```sh
# Sourced by installer — do NOT call exit

ui_print "- My Debloater installing..."

# List paths to remove (relative to /system)
REMOVE="
/system/app/Facebook
/system/app/Netflix
/system/priv-app/GoogleFeedback
"

# List directories to replace entirely (replaces dir contents with yours)
# Only set REPLACE if you are providing replacement files in system/
# REPLACE="/system/app/SomeApp"

ui_print "- Done."
```

**Notes:**
- The `REMOVE` variable is the correct pattern. Do NOT use `mknod` whiteouts
  in customize.sh — `REMOVE` is supported by Magisk.
- Test the target app paths on the device before hardcoding; paths vary by OEM.
- Some protected system apps require additional SELinux rules to remove cleanly.
  If the app persists after removal, check logcat for SELinux denials.

---

## Archetype 3 — Font Injection Module

**What it does:** Replaces system fonts by overlaying files under
`system/fonts/` and patching `system/etc/fonts.xml` or its equivalent.

**Files needed:** `module.prop`, `customize.sh`, `system/fonts/`, `system/etc/fonts.xml`
**Files NOT needed:** `service.sh`, `post-fs-data.sh`, `system.prop`

### module.prop
```properties
id=my_font_mod
name=My Font Mod
version=v1.0.0
versionCode=1
author=Author
description=Replaces system fonts with custom typefaces
```

### Directory structure
```
system/
├── fonts/
│   ├── MyFont-Regular.ttf
│   ├── MyFont-Bold.ttf
│   └── ...
└── etc/
    └── fonts.xml     <- patched fonts config
```

### customize.sh
```sh
# Sourced by installer — do NOT call exit

ui_print "- Font Mod installing..."

# API guard — fonts.xml format changed at API 29
if [ "$API" -lt 26 ]; then
    abort "! Android 8.0 (API 26) or higher required"
fi

ui_print "- Architecture: $ARCH | API: $API"
ui_print "- Installing fonts..."

# Permissions: fonts must be readable by all
set_perm_recursive "$MODPATH/system/fonts" root root 0755 0644

ui_print "- Done."
```

**Notes:**
- `fonts.xml` format differs between Android versions. Provide the correct
  format for your target API range and document the tested versions.
- On Android 12+, system fonts may also be registered via the
  `FontManager` API. The file-injection approach still works for most apps.
- Do not replace `DroidSansFallback.ttf` (CJK fallback) unless you are
  providing a CJK-capable replacement — its removal causes UI breakage.
- Always set 0644 permissions on `.ttf` files. Wrong permissions cause
  silent font fallback to the default with no visible error.

---

## Archetype 4 — Audio Driver / Effect Module

**What it does:** Installs audio effects, HAL configs, or audio policy files
to modify the audio pipeline.

**Files needed:** `module.prop`, `customize.sh`, `system/`, `service.sh` (usually), `sepolicy.rule` (often)
**Files NOT needed:** `post-fs-data.sh`

### module.prop
```properties
id=my_audio_mod
name=My Audio Mod
version=v1.0.0
versionCode=1
author=Author
description=Installs custom audio effects and policy
```

### Directory structure
```
system/
├── lib/
│   └── soundfx/
│       └── libmyeffect.so        <- 32-bit effect library
├── lib64/
│   └── soundfx/
│       └── libmyeffect.so        <- 64-bit effect library
└── etc/
    ├── audio_effects.xml         <- registers the effect
    └── audio_policy_configuration.xml  <- optional, if patching routing
```

### customize.sh
```sh
# Sourced by installer — do NOT call exit

ui_print "- Audio Mod installing..."

# Install architecture-correct library
case "$ARCH" in
    arm64) LIB_SRC="arm64-v8a" ;;
    arm)   LIB_SRC="armeabi-v7a" ;;
    x64)   LIB_SRC="x86_64" ;;
    x86)   LIB_SRC="x86" ;;
esac

mkdir -p "$MODPATH/system/lib64/soundfx"
cp "$TMPDIR/libs/$LIB_SRC/libmyeffect.so" \
   "$MODPATH/system/lib64/soundfx/libmyeffect.so"

set_perm "$MODPATH/system/lib64/soundfx/libmyeffect.so" root root 0644 \
    u:object_r:system_file:s0

ui_print "- Done. Reboot to activate."
```

### service.sh
```sh
#!/system/bin/sh
MODDIR=${0%/*}

# Wait for audioserver to be ready before reloading effects
while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 1
done

# Signal audioserver to reload effects (if supported by ROM)
# Some ROMs require a full reboot — document this if so
pkill -HUP audioserver 2>/dev/null || true
```

### sepolicy.rule
```
# Allow audioserver to load your effect library from the module path
allow audioserver system_file:file { read open execute }
```

**Notes:**
- `audio_effects.xml` registration format varies by Android version and OEM.
  Test with `dumpsys media.audio_flinger` to verify the effect is loaded.
- Some audio HAL configs are device-specific. Document supported devices.
- Play Integrity risk: low for audio modules unless you hook GMS audio paths.

---

## Archetype 5 — Performance / Sysctl Module

**What it does:** Applies kernel sysctl tuning and I/O scheduler changes at
boot via `service.sh` or `system.prop`.

**Files needed:** `module.prop`, `service.sh` (for sysctl), `system.prop` (for props)
**Files NOT needed:** `customize.sh` (unless conditional install needed), `system/`

### module.prop
```properties
id=my_perf_mod
name=My Performance Mod
version=v1.0.0
versionCode=1
author=Author
description=Applies kernel sysctl and I/O scheduler tuning at boot
```

### service.sh
```sh
#!/system/bin/sh
MODDIR=${0%/*}

# Wait for full boot before applying — avoids race conditions with init
while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 1
done

# I/O scheduler tuning — change to match your target storage type
for block in /sys/block/sd*/queue/scheduler \
             /sys/block/mmcblk*/queue/scheduler; do
    [ -f "$block" ] && echo "mq-deadline" > "$block"
done

# VM tuning
sysctl -w vm.swappiness=10
sysctl -w vm.dirty_ratio=20
sysctl -w vm.dirty_background_ratio=5

# CPU scheduler
sysctl -w kernel.sched_latency_ns=10000000
sysctl -w kernel.sched_min_granularity_ns=1000000
```

**Notes:**
- Sysctl writes from `service.sh` are not persistent across reboots on their
  own. The script must run at every boot — which `service.sh` does.
- `system.prop` handles standard Android properties only, not Linux kernel
  sysctl nodes. Use `service.sh` for anything under `/sys/`.
- Document which devices and kernels the tuning values are safe for. Aggressive
  values can cause instability or battery drain on certain SoCs.
- Play Integrity risk: low, unless patching GMS-visible props.

---

## Archetype 6 — Integrity compatibility (no bypass)

This skill does not scaffold modules that spoof device identity/attestation, hide root from apps, evade anti-cheat, or bypass an app/service integrity decision. Such behavior can enable fraud and violate service controls.

For a legitimate module, document exact devices and Android builds tested and any observed compatibility limitations. Prefer a non-invasive configuration or vendor-supported test environment. Do not change attestation properties, modify GMS data, or prescribe companion bypass modules.
