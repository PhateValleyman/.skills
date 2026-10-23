## Phase 5 — Safe modification and rebuild

Before patching, create a clean working copy or a version-controlled branch. Keep a machine-readable patch log containing file, method/resource, original behavior, change, rationale, and test.

### 5.1 Choose the narrowest edit

- Resource/UI-only change: modify the relevant resource and rebuild.
- Manifest/component change: assess permissions, exported status, and compatibility.
- Java/Kotlin logic change: patch Smali only when source-level rebuilding is unavailable or inappropriate.
- Native behavior change: use a matching ABI and a reproducible native build where possible.
- Framework-specific bundle: use tooling compatible with the framework and exact format.

Avoid editing generated files unnecessarily. Keep a diff and verify that only intended files changed.

### 5.2 Build, sign, and verify

Apktool output is generally unsigned. A modified APK must be signed before Android will install it. A new signing key does not match the original app signature; updating an installed package may therefore require a compatible signing identity or a controlled uninstall/reinstall, which can delete app data.

```bash
# Rebuild the decoded project into a separate output APK.
apktool b "$CASE/static/apktool" -o "$CASE/patches/unsigned.apk"

# Align the APK when zipalign is available in the Android build tools.
zipalign -p -f 4 "$CASE/patches/unsigned.apk" "$CASE/patches/aligned.apk"

# Sign with a test key that you control; never expose its passwords or private key.
apksigner sign --ks "$HOME/.android/debug.keystore" \
    --out "$CASE/patches/modified.apk" "$CASE/patches/aligned.apk"

# Verify signature integrity and certificate details.
apksigner verify --verbose --print-certs "$CASE/patches/modified.apk"
```

The debug keystore path may differ, and a default debug keystore may not exist. Generate or configure a test key securely if needed. Never overwrite or publish a private signing key. Ensure the signing options are compatible with the target Android version and distribution requirements.

### 5.3 Install and smoke-test

```bash
# Install the modified APK on the explicitly selected test device.
adb install -r "$CASE/patches/modified.apk"

# Launch the app using its known package/activity or the appropriate test procedure.
# Replace the example package and activity with values verified from the manifest.
adb shell monkey -p com.example.app 1
```

Do not assume the example package name is correct. For split APKs, installation may require the complete compatible split set rather than one standalone APK.

Test at minimum:

- Installation and launch.
- Main target behavior and relevant edge cases.
- Permissions, intents, storage, networking, and process restart.
- Upgrade/reinstall behavior where relevant.
- Crash-free operation and logs.
- Signature, package identity, and ABI compatibility.
