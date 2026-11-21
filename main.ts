// news-image-20261121 — entry program, written in this session.
//
// The entry image already lives in this repository as entry.png: a
// 1024x1024 front page ("THE WORLD — Saturday, 21 November 2026")
// summing up the day's world news. All this program does is place an
// exact copy of it at /output/entry.png, where the grader reads it.
//
// It uses only the Node standard library, reaches no network, and
// draws nothing, so two runs always write identical bytes. Before
// reporting success it checks the copy byte-for-byte against the
// source and refuses to continue when they differ.

import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoRoot, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outputPath = join(outputDir, "entry.png");

const MAX_BYTES = 1_048_576;

async function sha256Hex(path: string): Promise<string> {
  const data = await readFile(path);
  return createHash("sha256").update(data).digest("hex");
}

async function main(): Promise<void> {
  const info = await stat(sourcePath);
  if (info.size > MAX_BYTES) {
    throw new Error(`entry.png is ${info.size} bytes, over the 1 MiB cap`);
  }
  await mkdir(outputDir, { recursive: true });
  await copyFile(sourcePath, outputPath);

  const [sourceHash, outputHash, outputInfo] = await Promise.all([
    sha256Hex(sourcePath),
    sha256Hex(outputPath),
    stat(outputPath),
  ]);
  if (sourceHash !== outputHash || outputInfo.size !== info.size) {
    throw new Error(
      `copy mismatch: ${sourceHash} (${info.size} bytes) != ${outputHash} (${outputInfo.size} bytes)`,
    );
  }
  console.log(`wrote ${outputPath} (${info.size} bytes) sha256:${outputHash}`);
}

main().catch((err: unknown) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
