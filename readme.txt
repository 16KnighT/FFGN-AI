Little project by Toby Knight to use LoRa to tune a model using exported whatsapp chats

formatter.py - takes a whatsapp chat removes time and allows you to replace user's names with something else (accounts for if it's just a phone number)
gpuchecker.py - just to help me check if PyTorch found my GPU
individualjson.py - creates a JSON file for every user of their prompts and responses
fullchatjson.py - creates a JSON file which splits every message into the user and their message
lorafinetune.py - trains a model on the chat
pairsjson.py - creates a JSON file made up of pairs of what someone messaged and the response to that message
tojsonl.py - converts .json file to .jsonl file