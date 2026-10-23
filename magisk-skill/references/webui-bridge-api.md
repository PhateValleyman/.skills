# Bridge API (window.ksu)

MMRL injects `window.ksu` (the name is historical; it is the WebUI bridge). Methods are synchronous Java-bridge calls; results of shell commands come back through **named global callbacks**.

| Method | Purpose |
|---|---|
| `ksu.exec(cmd, optionsJson, callbackName)` | Run `cmd` in a root shell. Callback: `(errno, stdout, stderr)`. |
| `ksu.spawn(cmd, argsJson, optionsJson, callbackName)` | Streaming process. Callback object exposes `stdout`, `stderr`, `exit`, `error` emitters via `callbackName.stdout.emit(...)` etc. |
| `ksu.toast(message)` | Native toast. |
| `ksu.fullScreen(bool)` | Hide/show system bars (UI chrome). |
| `ksu.moduleInfo()` | JSON string with at least module id (and, depending on manager, name/version). Parse with `JSON.parse`. |

`optionsJson` is a JSON string, e.g. `{"cwd":"/data/adb/modules/my.mod","env":{"FOO":"1"}}`.

## Promise wrappers (copy as-is)

```js
const hasBridge = typeof window.ksu !== 'undefined';

function exec(cmd, options = {}) {
  return new Promise((resolve, reject) => {
    const cb = `exec_cb_${Date.now()}_${Math.random().toString(36).slice(2)}`;
    window[cb] = (errno, stdout, stderr) => {
      delete window[cb];
      resolve({ errno, stdout, stderr });
    };
    try {
      ksu.exec(cmd, JSON.stringify(options), cb);
    } catch (e) {
      delete window[cb];
      reject(e);
    }
  });
}

function spawn(cmd, args = [], options = {}) {
  const cb = `spawn_cb_${Date.now()}_${Math.random().toString(36).slice(2)}`;
  const handlers = { stdout: [], stderr: [], exit: [], error: [] };
  const child = {
    on(ev, fn) { handlers[ev].push(fn); return child; },
  };
  window[cb] = {
    stdout: { emit: (_, d) => handlers.stdout.forEach(f => f(d)) },
    stderr: { emit: (_, d) => handlers.stderr.forEach(f => f(d)) },
  };
  window[cb + 'Exit'] = (code) => { handlers.exit.forEach(f => f(code)); cleanup(); };
  function cleanup() { delete window[cb]; delete window[cb + 'Exit']; }
  try { ksu.spawn(cmd, JSON.stringify(args), JSON.stringify(options), cb); }
  catch (e) { handlers.error.forEach(f => f(e)); cleanup(); }
  return child;
}
```

NOTE: the exact event plumbing of `spawn` differs slightly across MMRL versions. If streaming is essential, verify it in the current MMRL docs, or fall back to polling a log file with `exec('tail -n 50 file')`.

## Result handling

- `errno === 0` means success. Always show `stderr` on failure.
- `stdout` is a string with trailing newline; `.trim()` it.
- Large outputs (>~1 MB) may be truncated or slow: write to a file and read in chunks (`sed -n 'A,Bp'`).

## Feature detection

```js
const caps = {
  exec: !!window.ksu?.exec,
  spawn: !!window.ksu?.spawn,
  toast: !!window.ksu?.toast,
  fullScreen: !!window.ksu?.fullScreen,
  moduleInfo: !!window.ksu?.moduleInfo,
};
```
