## Phase 3 — Runtime and dynamic analysis

Use a controlled test device or emulator with test data. Capture baseline behavior before changing anything.

### 3.1 Baseline observation

- Record app version, Android version, ABI, permissions, network state, and account/test state.
- Reproduce one behavior at a time.
- Capture filtered Logcat output and relevant crash traces.
- Observe files, preferences, databases, intents, and network activity.
- Record exact steps and expected versus observed results.

```bash
# Confirm that ADB can see the intended test device.
adb devices -l

# Capture a clean Logcat buffer before reproducing the issue.
adb logcat -c

# Start recording logs while reproducing one test case.
adb logcat -v threadtime > "$CASE/dynamic/logcat.txt"
```

Stop log capture deliberately after the test. Logs may contain personal data, session identifiers, or tokens; redact them before sharing.

### 3.2 Frida and instrumentation

Use Frida only on an authorized test target. First establish process identity, app startup behavior, and whether the runtime supports the required Frida version and architecture.

Instrumentation goals may include:

- Tracing method entry/exit and arguments, with sensitive values redacted.
- Confirming which overload or call path is actually executed.
- Observing runtime-generated configuration and reflection.
- Monitoring JNI boundaries and selected native functions.
- Measuring whether a hypothesis is correct before implementing a permanent patch.

Keep hooks narrow, deterministic, and reversible. Avoid dumping all process memory or collecting unrelated user data. Log only what is necessary for the test. A hook may change timing or control flow; validate findings without the hook when possible.

### 3.3 Network behavior

For authorized testing, map request creation to response handling:

1. Identify the HTTP client and request-building code.
2. Trace endpoint, method, headers, body serialization, and response parsing.
3. Separate app-layer encryption from TLS.
4. Use a controlled test endpoint or an explicitly authorized proxy.
5. Record status codes, timing, retry logic, and error paths.

Certificate pinning, TLS validation, and application-level encryption are distinct mechanisms. Do not disable production protections or intercept third-party users' traffic. For owned applications, prefer debug builds, test certificates, and documented test configuration.
