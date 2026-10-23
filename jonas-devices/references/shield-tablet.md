# Nvidia SHIELD tablet — CarbonROM 5.1.1 / Termux

- Android 5.1.1 (API 22), rooted with Magisk, Termux for Android 5.1 (legacy build). SSH: port **8022**, user `user`, key `~/.ssh/server`.
- Treat as a **legacy Android** target: do not assume modern Android tools, flags, APIs, or current Termux package availability. Verify everything (`getprop ro.build.version.release`, `uname -m`, `echo $PREFIX`, `command -v TOOL`) before relying on it, and check binary/architecture compatibility before deploying anything built elsewhere.
- Apply the same Magisk/root rules as in `references/redmi-termux.md` and the global contract and destructive-operation gate in `SKILL.md`.
