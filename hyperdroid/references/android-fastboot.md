# Fastboot, bootloaders, and partitions

Use for bootloader/fastboot operations, recovery, partition layouts, root-image workflows, and firmware flashing. These actions can erase data or make a device unbootable. Device layouts and vendor commands vary; generic examples below are not authorization to execute them.

## Contents

- [Safety and preflight](#safety-and-preflight)
- [Identify the mode and layout](#identify-the-mode-and-layout)
- [Unlocking and recovery](#unlocking-and-recovery)
- [Flash planning](#flash-planning)
- [A/B and dynamic partitions](#ab-and-dynamic-partitions)
- [Recovery planning](#recovery-planning)

## Safety and preflight

Before any write:

1. Verify the exact device model/codename, bootloader mode, current firmware/slot, and the manufacturer's or ROM maintainer's instructions for that device and release.
2. Verify each image is intended for that exact variant and release; confirm its source and checksum when provided. Keep the matching stock firmware and a recovery path available. Ensure stable power and connection.
3. Inspect local files and preserve user data. Explain whether unlocking, wiping, flashing, or relocking will erase data or risk a brick. Obtain explicit approval for that exact destructive operation unless already explicitly authorized.
4. Execute one write at a time, inspect its result, and stop on any unexpected output. Do not proceed by trying random partitions or images.

Do not use `fastboot getvar all` as a default dump: it may expose identifiers and produces device-specific output. Query only the variables needed, and redact identifiers before sharing.

```sh
# List devices visible in fastboot mode.
fastboot devices

# Check the reported product/codename.
fastboot getvar product

# Check the current slot when the device implements this variable.
fastboot getvar current-slot

# Check whether fastboot is running in userspace fastbootd when relevant.
fastboot getvar is-userspace
```

## Identify the mode and layout

- `fastboot` may mean bootloader fastboot or **fastbootd** (userspace fastboot). Dynamic logical partitions typically require fastbootd; verify using device documentation and `is-userspace` where supported.
- Common partition families include `boot`, `init_boot` (common on Android 13+ devices), `vendor_boot`, `dtbo`, `vbmeta`, `recovery` (layout-dependent), and `super` containing logical partitions such as `system`, `vendor`, `product`, `system_ext`, or `odm`. This is not a universal map; inspect the exact device's documented layout.
- `bootloader`, `radio`/`modem`, TrustZone and related firmware partitions are especially device-specific and can hard-brick a device if mismatched. Never guess their names or images.
- A/B devices may have `_a`/`_b` slots. Recovery may be integrated into a boot-related image rather than a standalone partition. Do not assume an A/B or recovery layout based only on Android version.

## Unlocking and recovery

- Bootloader unlocking usually requires OEM unlocking to be enabled, vendor-specific prerequisites, and confirmation on the device; it commonly performs a factory reset. Explain and obtain approval before starting it.
- Unlock methods differ by manufacturer; some brands/models do not use fastboot. Follow the official vendor procedure, eligibility rules, and current device guide. Do not substitute a generic unlock command.
- Re-locking with a custom ROM or modified/unsigned images can prevent boot or brick the device. Do not recommend or perform it unless the exact device documentation supports the complete stock state and the user explicitly requests it.
- Recovery sideload or custom recovery flashing also depends on the device's slot and recovery layout. Prefer a supported temporary boot/test path where the manufacturer/maintainer explicitly documents it; a temporary boot is not universally supported or risk-free.
- Magisk or other boot-image patching is version-sensitive. Use the matching image and the project's current instructions; never distribute patched images or secrets without authorization.

## Flash planning

- Confirm the approved operation includes the device, exact image path(s), target partition(s), and whether the operation wipes data. A vague request to “fix” a phone is not enough to choose a flash plan.
- Verify checksums when published and inspect image names/metadata rather than trusting filenames. A build for a similar model is not necessarily compatible.
- Avoid `erase`, `-w`, format, snapshot cancellation, verification-disabling flags, and bootloader/radio writes unless the current device-specific instructions require them and the user approved their consequences.
- Never interrupt a flash that is in progress. Stop and diagnose unexpected failure rather than retrying with different partitions.

```sh
# Check a downloaded image against its published SHA-256 checksum.
sha256sum <image-file>

# Reboot an attached device to normal Android only when appropriate.
fastboot reboot

# Enter fastbootd only when the device guide requires logical-partition operations.
fastboot reboot fastboot

# Flash one already-approved image to one verified partition.
fastboot flash <partition> <image-file>
```

The last example is deliberately parameterized: do not fill its placeholders without device-specific validation and approval.

## A/B and dynamic partitions

- Query the active slot where supported and follow the ROM/device guide on which slot(s) to update. Incorrectly changing the active slot can leave the device unbootable.
- Do not assume that flashing a generic `boot` target updates the intended slot; supported syntax varies. Use documented slot-aware commands only.
- For dynamic partitions, enter fastbootd when required, verify that mode, and use exact release images. `super` and logical-partition operations have device-specific constraints.
- Virtual A/B snapshot status/cancellation is sensitive to update state. Do not cancel snapshots or interrupt merge operations to force a flash; follow the official recovery procedure for the reported state.

```sh
# Read the current slot when supported.
fastboot getvar current-slot

# Enter userspace fastboot for documented logical-partition work.
fastboot reboot fastboot

# Verify fastbootd mode where the device implements this variable.
fastboot getvar is-userspace
```

## Recovery planning

- For a soft brick, first determine whether ADB, recovery, bootloader fastboot, or fastbootd remains available. Collect exact device/product and failure output before proposing writes.
- Use matching stock images and the device's official restore guide; a factory restore or `fastboot -w` erases user data and needs explicit approval.
- Hard-brick/EDL modes and service tools are manufacturer/chipset-specific. Do not improvise button combinations, test points, or low-level flashing instructions; refer to the exact vendor/service documentation and state when repair needs specialist hardware.
