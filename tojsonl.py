import json

with open("conversation_pairs.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)

with open("conversation_pairs.jsonl", "w", encoding="utf-8") as f:
    for pair in pairs:
        json.dump(pair, f, ensure_ascii=False)
        f.write("\n")