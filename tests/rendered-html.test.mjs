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

  assert.match(page, /The Living Object/);
  assert.match(page, /Ternary weights/);
  assert.match(page, /Built to be proven/);
  assert.match(page, /Open research/);
  assert.match(page, /deterministic policy gate/);
  assert.match(page, /no custom silicon has been fabricated/i);
  assert.match(layout, /Pocket Pet AI/);
  assert.match(layout, /product-family\.png/);
  assert.match(css, /prefers-reduced-motion/);
  assert.match(packageJson, /"name": "pocket-pet-ai"/);
  assert.doesNotMatch(page + layout + packageJson, /codex-preview|SkeletonPreview|site-creator-vinext-starter/);
});

test("ships responsive product imagery and the embedded research surface", async () => {
  const research = await readFile(new URL("app/research/page.tsx", root), "utf8");
  assert.match(research, /pocket-pet-ai-whitepaper\.pdf/);
  assert.match(research, /<iframe/);

  await Promise.all([
    access(new URL("public/product-v1/hero/product-family.png", root)),
    access(new URL("public/product-v1/story/listens-macro.png", root)),
    access(new URL("public/product-v1/story/exploded-memory.png", root)),
    access(new URL("public/product-v1/story/acts-silicon.png", root)),
    access(new URL("public/product-v2/story/acts-light.png", root)),
    access(new URL("public/product-v2/architecture/ternary-lattice.png", root)),
    access(new URL("public/product-v2/architecture/latent-memory.png", root)),
    access(new URL("public/product-v1/research/evidence.png", root)),
    access(new URL("public/product-v1/whitepaper/cover.png", root)),
  ]);
});
