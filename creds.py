import json

with open("creds.json") as f:
	creds = json.load(f)

def getdb():
	return creds

def getDiscordAPIKeys():
	return creds["discord_bot_token"]
