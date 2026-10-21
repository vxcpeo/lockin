"""Splice the new reskin templates into the Vue SFCs and switch the stylesheet.

Only the <template> block of each SFC is replaced; the <script setup> block is
copied byte-for-byte. main.js changes one import line.
"""

import pathlib
import shutil

ROOT = pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website")
RESKIN = ROOT / ".reskin"
BUILD = RESKIN / "build"
ORIGINAL = RESKIN / "original-src"
ORIGINAL.mkdir(parents=True, exist_ok=True)

for rel in ("src/App.vue", "src/Docs.vue", "src/main.js", "index.html", "src/styles/abyss.css"):
    src = ROOT / rel
    dst = ORIGINAL / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)
        print("backed up", rel)


def splice(vue_rel: str, template_rel: str) -> None:
    vue_path = ROOT / vue_rel
    text = vue_path.read_text(encoding="utf-8")
    index = text.find("<template>")
    if index < 0:
        raise SystemExit(f"no <template> in {vue_rel}")
    head = text[:index]
    new_template = (BUILD / template_rel).read_text(encoding="utf-8").rstrip() + "\n"
    vue_path.write_text(head + new_template, encoding="utf-8")
    print(f"{vue_rel}: kept {head.count(chr(10)) + 1} script lines, wrote new template")


splice("src/App.vue", "app-template.vue")
splice("src/Docs.vue", "docs-template.vue")

main_js = ROOT / "src/main.js"
main_js.write_text(
    "import { createApp } from 'vue'\n"
    "import App from './App.vue'\n"
    "import './styles/paper.css'\n\n"
    "createApp(App).mount('#app')\n",
    encoding="utf-8",
)
print("main.js -> paper.css")

index_html = ROOT / "index.html"
html = index_html.read_text(encoding="utf-8")
html = html.replace('content="#080d14"', 'content="#ffffff"')
index_html.write_text(html, encoding="utf-8")
print("index.html theme-color -> #ffffff")

abyss = ROOT / "src/styles/abyss.css"
if abyss.exists():
    abyss.unlink()
    print("removed src/styles/abyss.css (backup in .reskin/original-src)")
