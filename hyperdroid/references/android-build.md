# Android build systems

Use for Android app builds with Gradle, Android SDK/emulator setup, AOSP/Soong/Make, and kernel builds. LineageOS source/device/ROM workflows are in [lineageos.md](lineageos.md). Check the project's declared toolchain before changing versions or installing packages.

## Contents

- [Gradle app builds](#gradle-app-builds)
- [SDK and emulator](#sdk-and-emulator)
- [AOSP build workflow](#aosp-build-workflow)
- [Device trees and kernels](#device-trees-and-kernels)
- [Troubleshooting and build hygiene](#troubleshooting-and-build-hygiene)

## Gradle app builds

- Prefer the repository's Gradle wrapper (`./gradlew` on Unix-like hosts, `gradlew.bat` on Windows) to a globally installed Gradle. Inspect wrapper, JDK, Android Gradle Plugin (AGP), SDK, and project documentation first.
- Inspect tasks and variants before selecting a build. Common targets include `assembleDebug`, `assembleRelease`, `bundleRelease`, `test`, `connectedAndroidTest`, and `lint`; they may not exist for every project.
- Run the narrowest relevant build/test, inspect its exit status and output paths, and report warnings or skipped tests. Don't skip tests or modify dependencies just to make a build pass unless requested.
- Release signing involves private keys/passwords. Never print, commit, or transmit them; do not generate or replace signing credentials without an explicit request.
- A Gradle build scan uploads build metadata to a remote service. Do not enable `--scan` unless the user asked for that upload and understands it.

```sh
# List tasks using the repository's wrapper.
./gradlew tasks

# Build a debug APK.
./gradlew assembleDebug

# Run unit tests.
./gradlew test

# Run Android lint when configured.
./gradlew lint

# List dependencies for the app module.
./gradlew app:dependencies
```

Typical APK outputs are under `app/build/outputs/apk/`, but inspect the actual variant/module outputs rather than promising a fixed path.

## SDK and emulator

- Check `ANDROID_HOME`/`ANDROID_SDK_ROOT`, installed platform-tools, SDK platforms, and emulator availability before invoking SDK tools.
- `sdkmanager --list` and `avdmanager list avd` are useful read-only inspections. Installing/updating SDK packages or accepting licenses changes the host; do so only within the user's request and current permissions.
- Check required system-image API, ABI, and device profile before creating an AVD. Wiping an emulator's data is destructive to that AVD; do not use `-wipe-data` unless intended.

```sh
# List installed and available SDK packages.
sdkmanager --list

# List available AVDs.
avdmanager list avd

# List emulator profiles installed on this host.
emulator -list-avds

# Start a named AVD without changing its stored data.
emulator @<avd-name>
```

## AOSP build workflow

1. Check the AOSP branch/tag's official requirements for host OS, JDK, disk, memory, and dependencies. Large source syncs and builds can consume hundreds of gigabytes and sustained CPU/RAM; estimate capacity before starting.
2. Inspect the manifest/branch and local working state. Use the project's `repo` tool and documented manifest; do not assume the latest manifest branch is compatible with the target device.
3. Sync conservatively. Review local modifications before syncing; avoid `--force-sync` by default because it can overwrite project state. Choose a bounded job count based on available resources rather than blindly using all CPUs.
4. In a shell where environment functions persist, source `build/envsetup.sh`, select the documented product/variant with `lunch`, then build the narrowest target with `m`, `mm`, or `mmm`. Use `mka` only when provided by the tree.
5. Inspect build logs and `out/target/product/<device>/` for actual outputs. Don't flash the result without following the fastboot safety reference and gaining any required approval.

```sh
# Inspect the repository's top-level state before a sync or build.
git status --short --branch

# Source the build environment from the AOSP tree.
source build/envsetup.sh

# Choose the documented product and build variant.
lunch <product>-<variant>

# Build the selected tree using its supported build wrapper.
m -j<bounded-job-count>

# Build one module in the current directory when supported.
mm

# Build one module path and its dependencies when supported.
mmm <module-path>
```

A `repo sync` changes many checkouts. Before running it, determine the branch, inspect local changes, and use a moderate `-j` value. Do not add `--force-sync` unless explicitly required and approved.

## Device trees and kernels

- Common device-tree files include `AndroidProducts.mk`, `BoardConfig.mk`, `device.mk`, product makefiles, `Android.bp`/`Android.mk`, overlays, configs, and SELinux policy. Names and required variables depend on the branch and device.
- Inspect existing tree conventions and build files before editing variables such as `TARGET_ARCH`, `TARGET_BOARD_PLATFORM`, boot-header version, kernel source/config, partition sizes, or recovery fstab. Do not paste values from another device as if universal.
- Kernel builds may be in-tree or standalone. Determine source branch, defconfig, architecture, compiler/LLVM version, cross-compile prefix, and expected image output from the device tree. Don't replace a project's compiler/toolchain without evidence.
- Treat `setenforce 0` and permissive SELinux as diagnostic-only exceptional actions, not fixes. Prefer examining denials and correcting narrowly scoped policy.

```sh
# Locate likely device-tree build configuration files.
find device -maxdepth 3 \( -name BoardConfig.mk -o -name AndroidProducts.mk \) -print

# Set the target architecture for a documented standalone ARM64 kernel build.
export ARCH=arm64

# Configure a kernel with its documented device defconfig.
make <device>_defconfig

# Build with a job count that fits the host's available resources.
make -j<bounded-job-count>
```

## Troubleshooting and build hygiene

- Preserve the first failing log and exact command; rerun with `--stacktrace`/`--info` only when it can reveal the cause.
- For Gradle failures, inspect JDK/AGP compatibility, dependency resolution, and daemon output before deleting caches. For AOSP/Ninja failures, identify the first actionable error before cleaning.
- Avoid broad `rm -rf`, `clean`, cache deletion, dependency refresh, or forced sync as first-line fixes: they can discard state, take significant time, or hide the original problem. Explain cost/risk and confirm before destructive cleanup.
- Do not claim a build succeeded just because a command started. Check the exit code and expected artifact, and state when no build was run due to unavailable tools/resources.
