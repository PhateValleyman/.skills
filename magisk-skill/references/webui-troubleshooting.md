# Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| WebUI button missing in manager | No `webroot/index.html`, or module not enabled | Check zip layout: `webroot/` at zip root; module enabled and rebooted |
| Blank page | Absolute asset paths (`/app.js`) or JS error | Use `./app.js`; open remote debugging (`chrome://inspect`) if WebView debuggable |
| `ksu is not defined` | Opened in a normal browser, or manager lacks WebUI | Use the mock path in the template; update manager |
| Command never returns | Callback name collision or command waits for stdin | Unique callback names; add `</dev/null`; background long jobs with `&` |
| Quotes/spaces break command | Raw string concatenation | Use `shq()` |
| Works in one MMRL version, not another | Reliance on a version-specific API | Feature-detect; stay on `window.ksu` basics |
| `Permission denied` on file | SELinux context or wrong path | Check with `ls -Z`; use module dir or `/data/adb/<id>/` |
| Config lost after update | Stored inside module dir | Store user data under `/data/adb/<id>/` |
| Zip installs but "not a valid module" | Files nested in a folder inside the zip | Re-pack with `scripts/pack-module.sh` (zips contents, not the folder) |
| Fonts/icons missing | CDN blocked/offline | Bundle locally |
