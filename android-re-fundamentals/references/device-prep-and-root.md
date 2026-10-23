# Device Preparation and Rooting

Preparing a phone may involve a bootloader unlock, factory reset, firmware flash, and root; each can erase data, weaken security, violate support terms, or brick the device. The workflow below is an overview, not authorization or a universal flashing recipe. Use only the exact model/codename and current vendor or ROM-maintainer instructions. Obtain explicit approval for each destructive step and verify backup and recovery paths first. Unlock procedures vary by brand and model; do not infer a command or waiting period from this example.

> Replace every `<placeholder>` with your own value. Do not hardcode device serials or personal paths.

---

## Real device vs emulator

PC Android emulators (Genymotion, official AVD, and the various consumer emulators) are convenient — snapshots, multi-instance, disposable — but they are **easily detected** by hardened apps.

### How apps detect an emulator

| Signal | Real device | Emulator |
|--------|-------------|----------|
| `Build.MODEL` / `BRAND` / `HARDWARE` | concrete vendor values | `generic`, `goldfish`, `ranchu`, `sdk_gphone_*` |
| `Build.FINGERPRINT` | real device fingerprint | contains `generic`, `test-keys` |
| CPU architecture | ARM (arm64-v8a) | usually x86 / x86_64 |
| Sensors / battery / radio | full, realistic | missing or fixed values; IMEI all-zero |
| GL renderer | real GPU string | `SwiftShader`, `Android Emulator` |
| Marker files | absent | `/dev/qemu_pipe`, `/dev/goldfish_pipe`, vendor-specific `.so`/props |

No emulator perfectly emulates a real device — the x86-vs-ARM gap alone is hard to hide.

### Practical guidance

| Scenario | Emulator usable? |
|----------|------------------|
| Ordinary app traffic capture / static analysis | Yes |
| Basic dynamic debugging practice | Yes |
| Banking / finance apps | Generally no |
| Mainstream games (anti-cheat) | No |
| Packed / anti-debug apps | Often no |

**Recommendation:** start with a disposable emulator when feasible; use a physical device only if the test requires it and it is explicitly authorized. Keep test data isolated.

---

## Step 1: Drivers and Platform Tools

Windows may require a vendor or Google USB driver for the relevant device/mode. On Linux/macOS, follow the platform’s device-access and vendor guidance; do not install an unrelated universal driver by default.

| Driver source | Notes |
|---------------|-------|
| Google USB Driver | ships with the SDK Platform Tools, broadly compatible |
| Vendor driver | bundled with OEM flashing tools |
| Universal ADB Driver | one-click installers exist |

**Android SDK Platform Tools** provide the two core CLIs:

- **adb** — talks to the device while it is booted normally.
- **fastboot** — talks to the device while it is in bootloader/fastboot mode.

Download, extract to a stable path (e.g. `C:\platform-tools`), and add that path to the system `PATH`. Verify:

```bash
adb devices
# "<serial>    device" means connected
```

---

## Step 2: Enable developer options and USB debugging

1. Settings → About phone → tap the build/version number **7 times** to unlock Developer Options.
2. Settings → System → Developer options → enable **USB debugging**.
3. Re-run `adb devices` and accept the RSA authorization prompt on the phone.

---

## Core concepts

### Bootloader (BL) and the BL lock

The bootloader is the first program to run at power-on (analogous to BIOS/UEFI). It initializes hardware and verifies+loads the boot/system images. OEMs ship it **locked** so only officially signed images can boot. With the BL locked you cannot flash any third-party image — and you need to modify the `boot` partition (flash Magisk) to get root, so the BL must be unlocked first.

### Line-flash vs card-flash

| | Line-flash (fastboot) | Card-flash (recovery) |
|---|---|---|
| Method | USB cable + fastboot/OEM tool | zip placed on device, flashed via recovery |
| Mode | Fastboot / Download (Samsung Odin) | Recovery |
| Use | official firmware, un-brick, partition images | third-party ROMs, Magisk zips |

### Brand-by-brand unlock

Unlock eligibility and process vary by current vendor, region, carrier, exact model and firmware. Use current official instructions for the exact device/codename; do not apply a command, waiting period, or bypass method from another model. Some vendors no longer offer official unlocking.

---

## Step 3: Bootloader unlock (device-specific; no universal recipe)

Obtain explicit authorization for this exact device before unlocking. Confirm its model/codename, carrier/region, supported unlock path, current vendor instructions, verified backup, and a tested recovery route. Bootloader unlocking commonly wipes user data and can affect device security, warranty/support, DRM, banking apps, and future updates. Do not disable host security tools or change VPN/proxy settings as a generic troubleshooting step; consult the vendor support instructions for errors.

---

## Step 4: ROM change (high-impact; device-specific)

A ROM change is optional and can wipe data, break recovery/verified boot, or damage the device if an image is wrong. Use current maintainer instructions for the exact codename, verify image provenance/checksums and a restore path, and obtain explicit approval. There is no safe universal fastboot/recovery sequence, so commands are intentionally omitted.

---

## Step 5: Root with Magisk (device-specific)

If root is necessary, follow current Magisk/device-specific instructions for the exact model, firmware, active slot, and target partition. Do not assume `boot.img` is always correct: modern devices may use `init_boot`, A/B slots, or dynamic partitions. Never flash a placeholder or image from another build. Any root/flash action requires explicit approval for the exact device and a verified recovery image and backup.

---

## What root unlocks for RE

| Need | Why root is required |
|------|----------------------|
| Frida injection | `frida-server` must run as root |
| SSL pinning bypass | modify the system cert store / inject with Frida |
| Read app private data | `/data/data/<pkg>/` is owned by the app's UID |
| Hook system APIs | Xposed/LSPosed need Magisk + root |
| Capture encrypted traffic | installing a system CA cert needs root |

Root provides UID 0 and can bypass many discretionary permission checks, but does not inherently disable SELinux, defeat encryption, or cross every app isolation boundary.

---

## Magisk modules and features useful for RE

Magisk's value beyond bare root is its **systemless module system** (it never touches the `/system` partition) and its hiding mechanisms.

| Module / feature | Role |
|------------------|------|
| **LSPosed** | Xposed successor; hook arbitrary app Java methods. Core RE tooling. |
| Root visibility | Do not attempt to hide root from apps or bypass integrity/anti-cheat controls. |
| System CA changes | Avoid system-wide proxy CA promotion on personal/production devices; prefer app-specific debug trust on a controlled test build. |
| **Busybox** | Fill out the Linux command-line toolset. |
| **Zygisk** | Built-in injection in the Zygote process. |
| DenyList | Do not present this as a way to evade banking, payment, anti-cheat or integrity checks. |

Root, LSPosed, or Frida are optional tools for authorized isolated testing, not prerequisites. Do not defeat pinning or collect plaintext/third-party data without explicit authorization.
