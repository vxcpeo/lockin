# Reskin wireframe — Holdavia

Style: **Paper Protocol** (`ethereum-paper`) · Skeleton: **Gallery Scroll** (`gallery-scroll`)
Original: `document-flow` (editorial), dark navy, magenta accent `#b6509e`.

## New shell

- Root: `div.gx-page` → `main.gx-main` → a sequence of `section.gx-scene` panels, then `footer.gx-foot`.
- Navigation: one fixed **floating dock** (`nav.gx-dock`) pinned to the bottom centre. It carries the
  brand monogram, the five section links and the Docs link. No header, no top bar, no side spine.
- The old shell (`header.lt-command`, `nav.lt-spine-nav`, mobile sheet, `main.lt-main`, `footer.lt-foot`)
  is deleted from the render path.
- Page scroll: panels use `min-height: 100svh` with `scroll-snap-align: start`; related records live in
  horizontal snap rails (`.gx-rail`), not grids.

## Route → layout mapping

| Route | Composition |
|---|---|
| `/` | Opening panel (brand, kicker, h1, lede, actions, seal toggle, telemetry) → 11 scene panels (Rail plates, Time lock steps + signal, Combination workbook, Old locks ledger, Keys gallery wall, Master key matrix, Strongbox fee streams, Workings architecture, Pick-proof ledger, Workshop phases, Spec sheet, Weak points) → closing plate + CTA panel → footer |
| `/#/docs` | Docs masthead (kicker, h1, lede) → horizontal numbered index strip → ruled article blocks on a magazine column → footer |

## Regions and content

| Old region | New region | Notes |
|---|---|---|
| `header.lt-command` (sigil, presence, two actions, burger) | opening panel `.gx-opening` | brand lockup, `Market live`, actions kept as content; burger deleted because the dock replaces the sheet |
| `nav.lt-spine-nav` + footer `lt-foot-nav` | `nav.gx-dock` + footer `nav.gx-foot-nav` | the dock is the second navigation surface, so every nav label still renders twice |
| `section.lt-hero` | `#top.gx-scene.gx-opening` | h1 stays the first heading; seal button keeps `aria-pressed` and its bindings |
| `section.lt-band#rail` | `#rail.gx-scene` | listings become a snap rail of paper plates |
| `section.lt-plate` | `section.gx-plate` | full-bleed framed image with a serif caption |
| `#time-lock` | scene with a two-column steps rail + signal column | steps are a snap rail |
| `#combination` | `.gx-workbook` two-column: dial column + calculator ledger | slider, number inputs, lock buttons, all bindings kept |
| `#old-locks` | scene with a ruled ledger (`details` stays open) | compare table becomes two ruled columns |
| `#keys` | scene: gallery wall (big caption + ticket) + key list + record strip | |
| `#master-key` | scene: 4-up matrix + architecture wire + limits | first copy of the duplicated limits block |
| `#strongbox` | scene: two fee streams + 4 ruled bars | |
| `#workings` | scene: architecture wire + limits | second copy of the duplicated block (multiplicity preserved) |
| `#pick-proof` | scene: numbered ledger inside `details[open]` | |
| `#workshop` | scene: four phase plates + exclusions strip | |
| `#spec-sheet` | scene: decisions grid + measures ledger | |
| `#weak-points` | scene: holds / gives-way ledger + risk notes | |
| `.lt-finale` | closing plate inside the last panel | |
| `#app.lt-cta` | closing scene with the two actions | |
| `footer.lt-foot` | `footer.gx-foot` with the same three columns and legal block | |

## Kept as content-only children

Nothing is kept as an old component: every template is rewritten. The script blocks of `App.vue` and
`Docs.vue` are untouched (same imports, state, computeds, handlers). `main.js` changes only its
stylesheet import.

## New token file and breakpoints

- `src/styles/paper.css` — tokens, reset, typography, scene grammar, rails, docks, article blocks,
  responsive rules and reduced-motion guards. It replaces `src/styles/abyss.css` (removed from the
  render path; deleted after backup in `.reskin/original-src/`).
- Namespace: every class is `gx-*`; no `lt-*` selector survives.
- Breakpoints: `720px` (dock compresses, workbook stacks), `1080px` (scenes switch to the 12-column
  editorial grid, rails show two cards at once). Designed at 390px first.

## Risks

- Full-height panels can push copy below the fold; every panel is `min-height`, never fixed height, so
  nothing is clipped and a hairline + downward rule marks each continuation.
- Horizontal rails need keyboard access: the listings rail keeps `tabindex="0"` and the step rail is a
  scroll region with visible snap points.
- The dock must stay reachable and visible at 390px without overlap; it is a single pill with a
  horizontal scroll fallback and 44px targets.
