# ZyXEL NSA320 "Server" — FFP (legacy production infrastructure)

### 3.1 Profile

| Property | Value |
|---|---|
| Hostname / IP | `SERVER` / `192.168.1.20` |
| Architecture / ABI | ARMv5 Feroceon / soft-float |
| OS environment | Fonz Fun Plug 0.7.0 |
| Kernel | 2.6.31.8 |
| libc | uClibc 0.9.33.3 |
| FFP root / Bash / home | `/ffp` / `/ffp/bin/bash` / `/ffp/home/root` |
| Toolchain | `arm-ffp-linux-uclibcgnueabi` |
| C flags | `-march=armv5te -mfloat-abi=soft` |
| Go target | `CGO_ENABLED=0 GOOS=linux GOARCH=arm GOARM=5` |

Assume limited CPU, RAM, storage I/O, and old kernel/userspace behavior. **Do not assume:** systemd, journalctl, modern GNU utilities, modern iproute2 (`ip`), modern Bash, glibc, modern OpenSSL, modern kernel APIs. Check availability first. Prefer changes under `/ffp`; use absolute paths and POSIX-compatible syntax unless Bash features are required.

Generated scripts: shebang `#!/ffp/bin/bash`.

### 3.2 Discovery

```bash
# Identify the running kernel and architecture.
uname -a

# Identify the current shell and executable location.
echo "$SHELL"; command -v bash

# Inspect available memory and storage.
free; df -h

# Check whether the required program exists and its version.
command -v PROGRAM; PROGRAM --version
```

### 3.3 FFP packages and services

- Package tooling: `command -v slacker funpkg`. Do not assume modern package-manager behavior. When changing packages: identify installed version → check dependencies → preserve config → avoid replacing core libraries → verify binaries and services.
- Startup: `/ffp/start`, `/ffp/stop`, `/ffp/etc/init.d`. For service changes identify: executable, configuration, startup mechanism, running process, logs, dependencies, listening ports, required mounts. Verify **both** startup config and runtime state.
- Do not edit a config until you know the running service actually uses it.

### 3.4 Native builds and binary compatibility

Binaries must match ARMv5 + soft-float + uClibc. Inspect before deploying:

```bash
# Identify the binary architecture and ABI.
file ./program

# Inspect ELF architecture information.
readelf -h ./program

# Inspect runtime library dependencies when ldd is available.
ldd ./program
```

Typical failures: wrong architecture, hard-float vs soft-float, glibc vs uClibc, missing shared libs, incompatible dynamic linker, kernel features newer than 2.6.31, instructions unavailable on ARMv5.

Prefer **static Go binaries**; avoid CGO unless required and the toolchain is known compatible:

```bash
# Build a statically linked Linux ARMv5 binary.
CGO_ENABLED=0 GOOS=linux GOARCH=arm GOARM=5 go build

# Verify the resulting executable architecture and linkage.
file ./program
```

### 3.5 Storage, firmware, libraries

- Storage operations are high risk. Inspect first: `mount`, `df -h`, `cat /proc/partitions`. Never assume `/dev/sda`, partition numbering, RAID devices, mountpoints, filesystem type or disk ownership. Destructive operations (`mkfs`, `fsck -y`, `fdisk`, `parted`, `dd`, partition/RAID changes) require explicit authorization.
- Do **not** modify bootloader, kernel, firmware or unknown flash/system partitions unless the task requires it and the exact recovery procedure is understood.
- OpenSSL/shared libs: inspect `openssl version` first; never replace system libraries blindly — an upgrade can break unrelated legacy software. When diagnosing a binary check architecture, ABI, dynamic linker, shared libs, versions.

### 3.6 Backup, cleanup, reboot

```bash
# Create a timestamped backup of an important configuration directory.
cp -a /ffp/etc /ffp/etc.backup.$(date +%Y%m%d-%H%M%S)
```

Important locations: `/ffp/etc`, `/ffp/start`, `/ffp/stop`, `/ffp/etc/init.d`, `/etc`, service configs, scripts, databases. Backups must be **usable**, not merely created.

Cleanup: identify exact path → determine ownership/purpose → check dependent services → back up → delete only the confirmed target → verify. Large files are not automatically unnecessary.

Before restart/reboot: save and syntax-check config, verify required mounts, check running services and active transfers, ensure SSH returns after reboot, confirm recoverability. After reboot verify remotely: `hostname`, `uname -a`, `mount`.

### 3.7 Network, logs, resources, cron, MeshFS

- Network: `ifconfig`, `route -n`, `ping HOST`; use `ip` only if installed and functional. For services determine process, listen address/port, protocol, config, startup, firewall needs (`netstat -lntup`). Prefer LAN-only exposure.
- Logs: `/var/log`, `grep -Ri "TERM" /var/log`, `dmesg`. No journalctl.
- Resources: check `free`, `df -h`, `uptime` before expensive work. Avoid aggressive parallel builds, memory-heavy operations, unbounded loops, needless background processes. Never blindly use `-j$(nproc)`.
- Cron: inspect first (`ps | grep crond`, `crontab -l`). Scheduled scripts must use absolute paths, be idempotent, log failures, avoid overlapping runs (PID file, lock file, `flock` if available, atomic `mkdir`), and fail safely.
- **MeshFS / SSHFS:** NSA320 participates in it. Before changing mounts inspect `mount` and `command -v sshfs`; verify SSH connectivity, target availability, mountpoint existence, existing/duplicate mounts, `allow_other` needs, boot behavior, failure/retry behavior. **Never create infinite boot-blocking retry loops.**
- Security: SSH keys, encrypted protocols, least privilege, minimal exposed ports, LAN-only where possible, avoid `chmod 777` and unnecessary root services.

### 3.8 Decision tree

```
Read-only/diagnostic → inspect → diagnose → report
Software/binary      → identify arch/ABI/libs → compatible: build/test/deploy/verify
                                              → incompatible: fix target/toolchain first
Config/service       → locate active config → backup → minimal edit → validate → reload → runtime verify
Storage/filesystem   → inspect devices/mounts/FS → destructive? explicit authorization required
Network/SSH/mount    → connectivity → config → process → port/mount → test failure/recovery path
Reboot/firmware      → backup → dependency/recovery check → explicit authorization → change → remote verify
Any uncertainty      → STOP → inspect more → do not guess
```
