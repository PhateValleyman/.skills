#!/usr/bin/env bash
# Usage: pack-module.sh <module-dir> [out.zip]
# Creates an ordinary source ZIP; never installs or flashes a device.
set -euo pipefail
[[ $# -ge 1 && $# -le 2 ]] || { echo "usage: $0 <module-dir> [out.zip]" >&2; exit 2; }
DIR=$1
[[ -d "$DIR" ]] || { echo "ERROR: module directory not found" >&2; exit 1; }
DIR=$(cd "$DIR" && pwd -P)
for cmd in zip unzip python3; do command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: missing $cmd" >&2; exit 1; }; done
PROP="$DIR/module.prop"
[[ -f "$PROP" ]] || { echo "ERROR: missing module.prop" >&2; exit 1; }
for k in id name version versionCode author description; do grep -q "^$k=" "$PROP" || { echo "ERROR: module.prop lacks $k" >&2; exit 1; }; done
if grep -q '__ID__\|__NAME__' "$PROP"; then echo "ERROR: unresolved module.prop placeholder" >&2; exit 1; fi
ID=$(grep '^id=' "$PROP" | head -n1 | cut -d= -f2-)
VER=$(grep '^version=' "$PROP" | head -n1 | cut -d= -f2-)
VC=$(grep '^versionCode=' "$PROP" | head -n1 | cut -d= -f2-)
[[ $ID =~ ^[a-zA-Z][a-zA-Z0-9._-]+$ ]] || { echo "ERROR: invalid module id" >&2; exit 1; }
[[ $VC =~ ^[0-9]+$ ]] || { echo "ERROR: versionCode must be an integer" >&2; exit 1; }
[[ ! -e "$DIR/install.sh" ]] || { echo "ERROR: install.sh is reserved; use customize.sh" >&2; exit 1; }
if [[ -d "$DIR/webroot" && ! -f "$DIR/webroot/index.html" ]]; then echo "ERROR: missing webroot/index.html" >&2; exit 1; fi
OUT_ARG=${2:-"$ID-$VER.zip"}
OUT=$(python3 - "$OUT_ARG" "$DIR" <<'PYCODE'
import os, pathlib, sys
out = pathlib.Path(sys.argv[1]).expanduser().resolve()
root = pathlib.Path(sys.argv[2]).resolve()
if os.path.commonpath((str(out), str(root))) == str(root):
    raise SystemExit('ERROR: output ZIP must be outside source directory')
print(out)
PYCODE
)
[[ ! -e "$OUT" && ! -L "$OUT" ]] || { echo "ERROR: refusing to overwrite existing output: $OUT" >&2; exit 1; }
# Refuse symlinks and common credential/local-config artifacts rather than archive them.
python3 - "$DIR" <<'PYCODE'
import os, pathlib, sys
root=pathlib.Path(sys.argv[1]); bad=[]
blocked={'.git','.env','local.properties'}; exts={'.pem','.key','.p12','.pfx','.jks','.keystore'}
for base,dirs,files in os.walk(root,followlinks=False):
    for name in dirs+files:
        p=pathlib.Path(base)/name
        if p.is_symlink() or name in blocked or name.startswith('.env.') or p.suffix.lower() in exts: bad.append(str(p.relative_to(root)))
if bad:
    print('ERROR: remove/review symlinks or likely secret files before packaging:',file=sys.stderr)
    print('\n'.join('  '+x for x in bad),file=sys.stderr); raise SystemExit(1)
crlf=[]
for base,_,files in os.walk(root):
    for name in files:
        if name.endswith(('.sh','.prop','.rule')) or name in ('update-binary','updater-script'):
            p=pathlib.Path(base)/name
            if b'\r' in p.read_bytes(): crlf.append(str(p.relative_to(root)))
if crlf: raise SystemExit('ERROR: CRLF line endings: '+', '.join(crlf))
PYCODE
# Parse shell scripts only; never execute them as part of packaging validation.
shopt -s nullglob
for script in "$DIR"/*.sh; do if ! sh -n "$script"; then echo "ERROR: invalid shell syntax: $script" >&2; exit 1; fi; done
( cd "$DIR" && zip -r9 "$OUT" . -x '*.git*' '*.DS_Store' >/dev/null )
unzip -tq "$OUT" >/dev/null
unzip -Z -1 "$OUT" | grep -qx 'module.prop' || { echo "ERROR: module.prop not at ZIP root" >&2; exit 1; }
echo "Built $OUT"; unzip -Z -1 "$OUT"
echo "Ordinary source ZIP only; installation/flash requires separate authorization and compatibility review."
