# Reskin verification — PASS

Generated: 2026-10-20T16:37:17.594Z

- Project: **latchera-website**
- URL: http://127.0.0.1:4317/
- Original skeleton: `dashboard-shell` (shell)
- New skeleton: `document-flow` (editorial)
- Accent: #8b5cf6 -> #b6509e (47.87 ΔE; min 30)
- Source contract: intact (`aa39f627cace`)

| Route | Result | DOM similarity | Landmark similarity | Axe serious | Screenshot |
|---|---|---:|---:|---:|---|
| `/` | PASS | 0.314 | 0.571 | 0 | [desktop](current/home-desktop.png) |

## Blocking issues

- None.

## Warnings

- /: aria attribute added: aria-label=Hardware
- /: aria attribute added: aria-label=Paperwork

## Thresholds

- DOM fingerprint similarity <= 0.5
- Landmark sequence similarity <= 0.68
- CSS class overlap <= 0.1
- Accent distance >= 30 ΔE
- Contrast failures <= 0
- Axe serious/critical <= 0

All content is compared as a multiset of visible words plus rendered attribute values. Reordering is allowed, rewriting/removing/adding visible copy is not. Dynamic numeric values are reported as warnings, never silently accepted.
