---
name: generate-minecraft-3d-build-plan
description: Generate Minecraft 3D scene build plans through an authorized Craftsman Agent OneKey Router API. Use for text-to-build-plan requests or integrating its existing Python and TypeScript clients; not for editing live Minecraft worlds.
---


# Generate Minecraft 3D Build Plan

Call Craftsman Agent API OneKey Router to generate a Minecraft 3D scene build plan.

## Quick Start

1. Set your environment variable `DEEPNLP_ONEKEY_ROUTER_ACCESS`.
2. Use the CLI (primary suggested method) or the provided scripts.

## Usage

### 1. CLI (Recommended)

#### CLI Illustration
```shell
npx onekey agent <unique_id> <api_id> $JSON --timeout 60000
```
- `<unique_id>`: the unique identifier of the onekey routed agents, "owner/repo".
- `<api_id>`: refers to the unique endpoint name of API.
- `$JSON`: the json string passed to cli.
- `--timeout`: controls the timeout of API calling, unit is mill seconds.

#### Example
```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=YOUR_ACCESS_KEY
npx onekey agent craftsman-agent/craftsman-agent generate_minecraft_build_plan '{"prompt":"Minecraft scene of Grassland and TNT Block, Purple Crystals","images":[],"mode":"basic"}' --timeout 60000
```

### 2. Python REST API

```bash
python3 scripts/generate_minecraft_build_plan.py --prompt "Minecraft scene of Grassland and TNT Block, Purple Crystals" --mode basic
```

### 3. TypeScript REST API

```bash
node --experimental-strip-types scripts/generate_minecraft_build_plan.ts --prompt "Minecraft scene of Grassland and TNT Block, Purple Crystals" --mode basic
```

## Authentication

Remember to set the environment variable:
```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=YOUR_ACCESS_KEY
```
Get your key at [DeepNLP Workspace](https://www.deepnlp.org/workspace/keys).

## Demo Result

```json
{"success":true,"text":"","images":[{"url":"https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/efd67a8f-a427-4e56-8b00-c02d4eb332d5.png"}]}
```

## Dependencies, authorization and verification
Require an authorized `DEEPNLP_ONEKEY_ROUTER_ACCESS` environment credential; bundled scripts fail without it and never substitute demo credentials. Before a paid API call, verify provider terms and the user's authorization. Verify the installed CLI before using it; optional packages from the source example are `@aiagenta2z/onekey-gateway` and `ai-agent-marketplace`, not automatic global-install instructions. The Python REST client uses the standard library. Resolve scripts relative to this SKILL.md and quote their paths. TypeScript needs a compatible runtime or explicit compilation, not an assumption that every Node release executes `.ts`. Provider contracts differ from the sibling craftsman-agent-build-plans skill; preserve the existing `/agent_router`, `X-OneKey` and `images` contract until verified against provider documentation. Do not claim live endpoint or generation tests passed. Retain the original folder alias when mapping an existing installed skill to the normalized lowercase name.
