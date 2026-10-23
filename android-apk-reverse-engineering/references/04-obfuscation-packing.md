## Phase 4 — Obfuscation, packing, and dynamic loading

When the app appears obfuscated or packed, establish which code actually executes before spending time on static names.

Check for:

- Renamed classes/methods and shortened identifiers.
- Reflection and string-based class loading.
- `DexClassLoader`, `PathClassLoader`, in-memory DEX loading, and secondary DEX files.
- Downloaded or decrypted code, native loaders, and assets containing executable payloads.
- Integrity checks, anti-debugging, root detection, emulator checks, and environment-dependent branches.
- Flutter AOT snapshots, React Native Hermes bundles, Unity assets/IL2CPP, and .NET assemblies.

Recommended approach:

1. Identify the framework and executable formats.
2. Trace the loading sequence and the point where code becomes available.
3. Compare static artifacts with runtime class/method observations.
4. Inspect only the relevant loaded code and data.
5. Document uncertainty and limitations.

Do not equate root detection or anti-debugging with malicious behavior. Assess its context and impact.
