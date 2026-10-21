# Reskin report — Latchera

## Direction

- **Style:** Abyss Liquidity (`aave-abyss`, dark-technical) — sourced from the
  bundled blockchain style catalog. Live sampling of the ten references returned
  4/10 (Polygon, Base, Cosmos, Sui); `aave.com` itself failed (`fetch failed`),
  so the catalog tokens were used for the chosen direction.
- **Source DNA:** [https://aave.com](https://aave.com) (abstract tokens only —
  no logo, imagery, copy or code reused).
- **Seed:** `5a60d6f78850aac1da2122c2b52c794d4dc3b673f42ab5a422fe8c4dd08d2418`
- **Skeleton:** Command Rail (`command-rail`, linear), replacing the original
  **dashboard-shell** (shell).
- **Accent:** `#8b5cf6` → `#b6509e` — **47.87 ΔE** (threshold 30).

The UI was rebuilt around **Abyss Liquidity** / **Command Rail**; the original
**dashboard-shell** shell and palette were removed while the content contract
stayed byte-for-byte intact (one caveat about a duplicate CSS token is recorded
under *Known limitations*).

## Why this is a different skeleton

| | Original (`dashboard-shell`) | Rebuilt (`Command Rail`) |
|---|---|---|
| Navigation | Sticky 64px top header with a centred horizontal nav and a mobile overlay | Fixed 76px glyph spine on the inline-start edge, rotated micro-labels, floating glass command bar detached from the top edge |
| Page frame | Centred `wrap` (1180px) with alternating ink / night / paper bands | Full-bleed asymmetric bands: 62–104px rotated-marker gutter + ruled body, continuous abyss canvas |
| Hero | Centred copy column beside a giant violet brand mark | Running head + marginal caption beside a drawn vault dial, telemetry strip below a hairline |
| Listings | 3 × 2 rounded paper cards with lock art | Six-cell hairline market tape with oversized numerals |
| Data | Cards, rounded panels, icon columns | Ruled matrices, ledgers, sticky signal panels, horizontal scroll rails |
| Docs | Light content column plus left `<aside>` index | Dark ruled blocks under a sticky horizontal numbered index |
| Palette | Violet accent on ink/paper | Magenta + teal accent on a deep-water ground with a survey grid |
| Type | Self-hosted Gabarito / Hanken Grotesk / Azeret Mono | Trebuchet MS display, Segoe UI body, Cascadia Mono figures |
| Mobile | Sidebar collapses into a full-screen menu | Spine becomes a horizontal glyph dock; folds gain bars; calculators stack |

## Evidence

Screenshots (relative to `website/.reskin/`):

| Before | After |
|---|---|
| ![baseline desktop](baseline/home-desktop.png) | ![current desktop](current/home-desktop.png) |
| ![baseline mobile](baseline/home-mobile.png) | ![current mobile](current/home-mobile.png) |

Side-by-side views: [first viewport](report/compare-desktop-top.png) ·
[the rail / listings band](report/compare-desktop-data.png) ·
[mobile first viewport](report/compare-mobile-top.png)

Additional review captures: `review/home-top-1440.png`,
`review/home-rail-1440.png`, `review/home-combo-1440.png`,
`review/home-keys-1440.png`, `review/home-end-1440.png`,
`review/tablet-1000-top.png`, `review/tablet-1000-mid.png`,
`review/home-top-390.png`, `review/home-rail-390.png`,
`review/home-mid-390.png`, `review/home-foot-390.png`,
`review/docs-full-1440.png`, `review/docs-full-390.png`.

### Verification verdict — PASS

Command:

```bash
node "C:\Users\Administrator\.dsh\skills\reskin\scripts\verify.mjs" check \
  --project "E:\workspace\chuangye\solana\lockin\website" --out .reskin
```

Result: `PASS — 1 route(s), content intact, skeleton replaced, usability clean.`
(`verification.json`, latest run 2026-10-20T16:37Z; full log in `VERIFICATION.md`.)

| Gate | Required | Measured | Result |
|---|---|---:|---|
| Source content contract | no removed/changed/added tokens | 0 issues, 0 warnings | pass |
| Rendered words, `/` @1440 | multiset identical | 730 / 730 | pass |
| Numeric tokens | reported only | 99 / 99 | pass |
| DOM fingerprint similarity | ≤ 0.50 | **0.314** | pass |
| Landmark sequence similarity | ≤ 0.68 | **0.571** | pass |
| CSS class overlap | ≤ 0.10 | **0.017** | pass |
| Accent distance | ≥ 30 ΔE | **47.87** | pass |
| Route status / console | no errors | 200, 0 errors | pass |
| Contrast | 0 failures | **0 / 436** | pass |
| Axe serious/critical | 0 | **0** | pass |
| Horizontal overflow @390 | none | none | pass |
| Labels / alt / accessible names | complete | complete | pass |
| Keyboard focus visible | yes | yes | pass |
| Mobile navigation reachable | yes | dock + sheet | pass |
| Build | passes | `vite build` clean | pass |

