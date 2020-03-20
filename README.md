# She11Sh0ck
A Bot to manage discord servers for CTF Competitions

# Basic Initialization
This is a development build and not designed for personal use (yet) so in order to make this work you must supply your own `keys.txt` file and `server_config.json` file.

<u>Keys</u>
The `keys.txt` file must have your bot token on the first line. If one does not exist, it will ask for your token

<u>Server config</u>
This file is for storing data if the bot is active on multiple servers. It muse be called `server_config.json` and contain a single pair of curly brackets `{}`. It will fill up automatically with use.

# Important Notes
The bot will break if the json is desynced from the discord server. While we are looking to fix this in the future, if you delete a channel in the discord, please ensure that it is also deleted from `server_config.json`. 

This bot is a development build and may break. We are not responsible for damage to your discord server or data lost when using this build of the bot.
