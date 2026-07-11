# Design QA — The Living Object v1

## Source truth

- Primary direction: `design/references/option-3-living-object.png`
- Ending direction: `design/references/option-2-dark-product-theatre.png`
- Combined comparison: `design/qa/comparison-board-v1.png`
- Product renders: generated specifically for this implementation and stored under `public/product-v1/`

## Implementation captures

- Hero, desktop: `design/qa/implementation-hero-v2.png`
- Story, desktop: `design/qa/implementation-story-listens.png`
- Technical theatre, desktop: `design/qa/implementation-technical.png`
- Finale, responsive narrow state: `design/qa/implementation-footer-v2.png`
- Hero, mobile: `design/qa/implementation-mobile-hero-v2.png`
- Footer, mobile: `design/qa/implementation-mobile-footer-v3.png`

## Viewports and states

- Desktop source comparison: landing page at initial load, 1440 × 1024 emulated viewport.
- Desktop focused comparisons: hero, product-story, technical-theatre, and footer scroll states.
- Mobile comparison: 390 × 844 emulated viewport at hero and footer states.
- The in-app browser's stitched full-page capture repeated scroll segments, so the full-view review uses the source references plus a deterministic montage of focused captures. Each focused capture was also inspected at native resolution.

## Visual comparison

The implementation preserves option 3's warm-white product theatre, centered oversized typography, generous negative space, full-width macro chapters, exploded hardware view, small blue research labels, and restrained navigation. The ending then switches to option 2's near-black technical field, large stacked architecture statement, evidence-led light sections, open-research paper wall, and dark metric footer.

Product imagery is isolated, text-free, and composed for its actual slot. The mobile hero contains the complete puck and both ear clips without cropping. Technical charts use direct labels, restrained axes, and explicit measured/simulated/analytical scope.

## Findings and iteration history

1. **P1 — mobile product crop:** the first hero crop cut into both ear clips. Fixed by using a contained mobile image frame and a dedicated 240 px hero height. Verified in `implementation-mobile-hero-v2.png`.
2. **P2 — desktop hero density:** the first pass crowded the title and product render. Fixed by reducing headline maximum size, tightening top spacing, and increasing the product stage. Verified in `implementation-hero-v2.png`.
3. **P2 — framework image warnings:** corrected non-square favicon dimensions and eagerly loaded scroll-position LCP candidates. Lint, production build, and rendered-HTML tests pass.
4. **P3 — development overlay:** the circular `N` control appears only in local Next.js development captures and is absent from production.

No unresolved P0, P1, or P2 findings remain.

final result: passed
