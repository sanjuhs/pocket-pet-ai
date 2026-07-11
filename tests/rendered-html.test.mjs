import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("ships the complete product narrative without starter markers", async () => {
  const [page, layout, css, packageJson] = await Promise.all([
    readFile(new URL("app/page.tsx", root), "utf8"),
    readFile(new URL("app/layout.tsx", root), "utf8"),
    readFile(new URL("app/globals.css", root), "utf8"),
    readFile(new URL("package.json", root), "utf8"),
  ]);

  assert.match(page, /A personal AI/);
  assert.match(page, /STAGE 01/);
  assert.match(page, /STAGE 02/);
  assert.match(page, /The model proposes/);
  assert.match(page, /architecture targets, not measured silicon/i);
  assert.match(layout, /Pocket Pet AI/);
  assert.match(layout, /og\.png/);
  assert.match(css, /prefers-reduced-motion/);
  assert.match(packageJson, /"name": "pocket-pet-ai"/);
  assert.doesNotMatch(page + layout + packageJson, /codex-preview|SkeletonPreview|site-creator-vinext-starter/);
});

test("ships responsive product imagery and the embedded research surface", async () => {
  const research = await readFile(new URL("app/research/page.tsx", root), "utf8");
  assert.match(research, /pocket-pet-ai-whitepaper\.pdf/);
  assert.match(research, /<iframe/);

  await Promise.all([
    access(new URL("public/images/pocket-pet-in-use.png", root)),
    access(new URL("public/images/pocket-pet-architecture.png", root)),
    access(new URL("public/images/pocket-pet-product-system.png", root)),
    access(new URL("public/og.png", root)),
  ]);
});
