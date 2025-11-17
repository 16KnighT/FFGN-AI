from collections import defaultdict
import re
import json

messages_by_user = defaultdict(list)

with open("formattedchat.txt", "r", encoding="utf-8") as f:
    for line in f:
        match = re.match(r"([^:]+): (.*)", line.strip())
        if match:
            speaker, message = match.groups()
            messages_by_user[speaker.strip()].append(message.strip())

# Save each user's messages in a separate file
for speaker, messages in messages_by_user.items():
    filename = f"{speaker}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
