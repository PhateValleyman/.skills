# Contents

- Phase 2 — Static analysis

## Phase 2 — Static analysis

### 2.1 Manifest and component attack surface

- Identify exported components and their permission requirements.
- Trace externally reachable intents, deep links, content providers, broadcast receivers, and services.
- Check for unsafe implicit intents, weak URI validation, debuggable flags, backup settings, cleartext traffic, and overly broad permissions.
- Follow the code path from component entry point to sensitive operations.
- Distinguish manifest declarations from runtime registration and dynamically loaded components.

Do not report a manifest flag as exploitable without establishing a reachable behavior and realistic impact.

### 2.2 JADX and DEX/Smali correlation

Use JADX for navigation, call hierarchy, string search, and an initial understanding of Java/Kotlin logic. Verify critical findings in Smali or DEX because decompilation may be incomplete or misleading around compiler-generated code, exception flow, reflection, Kotlin coroutines, synthetic methods, and obfuscation.

Recommended sequence:

1. Search for the visible UI text, error message, URL path, preference key, database table, or relevant API.
2. Find references to the matching method and identify callers.
3. Trace parameters, return values, state changes, exceptions, and callbacks.
4. Inspect the corresponding Smali when control flow or register behavior matters.
5. Record class/method descriptors and the original behavior before making a patch.

Smali review checklist:

- Register counts and parameter registers.
- Method prototypes and return types.
- Branch targets and labels.
- `invoke-*` instruction compatibility with the target API/DEX version.
- Correct `move-result*` placement and type.
- `try`/`catch` ranges and exception behavior.
- Register types, wide values, object references, and constructor invocation.
- Updated resource IDs, method references, and string constants.

Never patch based solely on a decompiler line number. Map the proposed edit back to the actual method and bytecode.

### 2.3 Strings, constants, and embedded data

Search for domain names, endpoint paths, feature flags, preference keys, error messages, analytics events, cryptographic APIs, file paths, and native method names. Use multiple signals; strings may be encrypted, compressed, generated at runtime, or absent due to obfuscation.

Treat discovered endpoints and credentials as sensitive. Do not publish active secrets in reports or commits. If a secret appears to be exposed, report its location and recommend rotation rather than using it.

### 2.4 Data storage and serialization

Identify SharedPreferences, SQLite/Room, files, protobuf, JSON, Parcelables, custom binary formats, and Android Keystore usage. Determine schema/versioning, encoding, endianness, compression, encryption, integrity checks, and migration behavior before editing stored data.

For binary formats:

- Preserve a clean sample and its hash.
- Compare multiple samples representing controlled state changes.
- Use hex dumps and byte offsets to form hypotheses.
- Validate field boundaries and lengths against several samples.
- Implement a parser before an editor; round-trip unchanged data and compare bytes.
- Do not assume that an unknown byte sequence is a timestamp, integer, or checksum without evidence.

### 2.5 Native libraries and JNI

Inventory each ABI and library. Inspect ELF headers, imports/exports, symbols, strings, JNI registration, and Java-to-native call sites. Use Ghidra, Rizin/Cutter, `readelf`, `objdump`, and `nm` where available.

For stripped binaries:

- Locate JNI exports or `RegisterNatives` usage.
- Trace callers from Java/Kotlin declarations.
- Identify architecture, calling convention, argument types, and return values.
- Use dynamic traces to validate decompiler hypotheses.
- Consider C++ name mangling, compiler optimizations, inlining, and anti-debugging checks.

Do not infer native function semantics from symbol names alone. Verify with call sites, data flow, and runtime behavior.
