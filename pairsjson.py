import json

pairs = []
previous_speaker = None
previous_message = None

with open("chat.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    for entry in data:
        if previous_speaker and previous_speaker != entry["speaker"]:
            pairs.append({
                "prompt": f"{previous_speaker}: {previous_message}",
                "response": f"{entry['speaker']}: {entry['message']}"
            })
        previous_speaker = entry["speaker"]
        previous_message = entry["message"]

with open("conversation_pairs.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, ensure_ascii=False, indent=2)