## Phase 8 — Reporting and deliverables

Each investigation should produce:

- `README.md`: scope, target identity, environment, and reproduction steps.
- `metadata/`: hashes, package details, tool versions, certificate details, and ABI inventory.
- `static/`: decompiler/disassembly output or references to it.
- `dynamic/`: sanitized logs, test notes, and instrumentation scripts.
- `patches/`: patch files, diffs, rebuilt artifacts, and signing verification output.
- `reports/`: findings, evidence, limitations, and final verification.

For each finding, state:

- **Observation:** what was directly observed.
- **Evidence:** file/method, instruction, trace, log, or reproducible test.
- **Interpretation:** what the evidence likely means.
- **Confidence:** confirmed, strongly supported, tentative, or unknown.
- **Impact:** practical effect and affected conditions.
- **Change:** exact patch, if any.
- **Verification:** commands and test results.
- **Limitations:** unavailable symbols, missing runtime, inaccessible server-side logic, or other uncertainty.

Do not claim a successful fix unless the relevant behavior was tested after the change.

## Phase 9 — Completion checklist

- [ ] Authorization and scope documented.
- [ ] Original APK preserved and SHA-256 recorded.
- [ ] Package/version/signature/SDK/ABI inventory completed.
- [ ] Static findings cross-checked against bytecode or runtime evidence.
- [ ] Dynamic tests use controlled data and sanitized logs.
- [ ] Changes are minimal, documented, and reversible.
- [ ] Rebuilt APK signature verified.
- [ ] Installation and target behavior tested on the intended Android version.
- [ ] No private keys, tokens, personal data, or unrelated files included.
- [ ] Report separates facts, hypotheses, and limitations.
- [ ] Reusable project knowledge and this skill updated with confirmed discoveries only.
