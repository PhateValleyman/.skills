---
name: hyperdroid
description: Android device work and development across ADB, app debugging and UI automation, fastboot and recovery, Gradle/SDK/AOSP/kernel builds, and LineageOS ROM development. Use for requests mentioning adb, logcat, Android devices, APKs, fastboot, flashing, bootloaders, Gradle, AOSP, kernels, device trees, LineageOS, breakfast, brunch, repopick, or Gerrit.
---

# Hyperdroid

Adapted from [hyperb1iss/hyperdroid-skill](https://github.com/hyperb1iss/hyperdroid-skill), copyright © 2025 Bliss; licensed under MIT. See [LICENSE](LICENSE).

## Route to the relevant reference

- **ADB/device access, app management, UI interaction, logs, crashes, or system inspection:** read [references/android.md](references/android.md).
- **Bootloader, fastboot, partition, recovery, root-image, or flashing work:** read [references/android-fastboot.md](references/android-fastboot.md).
- **Gradle, Android SDK/emulator, AOSP, or kernel builds:** read [references/android-build.md](references/android-build.md).
- **LineageOS source, device trees, vendor blobs, ROM builds, or Gerrit:** read [references/lineageos.md](references/lineageos.md). For build commands, also read `android-build.md`.
- Read multiple references only when the task crosses domains; keep each reference one level below this entrypoint.

## Operating workflow

1. **Establish the target and requested outcome.** Identify host OS, Android model/codename, Android/build version, project branch, connected device, and whether the request is for advice or execution. Do not infer these from a product name alone.
2. **Check actual access and tools.** Use only capabilities available in the current session. Android commands such as `adb`, `fastboot`, `gradlew`, `repo`, or `m` are host-side CLIs, not built-in device connectors; check that they exist and that the intended device/project is reachable. Never claim a command ran or a device is connected unless verified. If direct access is unavailable, provide exact commands for the user to run and analyze returned output.
3. **Prefer inspection before mutation.** Read project/device state and preserve local changes before building or changing anything. Use the exact serial when more than one device is present. Check current official device/vendor/LineageOS instructions when support, branch, partition layout, or command syntax can vary.
4. **Treat destructive device operations as high impact.** Before bootloader unlock/lock, data wipe, erase, or partition flash, verify the exact device and images, explain the specific data-loss/brick risk and recovery prerequisites, and get explicit approval for that exact operation unless already explicitly authorized. Never apply generic commands to an uncertain target; do not bypass verified boot or relock a device running a custom OS by default.
5. **Keep changes scoped and report evidence.** Avoid global configuration changes, forced source syncs, cache deletion, secret exposure, or external uploads unless requested. Run proportionate checks and summarize what was inspected, changed, tested, and left for the user.

## Domain references

- [Android devices and debugging](references/android.md)
- [Fastboot and partitions](references/android-fastboot.md)
- [Android build systems](references/android-build.md)
- [LineageOS development](references/lineageos.md)

The repository also provides a separate crash-analyzer agent. This skill does not create or invoke that agent; its useful crash-triage workflow is incorporated into `android.md` and must be performed only with available, authorized access.
