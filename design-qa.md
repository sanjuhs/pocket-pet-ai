# Design QA — Option 3 + Option 2 ending

## Source visual truth

- Option 3 page: `design/references/option-3-living-object.png`
- Option 2 ending: `design/references/option-2-dark-product-theatre.png`
- Direct side-by-side board: `design/qa/comparison-board-v2.png`

## Browser-rendered implementation evidence

- Desktop hero: `design/qa/final-hero.png`
- Desktop product story: `design/qa/final-hardware.png`
- Desktop principles and Option 3 evidence: `design/qa/final-principles.png`
- Desktop Option 2 architecture: `design/qa/final-architecture.png`
- Desktop proof section: `design/qa/final-evidence.png`
- Desktop research and footer: `design/qa/final-footer.png`
- Mobile hero: `design/qa/mobile-hero-v5.png`
- Mobile product story after readability correction: `design/qa/mobile-hardware-v8.png`
- Mobile action chapter after readability correction: `design/qa/mobile-acts-v8.png`
- Mobile architecture: `design/qa/mobile-architecture-v5.png`
- Mobile footer: `design/qa/mobile-footer-v5.png`

## Viewports and state

- Desktop: 1440 × 1024, landing-page route, initial and anchored section states.
- Mobile: 390 × 844, landing-page route, hero, product-story, architecture, and footer states.
- Full-view comparison: `comparison-board-v2.png` pairs the complete source pages with focused browser captures for each major region. A focused montage was used because the in-app browser’s stitched full-page capture repeated scroll segments.
- Focused comparisons were required because the source is a 725 × 2168 overview and typography, product crops, charts, and footer metrics are too small to judge accurately from the complete source alone.

## Required fidelity surfaces

- **Fonts and typography:** Geist’s neutral grotesk forms closely match the source’s Apple-like sans serif. Display weights, negative tracking, compact line heights, blue mono labels, small evidence copy, and desktop headline wrapping match the reference hierarchy. Mobile display lines reflow without clipping.
- **Spacing and layout rhythm:** Desktop uses the source’s narrow navigation, centered hero, four-column proof strip, three alternating product chapters, four-column principle row, compact research board, three-column architecture, two-column proof row, paper tableau, and horizontal black footer. Section heights were reduced from the earlier oversized implementation to match the source density.
- **Colors and tokens:** Warm ivory `#f7f6f2`, warm section surface `#f0ede7`, near-black `#03060b`, muted gray, restrained cobalt labels, and hairline dividers map directly to the two references. The previous dark architecture section was replaced with Option 2’s light technical surface.
- **Image quality and asset fidelity:** All visible product and architecture illustrations are raster assets. Product family, microphone macro, exploded puck, light accelerator macro, ternary lattice, latent-memory stack, evidence charts, primary papers, and whitepaper cover are sharp and composed for their consuming slots. No CSS art, placeholder illustration, handcrafted SVG art, or text baked into generated product imagery is used.
- **Copy and content:** The visible narrative follows Option 3’s “It listens / remembers / acts” progression, then Option 2’s “Ternary weights / Latent memory / Real recall,” “Built to be proven,” and “Open research / Real rigor.” Hardware claims remain explicitly labeled measured, simulated, analytical, target, estimate, or concept.
- **Icons and interactions:** Iconoir icons use consistent stroke weights. Desktop Research navigation was clicked in the browser and resolved uniquely to `#research`; homepage, research route, GitHub links, whitepaper route, PDF, and evidence links are real targets. Hover and focus styles remain visible.
- **Accessibility and responsiveness:** Semantic navigation and headings, descriptive image alt text, reduced-motion handling, readable mobile text blocks, contained hero art, practical tap targets, and no horizontal overflow were verified. The mobile product chapters now separate copy from imagery instead of laying low-contrast text over dark hardware.

## Findings and comparison history

1. **P1 — ending used the wrong dark architecture surface.**
   - Earlier evidence: `design/qa/implementation-technical.png`.
   - Source difference: Option 2 places the architecture, proof, and research sections on warm white, reserving near-black for the footer.
   - Fix: rebuilt the architecture as a light three-column research panel and kept black only for the final footer.
   - Post-fix evidence: `design/qa/final-architecture.png` and `design/qa/final-footer.png`.
2. **P1 — Option 3 evidence board was missing as a distinct chapter.**
   - Earlier evidence: `design/qa/comparison-board-v1.png` moved directly from principles to the Option 2 architecture treatment.
   - Fix: added the exact centered “Research and evidence” board with measured chart, simulated FPGA pathway, and primary-download column.
   - Post-fix evidence: `design/qa/final-principles.png`.
3. **P2 — product chapters were roughly twice the source height and display type was oversized.**
   - Fix: reduced listens/remembers/acts heights, brought headings to the source optical scale, tightened paragraph measures, and matched warm section boundaries.
   - Post-fix evidence: `design/qa/final-hardware.png` and `design/qa/final-principles.png`.
4. **P2 — “It acts” used a black accelerator asset instead of the source’s warm light product macro.**
   - Fix: generated `public/product-v2/story/acts-light.png` with left copy space and a right-weighted open puck.
   - Post-fix evidence: `design/qa/v4-acts-settled.png`.
5. **P2 — architecture visuals did not match Option 2’s editorial lattice and memory objects.**
   - Fix: generated `ternary-lattice.png` and `latent-memory.png`, then paired them with the measured adaptation chart.
   - Post-fix evidence: `design/qa/final-architecture.png`.
6. **P2 — mobile story copy lost contrast over dark hardware imagery.**
   - Fix: separated each mobile copy block onto a warm solid surface above its product image.
   - Post-fix evidence: `design/qa/mobile-hardware-v8.png` and `design/qa/mobile-acts-v8.png`.

No unresolved P0, P1, or P2 findings remain. The circular `N` visible in local captures is the Next.js development overlay and does not ship in production.

## Browser verification

- Primary interaction tested: desktop Research navigation.
- Result: one unique target; URL changed to `http://localhost:3000/#research`.
- Browser console errors/warnings on the fresh verification tab: none.
- Local prototype remained running after verification.

final result: passed
