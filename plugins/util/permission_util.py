from functools import wraps

from disco.bot.command import CommandEvent
from disco.types import GuildMember, Role as DiscordRole, Guild


def admin_only():
    def decorator(func):
        @wraps(func)
        def wrapper(self, event: CommandEvent, *args, **kwargs):
            if not is_admin(event.guild, event.member):
                event.msg.reply('Insufficient Permissions!')
            else:
                return func(self, event, *args, **kwargs)
        return wrapper
    return decorator


def is_admin(guild: Guild, member: GuildMember):
    for role in member.roles:
        if guild.roles[role].name == 'Admins':
            return True
    return False


def has_discord_role(member: GuildMember, discord_role: DiscordRole):
    if discord_role is None:
        return False
    else:
        return discord_role.id in member.roles
