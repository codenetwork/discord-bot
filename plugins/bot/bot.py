from disco.bot import Plugin
from disco.bot.command import CommandEvent


class Bot(Plugin):
    @Plugin.command('bot')
    def command_test(self, event: CommandEvent):
        event.msg.reply('Bot module responsive')
