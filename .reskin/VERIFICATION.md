# Reskin verification — PASS

Generated: 2026-10-21T17:27:06.471Z

- Project: **holdavia-website**
- URL: http://127.0.0.1:4318/
- Original skeleton: `document-flow` (editorial)
- New skeleton: `gallery-scroll` (spatial)
- Accent: #b6509e -> #0c5681 (57.72 ΔE; min 30)
- Source contract: intact (`2aff2e61c4f3`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.289 | 0.571 | 0 | [desktop](current/home-desktop.png) |

## Blocking issues

- None.

## Warnings

- attributes: "href=#top" count increased 12 -> 14
- links: "href:#top" count increased 12 -> 14
- /: aria attribute changed/removed: aria-label=Paperwork
- /: aria attribute added: aria-label=Holdavia home
- /: aria attribute added: aria-label=Open the section list
- /: link target added: #top

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
