---
name: android-re-fundamentals
description: Android reverse-engineering fundamentals: APK/DEX structure, ADB and host setup, device/rooting concepts, Frida basics, Android filesystem, packaging, traffic-analysis concepts, and UI automation. Use when explaining these topics or planning an authorized Android RE environment; use a task-specific RE skill for analysis of a particular app. Device unlock, flashing, rooting, data extraction, and traffic interception can erase data or expose sensitive information, so do not perform them without explicit, scoped authorization. Do not use for ordinary Android app development or general mobile troubleshooting.
---

# Android RE Fundamentals

The onboarding and fundamentals layer for authorized Android reverse engineering. It is **generic and tool-agnostic**; it explains APK artifacts and helps plan a host/device setup, but a rooted device, ROM change, traffic interception, and every listed tool are not prerequisites for static analysis. It does not target one specific application; for concrete app analysis, follow the task-specific references available in the project.

## when_to_use

Use this skill when any of the following is true:

- The user is **new to Android reverse engineering** and needs the lay of the land.
- A **workstation is being bootstrapped** — JDK, adb/fastboot, Frida, Charles/mitmproxy, scrcpy are not yet installed or verified.
- The user asks about **authorized test-device preparation** or needs to weigh emulator versus device trade-offs. Treat unlock, reset, firmware flash, and rooting as high-impact actions requiring explicit scoped approval; suggest static/emulator analysis first where feasible.
- The user asks a **conceptual** question about how APKs are packaged, what is inside an APK/DEX, how the Android filesystem and partitions are laid out, or where an app stores its data.
- The user wants **phone UI automation** (adb input, uiautomator2, Appium, Airtest) to drive a target app.

If the user already has a working environment and a concrete target, prefer the specialized skill for the task at hand (decompile, hook, capture, native RE) — point them there from the workflow below.

## Workflow

Work top-down. Each phase points to a reference document with the full detail.

### Phase 0: Decide on a target device

A disposable emulator is often the safest first choice for learning and static/dynamic work on an authorized test target. Some apps detect emulators; a physical device is not inherently more reliable or safer and may contain personal data. Prefer the least-privileged isolated option that meets the test need. See `references/device-prep-and-root.md` for trade-offs; do not root or unlock as a default.

### Phase 1: Prepare and root the device

1. On Windows, install the vendor/Google USB driver if needed; on other hosts, follow the host OS and vendor guidance. Confirm the device is recognized in normal and bootloader modes.
2. Enable Developer Options and USB debugging.
3. Use static analysis or an emulator if they meet the need. Consider a physical device, bootloader unlock, ROM change, or root only when technically necessary, supported for that exact model, and explicitly approved. These steps may wipe data, weaken security, affect support/DRM, or brick the device; follow current official instructions and verify recovery before any change.
4. Root does not disable SELinux or guarantee access to every app namespace or encrypted file.

`references/device-prep-and-root.md` is a conceptual overview, not a universal flashing recipe. Do not recommend a particular root-hiding, system-CA, or pinning-bypass module as a default; verify current, authorized, device-specific requirements first.

### Phase 2: Set up the host environment

Install and verify, in roughly this order — see `references/environment-setup.md`:

1. **JDK** (8 for legacy tooling, 17+ for modern jadx) — verify with `java -version`.
2. **Android SDK Platform Tools** — `adb` and `fastboot` on PATH; verify with `adb devices`.
3. **Frida** (optional) — follow the official, current installation instructions and pair host/device components as required by their versions. Use only with an authorized test app/device. See `references/frida-setup.md`.
4. **Traffic capture** — use a controlled test device, test account, and an app you own or are authorized to assess. Android apps’ trust of user-added CAs depends on target SDK and network security configuration; do not assume a CA is universally trusted or promote a proxy CA system-wide on a personal/production device. Prefer a debug build/test trust configuration and remove test certificates afterward. See `references/environment-setup.md`.
5. **scrcpy** (optional) for screen mirroring/control.

### Phase 3: Learn the fundamentals (reference reading)

Before touching a real target, understand the artifacts you will be manipulating:

- **APK internals** — what every entry in the ZIP is for, DEX format, Smali basics, signing schemes (V1/V2/V3). See `references/apk-structure.md`.
- **Forward packaging pipeline** — how source becomes an installable APK (aapt2 → javac/kotlinc → D8/R8 → zipalign → apksigner), because *reversing is this pipeline run backwards*. See `references/apk-packaging.md`.
- **Android filesystem** — partitions, `/system`, `/data/data/<pkg>`, `/proc/<pid>/maps`, where apps keep prefs/databases. See `references/android-filesystem.md`.
- **adb cheat sheet** — push/pull, install/uninstall, pulling an installed APK off the device, writing files without an editor. See `references/adb-cheatsheet.md`.

### Phase 4: Decompile and hook basics

Static decompilation (jadx/apktool) plus dynamic hooking (Frida) is the core RE loop. `references/decompile-and-hook.md` covers the tool chain, identifying third-party SDKs and packers from the `lib/` directory, what Frida injection leaves behind, and a minimal Java/native hook example. For deeper work hand off to the specialized skills (`android-re-decompile`, `apktool-decompile`, `frida-hooking`, `objection-runtime`, `android-unpacking`, `ghidra-reverse-engineering` / `ida-reverse-engineering`).

### Phase 5: Automate the device (optional)

When you need to repeatedly drive the target's UI, choose an automation approach by app type — accessibility-tree tools (uiautomator2, Appium, AutoX.js) for normal apps, vision-based tools (Airtest/OpenCV) for games and custom-rendered UIs. See `references/phone-automation.md`.

## References

- `references/device-prep-and-root.md` — emulator/device trade-offs and high-level, device-specific preparation cautions.
- `references/environment-setup.md` — host tools and optional test-capture proxy setup, with safe test-certificate handling.
- `references/frida-setup.md` — frida-tools (host) + frida-server (device) install, version matching, starting the server, verification, injection footprint.
- `references/adb-cheatsheet.md` — push/pull/install/uninstall, pulling installed APKs, command-source taxonomy, writing files on-device.
- `references/apk-structure.md` — APK as a ZIP, every file/dir explained, DEX format, Smali basics, signing schemes, packer fingerprints.
- `references/apk-packaging.md` — Full forward build pipeline (AIDL → aapt2 → D8/R8 → zipalign → apksigner), AAB vs APK, forward↔reverse mapping, repackage flow.
- `references/android-filesystem.md` — Partitions, `/system`, `/vendor`, `/data`, `/proc`, `/dev`, boot flow, security model, RE-relevant paths.
- `references/decompile-and-hook.md` — decompiler/hook concepts, packer indicators and read-only instrumentation examples.
- `references/phone-automation.md` — Automation approaches (adb input, uiautomator2, Appium, AutoX.js, Airtest), accessibility vs vision-based, examples.
