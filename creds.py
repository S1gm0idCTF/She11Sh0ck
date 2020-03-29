import json

with open("creds.json") as f:
	creds = json.load(f)

def getcreds():
	return creds

def getDiscordAPIKeys():
	return creds["discord_bot_token"]
