# Android devices, ADB, and debugging

Use this reference for authorized ADB device work, app management, UI interaction, logs, crash/ANR analysis, performance, and system inspection. Commands are examples for an available host-side Android Platform Tools installation; verify Android-version support and access before relying on them.

## Contents

- [Connect and identify](#connect-and-identify)
- [Shell and app management](#shell-and-app-management)
- [Files and UI interaction](#files-and-ui-interaction)
- [Logs and crash triage](#logs-and-crash-triage)
- [System diagnostics and troubleshooting](#system-diagnostics-and-troubleshooting)

## Connect and identify

- Check access with `adb devices -l`. `device` means authorized; `unauthorized` requires accepting the debugging prompt on the device; `offline` indicates an unavailable ADB connection.
- When multiple devices/emulators are listed, pass `-s <serial>` to every command, including nested shell commands. Never guess a serial or target.
- Gather model, Android release, and SDK level before using version-specific commands. Redact serials, account names, tokens, private paths, and personal data before sharing captured output.
- For Android 11+, pair through the device's **Wireless debugging** settings and its temporary pairing code, then connect to the displayed endpoint. Use a trusted network and disable wireless debugging or disconnect when finished. Legacy `adb tcpip` exposes a debugging endpoint; only use it when needed on a trusted network, then turn it off.

```sh
# List attached devices and their connection state.
adb devices -l

# Read the model from one selected device.
adb -s <serial> shell getprop ro.product.model

# Read the Android release from one selected device.
adb -s <serial> shell getprop ro.build.version.release

# Read the API level from one selected device.
adb -s <serial> shell getprop ro.build.version.sdk
```

## Shell and app management

- Run a single command with `adb shell <command>`; quote compound shell expressions carefully because commands pass through the host shell and device shell.
- Use `pm list packages -3`, `pm path <package>`, and `dumpsys package <package>` to inspect installed apps. Use `am start` or `monkey` to launch and `am force-stop` to stop an app.
- `adb install -r <apk>` replaces an existing app. Add `-g` only if granting all requested runtime permissions is intended and supported.
- `pm clear <package>` deletes that app's local data. Do not run it without the user's explicit approval for the target app and data loss.
- Grant/revoke permissions only when requested; confirm package, permission, and Android version first. `run-as <package>` works only for debuggable apps. Do not assume root access or bypass platform protections.

```sh
# Inspect third-party packages.
adb -s <serial> shell pm list packages -3

# Find an installed package's APK path.
adb -s <serial> shell pm path <package>

# Launch the app's launcher activity.
adb -s <serial> shell monkey -p <package> -c android.intent.category.LAUNCHER 1

# Stop an app without clearing its data.
adb -s <serial> shell am force-stop <package>

# Install or update an APK while preserving existing app data.
adb -s <serial> install -r <apk-path>
```

## Files and UI interaction

- Use `adb push`/`pull` only for the requested files and paths. Avoid reading private app data or personal files unless necessary and authorized.
- UI input by coordinates is brittle: capture the current screen and verify dimensions/state before taps or swipes. Use `uiautomator dump` when a view hierarchy is more useful. Do not treat a successful input command as proof that the UI action succeeded.
- `input text` has escaping limitations (for example, `%s` represents a space on many builds); do not use it to enter passwords or other secrets.
- `screencap` and `screenrecord` create files on the device. Pull only the requested output and clean up temporary files only when authorized.

```sh
# Copy a local file to shared device storage.
adb -s <serial> push <local-file> /sdcard/<name>

# Retrieve a device file into the current host directory.
adb -s <serial> pull /sdcard/<name> .

# Capture a screenshot to host stdout as a PNG.
adb -s <serial> exec-out screencap -p > screen.png

# Dump the current UI hierarchy on the device.
adb -s <serial> shell uiautomator dump /sdcard/ui.xml

# Retrieve the UI hierarchy for inspection.
adb -s <serial> pull /sdcard/ui.xml .

# Tap a coordinate after verifying the current screen and target.
adb -s <serial> shell input tap <x> <y>
```

## Logs and crash triage

Use the least-privileged, smallest useful capture. Log buffers and dumps can contain personal information, credentials, or identifiers; filter and redact before sharing.

```sh
# Read recent log entries with timestamps, without clearing the buffer.
adb -s <serial> logcat -d -t 200 -v threadtime

# Read recent crash-buffer entries.
adb -s <serial> logcat -b crash -d -t 100

# Read recent errors across log buffers.
adb -s <serial> logcat -d -t 300 '*:E'

# Inspect the most recent activity-manager ANR summary.
adb -s <serial> shell dumpsys activity lastanr

# List available DropBox entries without dumping their contents.
adb -s <serial> shell dumpsys dropbox
```

Triage in this order:

1. Establish a reproducible action, approximate time, package, device/build, and whether the failure is Java/Kotlin, native, ANR, or unknown.
2. **Java/Kotlin:** find the exception and full `Caused by` chain; locate the first relevant frame in the app's package. Distinguish the initiating cause from framework frames and follow-up errors.
3. **Native:** inspect an accessible tombstone for signal, fault address, and backtrace. Use matching unstripped symbols/NDK tools for symbolication when supplied. Access under `/data/tombstones/` commonly requires elevated privileges; do not attempt to bypass access controls. If unavailable, ask for the authorized tombstone or relevant bug report.
4. **ANR:** inspect the trace and `dumpsys activity lastanr`; focus on the main thread, blocking locks, long I/O/network work, and Binder waits. Avoid copying unrelated user data from a full trace.
5. Correlate timestamps with app/device changes and report evidence, likely cause (with uncertainty), and a testable next step. This is a workflow within the skill, not a separate crash-analyzer agent.

```sh
# List tombstone filenames only when the device permits access.
adb -s <serial> shell ls -la /data/tombstones/

# Read an ANR trace only when access is authorized and permitted.
adb -s <serial> shell cat /data/anr/traces.txt

# Check app memory use for a named package.
adb -s <serial> shell dumpsys meminfo <package>

# Inspect a focused service dump, limiting output where possible.
adb -s <serial> shell dumpsys activity | head -200
```

## System diagnostics and troubleshooting

- Use `getprop` for system properties and targeted `dumpsys <service>` calls for activity, package, battery, memory, CPU, display, or connectivity state. Service names and output vary by Android release.
- If the device is absent, check the cable/USB mode, host ADB installation, authorization prompt, and `adb devices -l` before restarting the ADB server. Do not repeatedly revoke authorizations or reset device settings without need.
- If a device-side command is missing or denied, check Android version and permissions; do not assume root. Explain any limitation and request only the required output.

```sh
# List available dumpsys services.
adb -s <serial> shell dumpsys -l

# Inspect battery state.
adb -s <serial> shell dumpsys battery

# Inspect per-package memory statistics.
adb -s <serial> shell dumpsys meminfo <package>

# Restart the host ADB server only when connection troubleshooting calls for it.
adb kill-server && adb start-server
```
