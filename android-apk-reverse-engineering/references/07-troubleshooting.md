## Phase 7 — Troubleshooting methodology

For every failure:

1. Capture the exact command, complete error output, tool version, Android/API level, and ABI.
2. Identify the failing stage: decode, analysis, patch, build, sign, install, launch, or runtime behavior.
3. Form one root-cause hypothesis at a time.
4. Make the smallest diagnostic change.
5. Re-run the same test and compare outputs.
6. Record the confirmed cause separately from assumptions.

Common pitfalls:

- **JADX output is incomplete:** verify the method in Smali/DEX and inspect compiler-generated or obfuscated control flow.
- **Apktool decode/build fails:** record Apktool version, framework dependencies, exact error, and whether the APK uses unusual resources or vendor-specific packaging.
- **APK installs but crashes:** collect the crash stack, compare manifest and runtime permissions, check ABI/native dependencies, and validate the patched method.
- **Signature mismatch:** compare certificates and signing schemes; do not assume a rebuilt APK can update the original.
- **Native library fails to load:** inspect ABI, ELF dependencies, API-level symbols, and linker errors.
- **Behavior differs under Frida:** account for timing and instrumentation effects; reproduce without hooks.
- **Build works on desktop but not Termux:** check Java version, CPU architecture, executable format, memory/storage limits, and Android compatibility of bundled binaries.
- **App data disappears:** check package/signature identity and backup/restore behavior before reinstalling.
