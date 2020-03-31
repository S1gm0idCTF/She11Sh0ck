 ![She11Sh0ck](/assets/logo.png)
# She11Sh0ck 
A Bot to manage discord servers for CTF Competitions

# Basic Initialization
This is a development build and not designed for personal use (yet) so in order to make this work you must supply your own `creds.json` file and mySQL server.

<u>Keys</u>
The `creds.json` file must look like this
```json
{
  "host": "<phpMyAdmin IP>", #string
  "port": <phpMyAdmin port>, #int
  "user": "<phpMyAdmin user>", #string
  "password": "<phpMyAdmin password>", #string
  "db": "<database name>", #string
  "discord_bot_token": "<discord bot token>" #string
}
```
You can also throw whatever else in there, I guess, but at least that :P

# Important Notes
The bot will break if the mySQL database is desynced from the discord server. While we are looking to fix this in the future with an integrity checker of some sort, if you delete a channel in the discord, please ensure that it is also deleted from your phpMyAdmin server. 

This bot is a development build and may break. We are not responsible for damage to your discord server or data lost when using this build of the bot.
