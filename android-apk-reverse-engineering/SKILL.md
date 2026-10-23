---
name: android-apk-reverse-engineering
description: Rigorous, reproducible workflow for authorized Android APK reverse engineering, debugging, interoperability research, security assessment and modification (JADX, Apktool, Smali, Frida, Ghidra, ADB, apksigner, JNI/native libs, Flutter, React Native, Unity, Xamarin, WebView). Use this skill whenever the user mentions APK, DEX, Smali, decompiling, patching or repacking an Android app, signing a rebuilt APK, Frida hooks, native .so analysis, obfuscation or packed apps, Android save/preference file formats, or Termux/rooted-device analysis, even if they do not say "reverse engineering" explicitly.
---

# Android APK Reverse Engineering

This skill defines a rigorous, reproducible workflow for authorized reverse engineering, debugging, interoperability research, security assessment, and modification of Android APKs. It covers Java/Kotlin bytecode, Smali, resources, app packaging, runtime behavior, JNI/native libraries, networking, persistence, and obfuscated applications.

## Operating principles

1. **Establish scope and authorization first.** Work on applications you own, are authorized to assess, or may lawfully modify. Do not use this workflow to steal credentials, extract private user data, bypass payment/licensing controls for fraud, deploy malware, or compromise third-party systems.
2. **Preserve evidence.** Never overwrite the source APK. Keep a pristine copy, record its SHA-256, document tool versions, and store outputs in a separate case directory.
3. **Prove before patching.** Reproduce the behavior, identify the relevant code path, and validate the hypothesis before changing bytecode or resources.
4. **Prefer the smallest reversible change.** Avoid broad rewrites, unnecessary manifest changes, and unrelated dependency updates.
5. **Treat decompiler output as an interpretation.** Confirm important conclusions against DEX/Smali, call sites, runtime traces, and native code where applicable.
6. **Do not assume a tool or command is available.** Check the installed version and help output first. Do not silently replace one tool with an incompatible alternative.
7. **Keep secrets out of artifacts.** Redact tokens, credentials, personal data, private URLs, signing keys, and sensitive log lines from reports and commits.
8. **No Docker requirement.** Prefer native packages, standalone binaries/JARs, Termux-compatible packages, or a remote Linux workstation where a tool cannot run on Android.

## User environment and portability

Prioritize this order when it fits the task:

1. Android/Termux on a rooted Redmi Note 11.
2. SSH-accessible Linux or another available host, when Android/ARM constraints block a tool.
3. A desktop GUI only when the task genuinely requires it.

Never assume that a rooted device has unrestricted access to every app's private data. Android version, SELinux, mount namespaces, app UID, package isolation, and filesystem encryption can still matter. Use the least invasive access method that answers the question.

For shell examples, use portable Bash where practical. Confirm the actual paths and installed tools rather than assuming a desktop Linux filesystem. On Termux, the prefix is typically `$PREFIX`; do not hardcode it unless the target environment is known.

## Workflow and reference map

Work through the phases in order. Read only the reference file for the phase you are in; each is self-contained.

| Phase | When | Read |
|---|---|---|
| 0–1 | Starting a case: provenance, hashes, tool versions, manifest/package/ABI inventory | `references/01-case-setup-and-inventory.md` |
| 2 | Static analysis: manifest attack surface, JADX↔Smali correlation, strings, storage formats, native/JNI | `references/02-static-analysis.md` |
| 3 | Runtime: baseline, Logcat, Frida, network behavior | `references/03-dynamic-analysis.md` |
| 4 | Obfuscated, packed or dynamically loaded code | `references/04-obfuscation-packing.md` |
| 5 | Patching, rebuild, align, sign, install, smoke-test | `references/05-modification-rebuild.md` |
| 6 | Kotlin, Flutter, React Native, Unity, Xamarin/.NET, WebView/hybrid | `references/06-frameworks.md` |
| 7 | Anything failing (decode, build, sign, install, crash, Frida, Termux) | `references/07-troubleshooting.md` |
| 8–9 | Reports, finding format, completion checklist | `references/08-reporting-and-checklist.md` |
| — | Upstream tool documentation links | `references/09-tool-links.md` |

## Minimum path for a simple task

1. Confirm authorization and scope; copy the APK to a case directory and record its SHA-256 (phase 0).
2. Inventory the package before decompiling (phase 1).
3. Locate the relevant code path, confirm in Smali/runtime (phases 2–3).
4. Make the smallest reversible change, rebuild, sign, verify the signature, test on the device (phase 5).
5. Report facts, hypotheses and limitations separately; claim a fix only after testing it (phase 8).

Check current upstream documentation and the installed `--help` output before relying on a specific option or version-specific behavior.
