import json
import pathlib
from collections import Counter

p = pathlib.Path(r"E:\workspace\chuangye\solana\lockin\website\.reskin\content-contract.json")
d = json.loads(p.read_text(encoding="utf-8"))
print("keys:", list(d.keys()))
for key, value in d.items():
    if isinstance(value, list):
        print(f"{key}: {len(value)} items")
    elif isinstance(value, dict):
        print(f"{key}: dict keys {list(value.keys())[:8]}")
    else:
        print(f"{key}: {value!r}"[:200])

visible = d.get("visibleText") or []
print("\nvisible text sample:", visible[:6])
if visible and isinstance(visible[0], dict):
    counts = Counter(item.get("value") for item in visible)
else:
    counts = Counter(visible)
print("total visible occurrences:", sum(counts.values()), "unique:", len(counts))
multi = [(v, c) for v, c in counts.items() if c > 1]
multi.sort(key=lambda x: -x[1])
print("\nrepeated tokens (top 40):")
for value, count in multi[:40]:
    print(f"  {count:3d}  {str(value)[:100]}")

print("\nbindings sample:", json.dumps((d.get("bindings") or [])[:8], ensure_ascii=False, indent=1)[:1200])
print("\nattributes sample:", json.dumps((d.get("attributes") or [])[:12], ensure_ascii=False, indent=1)[:1200])
print("\nevents:", json.dumps(d.get("events"), ensure_ascii=False)[:800])
print("\nforms:", json.dumps(d.get("forms"), ensure_ascii=False)[:800])
print("\nassets:", json.dumps(d.get("assets"), ensure_ascii=False)[:600])
