# Reskin art direction — Paper Protocol

> Selected automatically. Do not ask the user to confirm or choose another direction.

- **Style DNA:** `ethereum-paper` (crypto-editorial)
- **Skeleton:** `gallery-scroll` (spatial)
- **Seed:** `0a611f4a8e1c00f97fd2ec0d8fac934cface300a3ffb23cbde2ea26c695c6100`
- **Source DNA:** [https://ethereum.org](https://ethereum.org)
- **Live sampled:** yes — https://ethereum.org (3198 ms)
- **Original:** document-flow / dark / accent #b6509e

## Why this direction

The selector sampled 9/10 blockchain references, scored every direction for perceptual distance from the original accent (#b6509e) and background (#080d14), added a deterministic seed jitter, and chose Paper Protocol because it is 58 ΔE away from the original accent and pairs with Gallery Scroll, a spatial skeleton rather than the original document-flow.

## Live reference sampling

| Style | URL | Result | Accent sampled | Ground sampled |
|---|---|---|---|---|
| ethereum-paper | https://ethereum.org | ok (3198 ms) | #0c5681 | #ffffff |
| base-cobalt | https://www.base.org | ok (3402 ms) | #0000ff | #dde3e9 |
| polygon-agora | https://polygon.technology | ok (3942 ms) | #670de5 | #000000 |
| solana-spectrum | https://solana.com | ok (4332 ms) | #9945ff | #000000 |
| arbitrum-signal | https://arbitrum.io | failed: HTTP 403 | — | — |
| aave-abyss | https://aave.com | ok (3335 ms) | #ff0000 | #000000 |
| cosmos-orbit | https://cosmos.network | ok (3561 ms) | #40b3ff | #000000 |
| optimism-poster | https://www.optimism.io | ok (7167 ms) | #ff0421 | #fafaf9 |
| uniswap-bubblegum | https://uniswap.org | ok (8336 ms) | — | #ffffff |
| sui-tidal | https://sui.io | ok (8219 ms) | #298dff | #ffffff |

Live sampling is evidence, not a copy target. Never download or reuse a reference site's logo, imagery, copy, or code. Use only the abstract tokens below.

## Candidate ranking

| Candidate | Score | Accent ΔE from original | Layout | Live |
|---|---:|---:|---|---|
| Paper Protocol | 0.9048 | 57.7 | gallery-scroll | yes |
| Abyss Liquidity | 0.8869 | 94.8 | orbital | yes |
| Cosmos Orbit | 0.879 | 66.1 | gallery-scroll | yes |
| Signal Navy | 0.8741 | 64.8 | bento-canvas | no |
| Tidal Sui | 0.856 | 53.5 | split-stage | yes |
| Poster Optimism | 0.7959 | 86 | gallery-scroll | yes |
| Cobalt Blueprint | 0.7875 | 91.2 | split-stage | yes |
| Spectrum Terminal | 0.7738 | 58.5 | ticker-stage | yes |
| Agora Violet | 0.6776 | 57.7 | bento-canvas | yes |
| Bubblegum Exchange | 0.6318 | 34 | bento-canvas | yes |

## Skeleton brief

**Gallery Scroll** — full-viewport panels with generous negative space; horizontal scroll-snap for related panels; minimal floating dock navigation; each route is a sequence of framed scenes; large imagery/typography and very few borders.

Navigation: Floating dock at the bottom (icons + accessible names) and a vertical dot index for sections; no conventional header.

Structure:
1. opening panel with brand and route count
1. scene panels with snap points
1. horizontal data rail
1. closing panel with form/action
1. floating dock

Content mapping: Group each route's content into 2-4 scenes. Keep metrics as large typographic facts. Tables become horizontal snap rails with one record per panel on mobile. Forms become the closing scene.

Recipe: `.scene{min-height:100svh;display:grid;place-content:center;padding:clamp(24px,6vw,96px);scroll-snap-align:start}.rail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px}.rail>*{scroll-snap-align:start;flex:0 0 min(86vw,520px)}.dock{position:fixed;bottom:18px;left:50%;translate:-50% 0;display:flex;gap:6px;border-radius:999px}`

Risks: full-viewport panels can hide content below the fold; provide visible scroll cues; horizontal rails need keyboard and touch support

## Design tokens

```css
:root {
  --bg: #ffffff;
  --surface: #FFFDF8;
  --surface-alt: #EDE9DF;
  --ink: #1B1B1B;
  --muted: #6B675F;
  --accent: #0c5681;
  --accent-safe: #0c5681;
  --accent-2: #8B9DFF;
  --line: #D9D3C7;
  --success: #2F6B4F;
  --danger: #A83A2A;
  --warning: #8A5A00;

  --font-display: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  --font-body: "Charter", "Georgia", "Segoe UI", serif;
  --font-mono: "Courier New", ui-monospace, monospace;
  --display-weight: 500;
  --display-tracking: -0.025em;
  --label-tracking: 0.12em;

  --radius-sm: 0px;
  --radius-md: 2px;
  --radius-lg: 4px;
  --border: 1px solid var(--line);
  --shadow: none;

  --motion-duration: 300ms;
  --motion-ease: ease-out;
  --space-1: clamp(4px, .35vw, 6px);
  --space-2: clamp(8px, .7vw, 12px);
  --space-3: clamp(14px, 1.2vw, 20px);
  --space-4: clamp(22px, 2vw, 32px);
  --space-5: clamp(36px, 3.4vw, 56px);
  --space-6: clamp(56px, 5vw, 88px);
  --page-pad: clamp(18px, 4vw, 64px);
  --max-width: 1440px;
}
```

## Component grammar

- Surface: 1px solid var(--line); radius 2px; shadow none.
- Type: display **"Iowan Old Style", "Palatino Linotype", Georgia, serif** at weight 500, tracking -0.025em; body **"Charter", "Georgia", "Segoe UI", serif**; numerals and micro-labels **"Courier New", ui-monospace, monospace**.
- Texture: newsprint rules, drop caps, marginalia labels, ether gradient wash.
- Motion: quiet, 300ms, ease-out. Always wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.
- Density: comfortable. Keep body text >= 14px and body contrast >= 4.5:1.
- Use `--accent-safe` for text and icons on `--bg`; use `--accent` for fills and large shapes.

## Originality guard

The replacement must satisfy all of these:

1. The source inventory archetype is `document-flow`; the new skeleton is `gallery-scroll`. Do not fall back to the old shell during implementation.
2. Do not reuse any original class name, CSS selector, design token name, or original accent family.
3. Rewrite templates, not only CSS. Every route must visibly use the new skeleton.
4. Keep every token in `.reskin/content-contract.json`; move it, never rewrite it.
5. Run `node scripts/verify.mjs check` and do not stop until content, structure, accessibility and responsive checks pass.

## Commit statement

Use this sentence in the final report: "The UI was rebuilt around Paper Protocol / Gallery Scroll; the original document-flow shell and palette were removed while the content contract stayed byte-for-byte intact."
