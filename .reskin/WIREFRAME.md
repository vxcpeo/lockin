# Reskin wireframe — Latchera

Commitment written before implementation. The selected direction is **Abyss Liquidity
(`aave-abyss`)** with the **Command Rail (`command-rail`)** skeleton, replacing the
original `dashboard-shell` (sticky top header + centred nav + alternating bands +
card grid).

## 1. New shell

| Piece | Name | Role |
|---|---|---|
| Root | `.lt-app` | Full-bleed dark canvas, 76px inline start padding for the spine |
| Command bar | `.lt-command` | Floating glass bar, sticky 14px below the top edge: wordmark, live pill, the two hero actions, compact menu trigger |
| Spine | `.lt-spine` | Fixed 76px glyph rail on the inline start edge; two nav groups (sections + paperwork) with rotated micro-labels |
| Section sheet | `.lt-sheet` | Full-screen index opened from the command bar on compact widths |
| Main | `.lt-main` | Bands, plates and the closing call |
| Footer | `.lt-foot` | Wordmark column, Hardware / Paperwork navs, legal line |

The old shell (`header.site-header` + `nav.desktop-nav` + centred `.wrap` bands +
`.section` alternation + `.site-footer`) is removed from the render path.

## 2. Route to layout

| Route | Layout |
|---|---|
| `/` (hash `#top`) | `lt-app` → `lt-command` → `lt-spine` → `lt-main` (17 bands/plates) → `lt-foot` |
| `#/docs` and `#/docs/:section` | `lt-app lt-app--docs` → `lt-command` (docs variant) → `lt-docs` (hero + horizontal sticky index + 11 ruled blocks) → `lt-foot` |

The docs route keeps no left sidebar: the old `<aside class="docs-index">` becomes a
sticky horizontal numbered strip (`lt-docs-index`), and every block is a full-width
ruled entry with a monospace tag.

## 3. Composition per home band

| Band | New composition |
|---|---|
| `#top` hero | Asymmetric two-column stage: running head + lede on the left, drawn vault dial on the right; telemetry strip (3 figures + note) pinned under a hairline |
| `#rail` | Section marker in the rotated gutter, oversized head + marginal note, then a six-cell horizontal market tape with hairlines (no cards), legend row below |
| Plate | Full-bleed photo plate with the two-line caption on a dark gradient, no centred wrap |
| `#time-lock` | Head + small figure; numbered step ledger on the wide column, sticky signal panel (pool line, actors, fees) on the narrow column |
| `#combination` | Dial console (glass) on the left; comparison ledger on the right; burn row and footnote across the base |
| `#old-locks` | Two-column numbered issue ledger, then the two-column comparison table as a ruled list, closing line |
| `#keys` | Key treatise + figure + floating ticket on the left, numbered claim ledger on the right, position record as a ruled strip below |
| Plate | Full-bleed photo plate, caption right-aligned |
| `#master-key` | Four-cell ruled matrix, vertical contract map (TRANSACTIONS → READS → VALUE), limits + spec ledger |
| `#strongbox` | Two fee streams as labelled bars, four-cell share matrix with inline bars, note under a rule |
| `#workings` | Contract map repeated as a wide strip + limits + spec ledger |
| `#pick-proof` | Two-column check ledger in a ruled matrix |
| `#workshop` | Four phase columns in a ruled matrix, exclusions strip |
| `#spec-sheet` | Two-column decision ledger, then measured / ignored gauge columns |
| `#weak-points` | Holds vs gives-way columns, then a three-cell risk strip |
| Finale | Centred closing line over a ghost row of lock glyphs |
| `#app` | Closing call: running head left, two actions right, accent gradient wash |
| Footer | Wordmark column, two ruled nav columns, legal + copyright status line |

## 4. Kept vs removed

- Kept as content-only: the two hero actions (moved into the command bar), the
  vault toggle pair, the cost dial and its form fields, the five `<details>`
  disclosures, every image plate + `picture/source` pair, the docs loops.
- Removed: `style.css` (all of it), the sticky top header, the centred `wrap`
  bands, the six listing cards, the three-arrow architecture columns, the docs
  `<aside>` index, the hero brand-mark visual, the old section accordion styling.
- Scripts: `App.vue` and `Docs.vue` script blocks are byte-identical to the
  original; `main.js` changes only its stylesheet import.

## 5. Styling layer

- One global sheet: `src/styles/abyss.css` (tokens → base → shell → bands →
  components → responsive → motion).
- Tokens: `--abyss` `#080D14`, `--surface` `#111A24`, `--ink` `#F4F7FA`,
  `--muted` `#8FA3B5`, `--accent` `#B6509E`, `--accent-safe` `#E3A6DA`,
  `--accent-2` `#2EBAC6`, `--line` `#1E2A36`.
- Type: Trebuchet MS display, Segoe UI body, Cascadia Mono for figures and
  micro-labels; no external font request.
- Breakpoints: `1120px` (spine becomes a bottom dock, bands go single-column,
  fold bars appear, `.lt-app` gains 74px bottom padding), `760px` (single-column
  matrices, stacked calculator, wrapped command bar, stacked footer).
- Motion: 240ms `cubic-bezier(.22,1,.36,1)`; orbit animation only inside
  `prefers-reduced-motion: no-preference`.
