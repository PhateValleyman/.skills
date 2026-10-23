# Redmi Note 11 — Termux / Android / Magisk

### 2.1 Baseline (verify, do not trust)

- `PREFIX=/data/data/com.termux/files/usr`, `HOME=/data/data/com.termux/files/home`
- Shared storage: `/storage/emulated/0`, `/sdcard`
- App private data: `/data/user/0/<package>` or `/data/data/<package>`
- Magisk: `/data/adb`, `/data/adb/modules`, `/data/adb/service.d`, `/data/adb/post-fs-data.d`

First inspection (run only what is relevant):

```bash
# Display the Android release.
getprop ro.build.version.release

# Display the Android API level.
getprop ro.build.version.sdk

# Display the device model and codename.
printf '%s %s\n' "$(getprop ro.product.model)" "$(getprop ro.product.device)"

# Display the CPU architecture and kernel version.
uname -m && uname -r

# Display the active Termux prefix and shell.
printf 'PREFIX=%s\nSHELL=%s\n' "${PREFIX:-}" "${SHELL:-}"

# Check whether root is available without changing system state.
command -v su && su -p -s bash -c 'id'
```

### 2.2 Termux rules

- Use `#!/data/data/com.termux/files/usr/bin/bash`, never `/bin/bash`.
- Use `pkg update`, `pkg upgrade`, `pkg install PACKAGE`; do not assume desktop `apt` behavior.
- Build in `$HOME`; move final artifacts to shared storage only when needed. Run `termux-setup-storage` only when shared-storage access is required.
- Do not assume systemd, `/bin` or `/usr` semantics, unrestricted filesystem access, permissive SELinux, or that Termux background processes survive indefinitely (account for Android process killing, wake locks, boot integration, persistent logs, clean start/stop).
- Termux:API (battery, Wi-Fi, notifications, IR, location, sensors, clipboard, media): check the add-on and command exist first (`command -v termux-battery-status`).
- Check Android-native tools before use (`getprop setprop pm cmd am settings dumpsys logcat toybox svc input content`); options vary with Android version.

Generated Termux scripts:

```bash
#!/data/data/com.termux/files/usr/bin/bash
# Enable strict error handling.
set -Eeuo pipefail
```

### 2.3 Privilege model

Default to the unprivileged Termux user; elevate only for the specific operation that needs it (`/data`, Magisk, privileged Android inspection, app-private data, privileged networking).

```bash
# Start a root Bash shell only when the operation requires it.
su -p -s bash

# Check the effective identity without opening an interactive shell.
su -p -s bash -c 'id'
```

### 2.4 Magisk, properties, SELinux

- Prefer Magisk modules, overlays, property overrides, `/data/adb/service.d`, `/data/adb/post-fs-data.d` over modifying Android partitions.
- Before a critical modification: inspect state, determine persistence, assess bootloop risk, back up, make the smallest change.
- Before changing a property: is it read-only? can Magisk override it? does it survive reboot? what depends on it?
- Use the **earliest boot phase that is actually necessary**; never block boot with long-running scripts.
- **Never disable SELinux as a first step** — fix ownership, permissions, contexts, Magisk policy or app config instead.

```bash
# Display the current SELinux enforcement mode.
getenforce

# Display the security context of a file.
ls -Z FILE
```

### 2.5 Application data changes

Sequence: identify package and UID → stop app → back up data → modify only the required file → restore ownership/permissions/context → start app → inspect logs → verify.

```bash
# Display installed packages and their UIDs.
pm list packages -U

# Display detailed package information.
dumpsys package PACKAGE

# Force-stop the selected application before touching its data.
am force-stop PACKAGE

# Verify that the package is installed.
pm path PACKAGE
```

Prefer `am force-stop PACKAGE` over killing PIDs. Never kill system processes blindly. Preserve UID, GID, permissions and SELinux context.

### 2.6 Diagnostics

```bash
# Display running processes.
ps -A

# Filter Android logs for an application or keyword.
logcat | grep -i PACKAGE

# Display kernel messages when the production kernel permits access.
su -p -s bash -c 'dmesg'
```

### 2.7 Toolchains and resources

- Target: `aarch64 / arm64-v8a` (verify with `uname -m`). Known NDK context: r29 — locate, do not assume a path:

```bash
# Locate Android NDK directories without assuming a fixed path.
find "$HOME" -type d -name 'android-ndk-*' 2>/dev/null

# Display toolchain versions.
java -version; gradle --version; go version; rustc --version
```

- Before heavy builds inspect `nproc`, `free -h`, `df -h`. Do not blindly use `-j$(nproc)` on a thermally/memory-constrained phone.
- Network diagnostics: `ip addr`, `ip route`, `getprop | grep -i dns`, `ping -c 3 GATEWAY`. Do not change routing/subnet blindly.
