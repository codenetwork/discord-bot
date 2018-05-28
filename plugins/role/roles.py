import os
from typing import Optional, List

import jsonpickle

from disco.bot import Plugin
from disco.bot.command import CommandEvent
from disco.types import Guild

from plugins.util.config_util import get_file_path
from plugins.util.permission_util import admin_only, has_discord_role

from .role import Role


class RolePlugin(Plugin):
    # TODO Maybe add some lookup maps or something idk.
    roles: List[Role] = list()

    def load(self, ctx):
        if os.path.isfile(get_file_path('roles.json')):
            with open(get_file_path('roles.json'), 'r+') as f:
                self.roles = jsonpickle.decode(f.read(), keys=True)

    def save_roles(self):
        with open(get_file_path('roles.json'), 'w+') as f:
            f.write(jsonpickle.encode(self.roles, keys=True))

    def get_by_name(self, name: str, ignore_restricted: bool = True) -> Optional[Role]:
        for role in self.roles:
            if ignore_restricted and role.restricted:
                continue
            if name == role.role_name:
                return role
        return None

    def get_by_alias(self, alias: str, ignore_restricted: bool = True) -> Optional[Role]:
        for role in self.roles:
            if ignore_restricted and role.restricted:
                continue
            if alias in role.aliases:
                return role
        return None

    @classmethod
    def get_discord_role_by_name(cls, guild: Guild, name):
        for role in guild.roles.values():
            if role.name == name:
                return role
        return None

    @Plugin.command('create', '<role_name:str> <role_alias:str>', group='role')
    @admin_only()
    def command_role_create(
            self, event: CommandEvent, role_name: str, role_alias: str
    ):
        if role_name in {role.role_name for role in self.roles}:
            event.msg.reply('That role already exists!')
            return
        self.roles.append(Role(
            role_name=role_name,
            aliases=[role_alias]
        ))
        self.save_roles()
        event.msg.reply('Adding a role named {} with alias {}'.format(
            role_name, role_alias
        ))

    @Plugin.command('parent', '<role_name:str>, [parent:str]', group='role')
    @admin_only()
    def command_set_parent(self, event: CommandEvent, role_name, parent=None):
        role = self.get_by_name(role_name)
        if role is None:
            event.msg.reply('Unknown role!')
            return
        parent_role = self.get_by_name(parent)
        if parent_role is None:
            event.msg.reply('Removing parent of role {}'.format(role_name))
            role.parent = None
            self.save_roles()
            return
        role.parent = parent_role.role_name
        self.save_roles()
        event.msg.reply('Set parent of role {} to {}'.format(role_name, parent))

    @Plugin.command('add', '<role_name:str>', group='role')
    def command_role_add(self, event: CommandEvent, role_name):
        roles = role_name.split(",")
        for role in roles:
            role = self.get_by_alias(role)
            if role is None:
                event.msg.reply('Unknown role!')
                continue
            discord_role = self.get_discord_role_by_name(
                event.guild, role.role_name
            )
            if discord_role is None:
                event.msg.reply('Missing discord role!')
                continue
            if role.parent is not None:
                if not has_discord_role(event.member, self.get_discord_role_by_name(event.guild, role.parent)):
                    if self.get_discord_role_by_name(event.guild, role.parent) is not None:
                        event.msg.reply('You aren\'t in the parent role `{}` so I just added it for you. I also added you to `{}` like you asked.'.format(role.parent, role.role_name))
                        event.member.add_role(self.get_discord_role_by_name(event.guild, role.parent))
                        event.member.add_role(discord_role)
                        continue
                    else:
                        event.msg.reply('The parent role {} doesn\'t exist so I couldn\'t automatically add it for you. Ask in <#417555071551668225> if you\'re having problems.'.format(role.parent))
                        continue
            if has_discord_role(event.member, discord_role):
                event.msg.reply('You already have this role!')
                continue
            event.member.add_role(discord_role)
            event.msg.reply('You\'ve been given the {} role!'.format(role.role_name))

    @Plugin.command('remove', '<role_name:str>', group='role')
    def command_role_remove(self, event: CommandEvent, role_name):
        roles = role_name.split(",")
        for role in roles:
            role = self.get_by_alias(role)
            if role is None:
                event.msg.reply('Unknown role!')
                continue
            discord_role = self.get_discord_role_by_name(
                event.guild, role.role_name
            )
            if discord_role is None:
                event.msg.reply('Missing role definition!')
                continue
            if not has_discord_role(event.member, discord_role):
                event.msg.reply('You don\'t have this role!')
                continue
            for other_role in self.roles:
                if other_role.parent == role.role_name:
                    event.member.remove_role(self.get_discord_role_by_name(event.guild, other_role.role_name))
                    event.msg.reply('You\'ve lost the {} role!'.format(other_role.role_name))
            event.member.remove_role(discord_role)
            event.msg.reply('You\'ve lost the {} role!'.format(role.role_name))

    @Plugin.command('list', group='role')
    def command_role_list(self, event: CommandEvent):
        role_descriptions = []
        role_descriptions.append('**Available Roles**\n\n')
        current_description = 0

        role_dict = dict()
        ordered_names = list()
        for role in self.roles:
            if not role.restricted:
                role_name = role.role_name
                if role.parent:
                    role_name = role.parent + "/" + role_name
                role_dict[role_name] = role
                ordered_names.append(role_name)
        for role_name in sorted(ordered_names):
            role = role_dict[role_name]
            if len(role_descriptions[current_description]) + len(role_name) > 1800:
                current_description += 1
                role_descriptions.append("")

            role_descriptions[current_description] += '* Role `{}` with aliases: `{}`\n'.format(
                role_name, ', '.join(role.aliases)
            )

        for message in role_descriptions:
            event.msg.reply(message)

        event.msg.reply('\n\nTo give yourself a new role use `!role add qut` or add multiple like `!role add qut,hardware,python,javascript`. (note the lack of spaces between roles)')

    @Plugin.command('role')
    def command_role_help(self, event: CommandEvent):
        event.msg.reply('Beep Boop hi from the bot 🤖. To see what roles are available type `!role list`, to add roles you can use `!role add qut` or `!role add qut,python,hackathons,java`')

