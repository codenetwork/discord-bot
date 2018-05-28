from disco.bot import Plugin
from disco.bot.command import CommandEvent
from disco.types.message import MessageEmbed
embed = MessageEmbed()  # Create a discord embed object and set default name/icon
embed.set_author(name='Code Network', icon_url='https://codenetwork.co/wp-content/uploads/2018/05/cn-logo-dark-square.png')
embed.url = 'https://codenetwork.co/rules'

class Bot(Plugin):
    def get_welcome_embed(self):
        embed.description = 'Welcome to the official Code Network Discord. To get started, here are some handy links.'
        embed.description += 'We recommend you read through all of them so you get a better understanding of the '
        embed.description += 'community expectations. However, we\'ve also provided a tldr; of each one below.'

        embed.add_field(name='General Rules', value='https://codenetwork.co/rules', inline=True)
        embed.add_field(name='Code of Conduct', value='https://codenetwork.co/coc', inline=True)
        embed.add_field(name='Safe Space Policy', value='https://codenetwork.co/ssp', inline=True)
        embed.add_field(name='Main Website', value='https://codenetwork.co', inline=True)

        embed.add_field(name='General Rules tldr;', value='If you’re a recruiter, your job post doesn’t belong in our community. If you’re a technical looking to fill a paid role feel free to advertise it, but include detailed info about the role. No advertising or self promotion - share stuff you’ve built to start conversations, not conversions. Always follow our Code of Conduct and Safe Space Policy.', inline=False)
        embed.add_field(name='Code of Conduct (CoC) tldr;', value='Always be considerate, respectful and treat others how you’d want to be treated. Never start/continue flame wars or trolling and don’t make anyone feel uncomfortable or unwelcome. Always be collaborative, stay honest and don’t misrepresent the group or executive. Above all, never discriminate against or harass someone.', inline=False)
        embed.add_field(name='Safe Space Policy (SSP) tldr;', value='Abuse, discrimination, harassment, assault, sexism, racism, ableism, religious persecution or homophobic behaviour of any kind is not tolerated in the Code Network community. This include events, discussions and online communications. Any other behavior which would reasonably make a person feel trivialised or otherwise discriminated against is also prohibited. If you violate this policy you could be asked to leave our community either temporarily or permanently.', inline=False)

        return embed

    @Plugin.command('bot')
    def command_test(self, event: CommandEvent):
        event.msg.reply('Beep Boop. The bot 🤖 is responsive.')

    @Plugin.command('help')
    @Plugin.command('usage')
    def command_test(self, event: CommandEvent):
        event.msg.reply('Beep Boop hello from the bot! 🤖 To get started read everything in the <#413628419226468352> channel.')
        event.msg.reply('**Bot Usage**: \n Here is a list of all the commands we currently support:\n`!help` - this message.\n`!bot` - checks if the bot is responsive.\n`!invite` get the invite link to this server.\n`!coc` - link to our Code of Conduct.\n`!ssp` - link to our Safe Space Policy.\n`!welcome` - prints the welcome info again. (you should get it in a PM)\n`!role list` - show a list of roles currently available.\n`!role add qut` or `!role add qut,python,hardware` add a role to yourself so you can see role specific channels.\n`!parking qut` shows current parking state at location you specify.')

    @Plugin.command('invite')
    def command_invite(self, event: CommandEvent):
        event.msg.reply('Beep Boop. 🤖 here is your invite link: https://codenetwork.co/discord')

    @Plugin.command('coc')
    def command_invite(self, event: CommandEvent):
        event.msg.reply('Beep Boop. 🤖 here is a link to our Code of Conduct: https://codenetwork.co/coc')

    @Plugin.command('ssp')
    def command_invite(self, event: CommandEvent):
        event.msg.reply('Beep Boop. 🤖 here is a link to our Safe Space Policy: https://codenetwork.co/ssp')

    @Plugin.command('welcome')
    def command_welcome(self, event: CommandEvent):
        event.msg.reply('In case you missed it, here is some welcome info.', embed=self.get_welcome_embed())

    @Plugin.listen('GuildMemberAdd')
    def send_welcome_pm(self, event):
        event.member.user.open_dm().send_message('Hi there! Welcome to our friendly community. To get started, read through all the info in the <#413628419226468352> channel and everything below. If you have any questions, ask in <#349872637645684737>.',
                                                 embed=self.get_welcome_embed())
