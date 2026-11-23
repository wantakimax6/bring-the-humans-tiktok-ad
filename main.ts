// Entry program for bring-the-humans-03.
// The ad itself is the TikTok video this repo points at; this program only
// hands its address to the grader, in a file it can read.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const videoFile = join(botDir, "VIDEO.json");

const raw = readFileSync(videoFile, "utf8");
const parsed = JSON.parse(raw) as { url?: unknown };
if (typeof parsed.url !== "string" || !parsed.url.startsWith("https://www.tiktok.com/")) {
  console.error("VIDEO.json must name a full tiktok.com video address");
  process.exit(1);
}
if (!/\/video\/\d+/.test(parsed.url)) {
  console.error("VIDEO.json address has no /video/<id> in it");
  process.exit(1);
}
if (parsed.url.includes("<handle>") || parsed.url.includes("<id>")) {
  console.error("VIDEO.json still holds the starter placeholder");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(videoFile, join(outDir, "VIDEO.json"));
console.log(`handed in ${parsed.url}`);
