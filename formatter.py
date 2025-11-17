import re
import emoji

#needs to
#mark that a new line has been found when it reaches the pattern of
# Date, Time - Username
# Remove the date and time DONE
# match usernames to names (e.g. TobÉ -> Toby) DONE
# replace emojis with emoticons

emoji_pattern = re.compile(
    "[" 
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Symbols & pictographs
    "\U0001F680-\U0001F6FF"  # Transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
    "\U00002700-\U000027BF"  # Dingbats
    "\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
    "\U00002600-\U000026FF"  # Misc symbols
    "\U00002B00-\U00002BFF"  # Arrows
    "]+",
    flags=re.UNICODE
)

emojiCollection = set()

pattern = r"(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.*)"

merged = []
last_name, buffer = None, []

with open("ROthechat.txt", "r", encoding="utf-8") as file:
    while line := file.readline():
        emojis = emoji_pattern.findall(line)
        line = emoji.demojize(line)

        for emoticon in emojis:
            emojiCollection.add(emoticon)

        match = re.match(pattern, line)
        if not match:
            continue
        name, message = match[2], match[3]

        match name:
            case "TobÉ":
                name = "Toby"
            case "Stoned Messenger":
                name = "Gabe"
            case "Anime Girl":
                name = "Abbie"
            case "PøoBoO🍑":
                name = "Finn"
            case "PK Piano":
                name = "Pish"
            case "Bus?":
                name = "Joseph"
            case "Dandelion Yům":
                name = "Deven"
            case "Daniel Bookes":
                name = "Daniel Brookes"
            case "Possibly Penis":
                name = "Bea"
            case "Lōng":
                name = "Harry"
            case "Math Guy":
                name = "Stevie"
            case "Louis Miles":
                name = "Louis Miles"
            case "+44 7941 089692":
                name = "IDFKKKK"
            case _:
                print("No real name for " + name)
                break
        
        if name == last_name:
            buffer.append(message)
        else:
            if buffer:
                merged.append(f"{last_name}: {' '.join(buffer)}")
            buffer = [message]
            last_name = name
        
    

# Add the last one
if buffer:
    merged.append(f"{last_name}: {' '.join(buffer)}")

with open("formattedchat.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(merged))

print("\n".join(merged))
#print(emojiCollection)
