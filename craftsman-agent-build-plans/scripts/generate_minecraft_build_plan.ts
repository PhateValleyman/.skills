#!/usr/bin/env node

const ENDPOINT = "https://agent.deepnlp.org/agent";
const UNIQUE_ID = "craftsman-agent/craftsman-agent";
const API_ID = "generate_minecraft_build_plan";
const ENV_KEY = "DEEPNLP_ONEKEY_ROUTER_ACCESS";


function parseArgs(argv: string[]) {
  const args: Record<string, string | string[]> = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--prompt" || token === "--mode" || token === "--ref-image-url") {
      const value = argv[i + 1];
      i += 1;
      if (token === "--ref-image-url") {
        const list = (args[token] as string[]) || [];
        list.push(value);
        args[token] = list;
      } else {
        args[token] = value;
      }
    }
  }

  return {
    prompt: (args["--prompt"] as string) || "",
    mode: (args["--mode"] as string) || "basic",
    refImageUrl: (args["--ref-image-url"] as string[]) || [],
  };
}

async function main() {
  const { prompt, mode, refImageUrl } = parseArgs(process.argv.slice(2));
  if (!prompt) {
    console.error("Missing --prompt");
    process.exit(1);
  }

  let apiKey = process.env[ENV_KEY];
  if (!apiKey) {
    throw new Error("Missing DEEPNLP_ONEKEY_ROUTER_ACCESS; no request was sent.");
  }

  const url = new URL(ENDPOINT);
  url.searchParams.set("onekey", apiKey);

  const payload = {
    unique_id: UNIQUE_ID,
    api_id: API_ID,
    data: {
      prompt,
      ref_image_url: refImageUrl,
      mode,
    },
  };

  const response = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(60000),
  });

  const text = await response.text();
  if (!response.ok) {
    console.error(`HTTP ${response.status}; response body omitted to protect credentials.`);
    process.exit(1);
  }

  try {
    const json = JSON.parse(text);
    console.log(JSON.stringify(json, null, 2));
  } catch {
    console.log(text);
  }
}

main().catch((err) => {
  console.error("Request failed. Check credentials, network and runtime; sensitive details omitted.");
  process.exit(1);
});
