"""Each location should have it's own python file with a function called "get_parking_place". The "get_parking_place"
function should return an embed object with all the necessary parking information. Look at the QUT one as an example
of how to format the response. All responses should look the same! Each location should have a logo/picture so it can
be easily identified. If you need to use any libraries that aren't already in the main requirements.txt, don't forget
to add them there.
"""

from disco.bot import Plugin
from disco.bot.command import CommandEvent

# Import all of our location specific functions here
from .qut import get_parking_qut


class Parking(Plugin):
    @Plugin.command('parking', '[place:str...]')
    def command_info(self, event: CommandEvent, place = None):
        """Main parking bot method."""
        if place is None:
            message = '**Usage:**\n'
            message += 'List parking info for a place: `!parking <name>` Example: `!parking qut`'
            event.msg.reply(message)
        else:
            # Check which location was entered and reply with the correct parking information
            if place in ["qut", "QUT"]:
                event.msg.reply("Here you go.", embed=get_parking_qut())

            else:  # Default catch all for locations that haven't been implemented
                event.msg.reply('Sorry, {} hasn\'t been implemented yet. Look here if you want to have a go at '
                                'doing it yourself: https://github.com/codenetwork/discord-bot#how-to-contribute'
                                ''.format(place))

    @Plugin.command('parking', '<place:str>')
    def command_parking_list(self, event, place):
        """Replies with location specific parking information"""
        
