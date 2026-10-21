# Reskin inventory — holdavia-website

Generated: 2026-10-21T16:56:43.492Z

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

- Archetype: **document-flow** (editorial)
- Traits: hero, grid, modal, charts, sticky
- Max template depth: 10
- Top-level tags: docspage, div, div, docspage, div, div

The replacement skeleton must not be `document-flow` and must not be in the same family (`editorial`).

## Routes

- `/`

## Palette (most used first)

`#080d14` (32) · `#e3a6da` (12) · `#182533` (10) · `#b6509e` (10) · `#000000` (8) · `#8fa3b5` (6) · `#060a10` (4) · `#090f17` (4) · `#111a24` (4) · `#2ebac6` (4)

## Content lock

- Static visible text tokens: **762**
- Binding expressions: **154**
- Event handlers: **16**
- Contract hash: `9380f95d2cc5b4b04b576ea52f6c4f50d366fd127832c8cc5093e4301f1bbc2d`

Everything in `.reskin/content-contract.json` is immutable: visible copy, placeholders, labels, routes, link targets, asset sources, bindings, handlers, API endpoints and i18n values. A reskin may move these tokens to new markup but may not rewrite, remove or hide them.

## Next

```bash
node scripts/choose-style.mjs --project "E:/workspace/chuangye/solana/lockin/website" --out .reskin
node scripts/verify.mjs baseline --project "E:/workspace/chuangye/solana/lockin/website" --out .reskin
```

Then rewrite the UI and run `verify.mjs check`.