Warnings (non-blocking): `aria-label="Hardware"` and `aria-label="Paperwork"` were
added to the two footer `<nav>` elements (the original used plain `<div>`s with
visible labels; the labels themselves are unchanged).

Content contract: rendered and source content is unchanged. Baseline hash
`2b2c360e…`; current hash `aa39f627…`. The delta is a single duplicate entry:
the removed stylesheet also carried `content: 'Copyright 2026 Latchera'`, so the
contract used to list that string twice (CSS + Docs footer). The footer copy is
unchanged and still renders the line; only the obsolete pseudo-element duplicate
is gone (see *Known limitations*).

### Accessibility and responsiveness, beyond the gate

- Axe (WCAG 2.0/2.1/2.2 A + AA) on **both** routes at 1440 × 900 and 390 × 844:
  0 violations.
- No horizontal overflow at 1440, 1000, 768 or 390; the listings tape and docs
  index are explicit scroll regions, the tape is keyboard focusable.
- Focus: `:focus-visible` rings on the command bar, spine, tape, folds, inputs,
  sliders and footer; the spine keeps a visible in-rail ring.
- The vault toggle keeps `aria-pressed`; the sheet keeps `role="dialog"`
  `aria-modal="true"` and closes on Escape; every input keeps its label.
- 19 interaction checks passed (vault toggle, discount readout, lock-length
  selection + unlock date, docs route + deep link `#/docs/contracts`, back
  navigation, dock visibility, sheet open/close, fold collapse, tape focus).

## Changes

New token + layout + component layer:

- `src/styles/abyss.css` — tokens, base, shell, bands, components, responsive,
  motion guards (one global sheet, ~3.4k lines).

Rewritten templates (scripts untouched):

- `src/App.vue` — new template; the `<script setup>` block is byte-identical.
- `src/Docs.vue` — new template; the `<script setup>` block is byte-identical.
- `src/main.js` — stylesheet import only (`./styles/abyss.css`).

Removed from the render path and from disk:

- `src/style.css` (52.6 KB legacy global sheet: `.site-header`, `.hero-*`,
  `.section-*`, `.listing-*`, `.arch-*`, `.docs-*`, the self-hosted font faces
  and the CSS copyright pseudo-element).
- The sticky top header, the centred `wrap` band system, the listing card grid,
  the icon-column architecture, the docs `<aside>` index and the hero brand-mark
  visual.

Also updated:

- `index.html` — `theme-color` `#0c0b10` → `#080d14` (title, description,
  language and all social meta unchanged).
- `website/latchera/` — the deploy mirror's `src` was synced to the same files
  and its legacy `style.css` removed, so the audited tree stays single-sourced.
  Its committed `dist/` was not rebuilt.

## Known limitations

- **Hash delta from the removed pseudo-element.** The legacy stylesheet injected
  `content: 'Copyright 2026 Latchera'` on the docs footer line, duplicating the
  line that is already real markup. Removing the stylesheet leaves the footer
  copy once (as intended). No wording changed, the value multiset is identical
  and the source gate reports 0 issues / 0 warnings; only the duplicate array
  entry (and therefore the hash) disappeared.
- **Docs route coverage.** The source declares one static route (`/`); `#/docs`
  is a hash route and is not enumerated by the verifier. It was verified
  separately: axe 0 at 1440 and 390, no overflow, 11-link index, deep-link
  scrolling, back navigation, and full-page screenshots.
- **Accordion viewport sync.** `syncAccordionViewport()` in `App.vue` still
  queries the legacy `.section-accordion` selector and is now a no-op. Folds
  ship open on every viewport and are collapsible from 1120px down, where the
  summary bar is visible (the wide layout hides it, exactly as the original
  desktop did). No script logic was edited.
- **Deploy mirror build output.** `website/latchera/dist` still contains the
  previous build; run `npm run build` inside `website/latchera` before deploying
  from that checkout.
- No dynamic routes exist, so none were skipped.

The pre-edit `App.vue`, `Docs.vue`, `style.css`, `main.js` and `index.html` are
kept in `.reskin/original-src/` for rollback.
