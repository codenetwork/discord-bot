from disco.bot import Plugin
from disco.bot.command import CommandEvent


class TestPlugin(Plugin):
    @Plugin.command('test')
    def command_test(self, event: CommandEvent):
        event.msg.reply('Test Success - Bot is responsive')
