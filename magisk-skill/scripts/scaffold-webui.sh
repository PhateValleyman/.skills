#!/usr/bin/env bash
# Usage: scaffold-webui.sh <module-dir> <module-id> "<Module Name>"
set -euo pipefail
[[ $# -eq 3 ]] || { echo "usage: $0 <module-dir> <id> \"<Name>\"" >&2; exit 2; }
DIR=$1; ID=$2; NAME=$3
[[ $ID =~ ^[a-zA-Z][a-zA-Z0-9._-]+$ ]] || { echo "invalid module id" >&2; exit 1; }
HERE=$(cd "$(dirname "$0")/.." && pwd)
if [[ -e "$DIR" ]] && [[ -n "$(find "$DIR" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then echo "ERROR: target exists and is not empty" >&2; exit 1; fi
mkdir -p "$DIR"
cp -R "$HERE/assets/webui-starter/." "$DIR/"
python3 - "$DIR" "$ID" "$NAME" <<'PYCODE'
from html import escape
from pathlib import Path
import sys
root=Path(sys.argv[1]); mid,name=sys.argv[2:]
if not name.strip() or any(c in name for c in '\r\n'): raise SystemExit('ERROR: name must be non-empty and single-line')
p=root/'module.prop'; p.write_text(p.read_text(encoding='utf-8').replace('__ID__',mid).replace('__NAME__',name),encoding='utf-8')
p=root/'webroot/index.html'; s=p.read_text(encoding='utf-8'); label=escape(name,quote=True)
s=s.replace('<title>Module WebUI</title>',f'<title>{label}</title>').replace('<h1 id="title">Module WebUI</h1>',f'<h1 id="title">{label}</h1>')
p.write_text(s,encoding='utf-8')
PYCODE
echo "Created inert WebUI skeleton in $DIR; review before packaging."
