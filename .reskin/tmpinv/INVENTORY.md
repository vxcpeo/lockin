# Reskin inventory — holdavia-website

Generated: 2026-10-21T17:07:49.064Z

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
- Traits: sidebar, topbar, cards, hero, table, grid, modal, charts, sticky, gallery
- Max template depth: 10
- Top-level tags: docspage, div, div, docspage, div, div

The replacement skeleton must not be `dashboard-shell` and must not be in the same family (`shell`).

## Routes

- `/`

## Palette (most used first)

`#080d14` (16) · `#34322d` (10) · `#e3a6da` (6) · `#ffffff` (6) · `#182533` (5) · `#b6509e` (5) · `#000000` (4) · `#2c2a26` (4) · `#8fa3b5` (3) · `#ede9df` (3)

## Content lock

- Static visible text tokens: **763**
- Binding expressions: **154**
- Event handlers: **16**
- Contract hash: `135b9c65f301b4c5c9be25d009f34a4a9d246a9640a2b46b079221a4c041e1c5`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/lockin/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/lockin/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
