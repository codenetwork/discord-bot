
def is_admin(guild, member):
    for role in member.roles:
        if guild.roles[role].name == 'Admins':
            return True
    return False
