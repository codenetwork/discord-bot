# Code Network Discord Bot
This is the code that runs our official Code Network Discord bot. PRs welcome (see below).

# License
Everything in this repo is released under the MIT license. By submitting any code you agree
to license it under the MIT license too.

# How to contribute
Our bot is written in python and we've made it easy to make additions. To make it easier 
when developing your bot we highly recommend you make a test discord guild. This way you 
can test your bot before you make a pull request. You can suggest new features in the 
`#suggestions` or `#bot` channels in our discord. If you want to add a new feature,
you should read this entire page. After that you can make a pull request with any
changes.

### Make a test discord server
First off, make a new discord server (also referred to as a Guild). You can do this
from within discord once you're logged in. Click the "+" button on the left side of 
the screen below all the current Guilds you've joined.

### Create your test bot
You'll have to make a new discord app, create a bot user then add it to your test guild.
[Click Here](https://discordapp.com/developers/applications/me) to make a new discord app.
Name it something like "Joe's Test Guild" and fill in the mandatory fields. Once you've
made a new app, scroll down to the bot user section. Make a new bot user. Make note of the
token and paste it into the config.json file where it says "MY_BOT_TOKEN_HERE".

### Add your bot to your test guild
From just above the bot user section, click the "OAuth2 URL Generator" button. Select the
"bot" scope and "Administrator" from the permissions section. Copy the URL then open it in
a new window. Select your test guild from the dropdown menu and hit "Authorize". The bot
has now been added to your guild but is not currently running.

### Run your test bot
Because the bot opens a websocket to the discord API, it will run from almost anywhere.
You don't need to setup any webhooks or public endpoints. From the root of this GitHub
repo just run `python3 -m disco.cli --config config.json` to start the bot.

### Test your bot
From within your test guild you should be able to test your bot now. All bot commands 
start with "!". The command `!test` should work out of the box. Bear in mind some
of the bot's functionality (like `!role give blah`) is dependant on the guild configuration
and won't work unless your test guild is setup the same as the official Code Network one.
Feel free to post in the `#bot` channel on the official guild if you need any help.

### Adding new functionality and testing your bot
It's best to only add functionality that is actually useful. Pull requests that don't add
anything useful or that are buggy probably won't be accepted. Make sure you thoroughly 
test your bot first. Feel free to invite people to your test guild if you need help 
testing.