import json
import pathlib

p = pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website\.reskin\baseline\pages.json")
data = json.loads(p.read_text(encoding="utf-8"))
page = data["pages"]["/"]
words = page["desktop"]["words"]
counts = {item["word"]: item["count"] for item in words}
out = pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website\.reskin\baseline-words.txt")
lines = [f"{count:3d}  {word}" for word, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
out.write_text("\n".join(lines), encoding="utf-8")
print("unique words:", len(counts), "total:", sum(counts.values()))
for key in ["Holdavia", "Rail", "Time", "lock", "Docs", "Read", "the", "docs", "Hardware", "Paperwork", "Workings", "Spec", "Weak", "Market", "live"]:
    print(f"{key!r}: {counts.get(key)}")
