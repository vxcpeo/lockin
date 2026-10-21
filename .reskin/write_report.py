"""Write the reskin report (the previous .reskin/REPORT.md was archived)."""

import pathlib

TEXT = """# Reskin report — Holdavia website

## Direction

- **Style:** Paper Protocol (`ethereum-paper`, crypto-editorial) — sampled live from
  [ethereum.org](https://ethereum.org) (3 198 ms), then scored against the nine other
  blockchain references. No logo, image, copy or code from a reference is used.
- **Skeleton:** **Gallery Scroll** (`gallery-scroll`, spatial), replacing the original
  **document-flow** (editorial) shell.
- **Seed:** `0a611f4a8e1c00f97fd2ec0d8fac934cface300a3ffb23cbde2ea26c695c6100`
- **Live sampling:** 9 / 10 references reachable (arbitrum.io returned HTTP 403); the
  catalogue tokens were used for the chosen direction.
- **Accent:** `#b6509e` → `#0c5681` — **57.72 ΔE** (threshold 30).
- **Type:** Iowan Old Style / Palatino / Georgia display, Charter / Georgia body,
  Courier New numerals and micro-labels.
- **Ground:** paper white `#ffffff` with a faint ruled grid, warm surface `#fffdf8`,
  hairline `#d9d3c7`, zero-to-2px radii and no shadows.

The UI was rebuilt around **Paper Protocol** / **Gallery Scroll**; the original
**document-flow** shell and palette were removed while the content contract stayed
byte-for-byte intact.

## Why this is a different skeleton

| | Original (`document-flow`) | Rebuilt (`Gallery Scroll`) |
|---|---|---|
| Navigation | 76 px glyph spine pinned to the inline-start edge, rotated labels, floating glass command bar, full-screen section sheet | Single floating paper dock at the bottom with straight micro-labels, plus a top-right index button that opens a paper overlay |
| Page frame | Continuous dark canvas with ruled bands and a fixed gutter | A sequence of white paper scenes, each at least one viewport tall, separated by hairlines |
| Hero | Copy column beside a drawn vault dial on a dark ground | Opening plate: serif display + italic accent, hairline telemetry strip, and a ring "seal" that toggles |
| Listings | Six-cell tape with oversized numerals on a dark rail | Horizontal snap rail of matted paper plates |
| Data | Ledgers and matrices on near-black panels | Ruled ledgers, a two-column comparison table, fee streams on paper |
| Steps | Five stacked numbered rows in a dark band | Ruled numbered ledger beside a bordered signal panel (a scroll rail below 1080 px) |
| Palette | Deep-water navy + magenta accent | Paper white + deep-blue accent `#0c5681` |
| Type | Trebuchet MS / Segoe UI / Cascadia Mono | Iowan Old Style / Charter / Courier New |
| Mobile | Spine becomes a glyph dock; sheet unchanged | Dock wraps to two rows at the bottom; scenes stack; rails become one-plate-per-swipe |

## Evidence

Screenshots (relative to `website/.reskin/`):

| Before | After |
|---|---|
| ![baseline desktop](baseline/home-desktop.png) | ![current desktop](current/home-desktop.png) |
| ![baseline mobile](baseline/home-mobile.png) | ![current mobile](current/home-mobile.png) |

Review captures used during the pass: `review-hero.png`, `review-timelock.png`,
`review-full-desktop.png`, `review-top-mobile.png`, and the separately captured docs
route in `.rebrand/docs-shot3/screenshots/`.

### Verification verdict — PASS

```bash
node "C:\\Users\\Administrator\\.dsh\\skills\\reskin\\scripts\\verify.mjs" check \\
  --project "E:\\workspace\\chuangye\\solana\\lockin\\website" --out .reskin
```

`PASS — 1 route(s), content intact, skeleton replaced, usability clean.`
(`verification.json`, latest run; log in `VERIFICATION.md`.)

| Gate | Required | Measured | Result |
|---|---|---:|---|
| Source content contract | no removed/changed tokens | 0 issues, 2 additive warnings | pass |
| Rendered words, `/` @1440 | multiset identical | 730 / 730 | pass |
| Numeric tokens | reported only | 99 / 99 | pass |
| DOM fingerprint similarity | <= 0.50 | **0.289** | pass |
| Landmark sequence similarity | <= 0.68 | **0.571** | pass |
| CSS class overlap | <= 0.10 | **0.022** | pass |
| Accent distance | >= 30 dE | **57.72** | pass |
| Route status / console | no errors | 200, 0 errors | pass |
| Contrast | 0 failures | **0 / 436** | pass |
| Axe serious/critical | 0 | **0** | pass |
| Horizontal overflow @390 | none | none | pass |
| Labels / alt / accessible names | complete | complete | pass |
| Keyboard focus visible | yes | yes | pass |
| Mobile navigation reachable | yes | dock (two rows) + index overlay | pass |
| Build | passes | `vite build` clean | pass |

Source contract hash: `2aff2e61c4f34eab9a808129ec8fa6340067d91dfdb38dbf417a7c4926686cdd`.

Warnings (non-blocking): the dock adds one extra `#top` link and two accurate
`aria-label`s ("Holdavia home", "Open the section list"), and the duplicated
`aria-label="Paperwork"` now exists once instead of twice.

## Changes

New presentation layer:

- `src/styles/paper.css` — tokens, reset, twelve-column scene grid, rails, dock,
  article blocks, docs layout, responsive rules, reduced-motion guards.
- `src/App.vue` — new template; `<script setup>` byte-identical (232 lines).
- `src/Docs.vue` — new template; `<script setup>` byte-identical (91 lines).
- `src/main.js` — stylesheet import only (`./styles/paper.css`).
- `index.html` — `theme-color` `#080d14` -> `#ffffff` (title, description, language,
  social meta unchanged).
- `src/styles/abyss.css` — removed from disk and from the render path (backup in
  `.reskin/original-src/`).
- `website/deploy/` — the deploy mirror's `src/`, `index.html` and stylesheet were
  synced to the same files so the audited tree stays single-sourced.
- `public/brand/*.svg` — the mark tile recoloured from the old accent `#b6509e` to the
  new accent `#0c5681` so the favicon, the in-page mark and the dock monogram share one
  brand colour.

Removed from the render path: the sticky glyph spine, the floating command bar, the
section-sheet styling, the dark band system, the tape, the plate captions, the light
docs aside, and every `lt-*` class and `--abyss*` / `--lt-*` token.

### Interaction parity

- Vault/seal toggle keeps `aria-pressed`, both handlers and both label branches.
- Discount slider, both number inputs, the four lock-length buttons, the unlock-date
  readout and all six computed figures keep their exact expressions.
- The five `<details>` disclosures stay `open` by default; their summaries are visible
  from 1120 px down and hidden above it, matching how the original page exposed them.
- Hash routing, docs deep links, mobile menu open/Escape/close and scroll restoration
  were exercised manually and in the capture pass.

## Accessibility and responsiveness

- One `h1` on `/` and one on `/#/docs`; `main`, `footer`, `nav` landmarks; the dock has
  an accessible label; every control has an accessible name.
- Axe (WCAG 2.0/2.1/2.2 A + AA) on `/` at 1440 and 390: 0 violations, 0 contrast
  failures across 436 checks. The docs route was checked separately at 1440 and 390.
- No horizontal overflow at 1440, 1080, 768 or 390. The listings rail and the mobile
  step rail are explicit scroll regions; the listings rail keeps `tabindex="0"`.
- Focus rings on dock links, index button, seal, buttons, inputs, slider, rail and
  footer links. Motion is limited to colour/transform transitions and is disabled under
  `prefers-reduced-motion`.
- Mobile: scenes stack, the dock wraps to two rows inside the safe-area margin, tables
  become stacked rows, and the workbook becomes a single column.

## Known limitations

- **Docs route coverage.** The source declares one static route (`/`); `/#/docs` is a
  hash route the verifier does not enumerate. It was captured and reviewed separately
  (`.rebrand/docs-shot3/`): masthead, chip index, ruled blocks, footer, mobile stack.
- **Deploy mirror.** `website/deploy` is a git checkout deployed separately; its `dist/`
  was not rebuilt here. Run `npm run build` inside it before deploying from that
  checkout.
- **Brand raster assets.** The favicon PNG/OG card and the X-kit PNGs carry the previous
  accent until the rebrand asset pass that follows this reskin regenerates them.
- Pre-edit `App.vue`, `Docs.vue`, `main.js`, `index.html` and `abyss.css` are kept in
  `.reskin/original-src/` for rollback.
"""

path = pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website\.reskin\REPORT.md")
path.write_text(TEXT, encoding="utf-8")
print("wrote", path, len(TEXT), "chars")
