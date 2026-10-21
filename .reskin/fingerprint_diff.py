import json
import pathlib
from collections import Counter

base = json.loads(pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website\.reskin\baseline\pages.json").read_text(encoding="utf-8"))
cur = json.loads(pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website\.reskin\current\pages.json").read_text(encoding="utf-8"))
b = set(base["pages"]["/"]["desktop"]["fingerprint"])
c = set(cur["pages"]["/"]["desktop"]["fingerprint"])
inter = b & c
print("base", len(b), "cur", len(c), "inter", len(inter), "union", len(b | c), "jaccard", round(len(inter) / len(b | c), 3))
print("\nshared entries:")
for item in sorted(inter):
    print("  ", item)
print("\nonly current:")
for item in sorted(c - b):
    print("  ", item)
