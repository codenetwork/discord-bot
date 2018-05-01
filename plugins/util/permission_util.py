from functools import wraps

from disco.bot.command import CommandEvent


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


def is_admin(guild, member):
    for role in member.roles:
        if guild.roles[role].name == 'Admins':
            return True
    return False
