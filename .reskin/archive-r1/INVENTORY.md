# Reskin inventory — latchera-website

Generated: 2026-10-20T16:01:33.142Z

## Project

| Field | Value |
|---|---|
| Root | `E:/workspace/chuangye/solana/lockin/website` |
| Vue | ^3.5.13 |
| Package manager | npm |
| Nuxt | no |
| CSS frameworks | none detected |
| Files scanned | 7 (4 SFCs) |

## Original skeleton

- Archetype: **dashboard-shell** (shell)
- Traits: sidebar, topbar, cards, hero, grid, modal, charts, sticky
- Max template depth: 10
- Top-level tags: docspage, template, div, docspage, template, div

The replacement skeleton must not be `dashboard-shell` and must not be in the same family (`shell`).

## Routes

- `/`

## Palette (most used first)

`#686271` (40) · `#d6d0c7` (30) · `#d8d0c7` (20) · `#111016` (12) · `#faf7f1` (12) · `#ffffff` (10) · `#716a78` (8) · `#8a8290` (8) · `#8b5cf6` (8) · `#ded7cf` (8)

## Content lock

- Static visible text tokens: **764**
- Binding expressions: **154**
- Event handlers: **16**
- Contract hash: `2b2c360e987666c7549dc174f9c5c51d1896fc2169b9db9fc0ef3056ececea40`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/lockin/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/lockin/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
