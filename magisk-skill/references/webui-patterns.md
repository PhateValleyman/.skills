# Recipes

## Safe shell quoting (always use for user input)
```js
const shq = (s) => `'${String(s).replace(/'/g, `'\\''`)}'`;
await exec(`echo ${shq(userValue)} > ${shq(path)}`);
```

## Module paths
```js
const MODID = 'my.module';              // or JSON.parse(ksu.moduleInfo()).id
const MODDIR = `/data/adb/modules/${MODID}`;
const CONF = `${MODDIR}/config.prop`;   // persistent config next to the module
```
Prefer `/data/adb/<modid>/` for user data that must survive module updates.

## Read / write key=value config
```js
async function readConf() {
  const { stdout } = await exec(`cat ${shq(CONF)} 2>/dev/null`);
  return Object.fromEntries(stdout.split('\n')
    .filter(l => l.includes('=') && !l.startsWith('#'))
    .map(l => { const i = l.indexOf('='); return [l.slice(0, i).trim(), l.slice(i + 1).trim()]; }));
}
async function writeConf(obj) {
  const body = Object.entries(obj).map(([k, v]) => `${k}=${v}`).join('\n') + '\n';
  const r = await exec(`printf %s ${shq(body)} > ${shq(CONF)}`);
  if (r.errno) throw new Error(r.stderr || 'write failed');
}
```

## Toggle a service / script
```js
const status = async () => (await exec(`pidof mydaemon`)).errno === 0;
const start  = () => exec(`sh ${MODDIR}/service.sh >/dev/null 2>&1 &`);
const stop   = () => exec(`pkill -f mydaemon`);
```

## Live log (polling, works everywhere)
```js
let timer;
function followLog(file, el) {
  clearInterval(timer);
  timer = setInterval(async () => {
    const { stdout } = await exec(`tail -n 200 ${shq(file)}`);
    el.textContent = stdout;
    el.scrollTop = el.scrollHeight;
  }, 1500);
}
```

## Install an app list / pick from packages
```js
const { stdout } = await exec(`pm list packages -3 | sed 's/package://' | sort`);
const pkgs = stdout.trim().split('\n');
```

## System properties
```js
const getprop = async (k) => (await exec(`getprop ${shq(k)}`)).stdout.trim();
const setprop = (k, v) => exec(`setprop ${shq(k)} ${shq(v)}`);
```

## Reboot actions
```js
const reboot = (mode = '') => exec(`svc power reboot ${mode}`);
```

## Loading local assets
Use relative `fetch('./data.json')`; it is served from `webroot/`.
Images/fonts: reference with relative paths or inline as data URIs.

## UX rules of thumb
- Disable buttons while a command runs; show a spinner.
- Toast on success (`ksu.toast` when present, DOM toast otherwise).
- Confirm destructive actions (rm, reboot, flash).
