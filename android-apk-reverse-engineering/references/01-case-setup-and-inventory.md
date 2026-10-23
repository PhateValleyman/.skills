# Contents

- Phase 0 — Case setup and provenance
- Phase 1 — APK inventory and package structure

## Phase 0 — Case setup and provenance

Create a dedicated case directory. Preserve the original APK and record its digest, file type, size, package identity, version, SDK levels, signing certificate, DEX count, and native ABIs.

```bash
# Set the input APK path and a separate analysis directory.
APK="$HOME/storage/downloads/target.apk"
CASE="$HOME/apk-re/target-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASE"/{original,metadata,static,dynamic,patches,reports}

# Copy the original APK without modifying it.
cp -- "$APK" "$CASE/original/original.apk"

# Record a cryptographic hash for provenance and later comparison.
sha256sum "$CASE/original/original.apk" | tee "$CASE/metadata/sha256.txt"

# Record basic file information.
file "$CASE/original/original.apk" | tee "$CASE/metadata/file.txt"

# Record tool versions where the tools are installed.
for tool in java jadx apktool apksigner adb aapt unzip strings readelf; do
    if command -v "$tool" >/dev/null 2>&1; then
        printf '\n### %s\n' "$tool"
        "$tool" --version 2>&1 | head -n 3
    fi
done | tee "$CASE/metadata/tool-versions.txt"
```

Adapt commands to the installed tool versions. Some tools do not implement `--version`; consult their help output rather than treating that as a fatal analysis error. If `sha256sum`, `file`, or `head` is unavailable, use a verified equivalent already installed in the environment.

## Phase 1 — APK inventory and package structure

Inspect the package before decompiling it.

Record at minimum:

- Package name, app label, version name/code.
- `minSdkVersion`, `targetSdkVersion`, permissions, exported components, intent filters.
- Activities, services, receivers, providers, deep links, app links, and network-security configuration.
- DEX files (`classes.dex`, `classes2.dex`, etc.).
- Native libraries under `lib/<abi>/*.so`.
- Assets, databases, configuration files, bundled scripts, certificates, and resource files.
- Signing scheme/certificate information and whether the APK is split, bundled, or packed.
- Indicators of Flutter, React Native, Unity, Xamarin/.NET, Cordova, Kotlin, or other frameworks.

Useful commands:

```bash
# List archive entries without extracting or modifying the APK.
unzip -l "$CASE/original/original.apk" | tee "$CASE/metadata/archive-list.txt"

# Inspect the manifest and resources through Apktool when available.
apktool d -f "$CASE/original/original.apk" -o "$CASE/static/apktool"

# Decompile DEX to Java-like source for navigation and hypothesis generation.
jadx --show-bad-code -d "$CASE/static/jadx" "$CASE/original/original.apk"

# Inspect signing information with Android build tools.
apksigner verify --verbose --print-certs "$CASE/original/original.apk" \
    | tee "$CASE/metadata/signature.txt"
```

If a command-line option differs in the installed release, check `jadx --help` or `apktool --help` and adapt it. A successful decompilation is not proof that every method was reconstructed correctly.
