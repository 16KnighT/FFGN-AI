import json
import re

data = []
with open("formattedchat.txt", "r", encoding="utf-8") as f:
    for line in f:
        match = re.match(r"([^:]+): (.*)", line.strip())
        if match:
            speaker, message = match.groups()
            data.append({"speaker": speaker.strip(), "message": message.strip()})

# Save the full chat as JSON
with open("chat.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)