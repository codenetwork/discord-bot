import os
from typing import List, Optional

import jsonpickle

from disco.bot import Plugin
from disco.bot.command import CommandEvent

from plugins.util.config_util import get_file_path

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

    def get_by_alias(self, alias: str, ignore_restricted: bool=True) -> Optional[Role]:
        for role in self.roles:
            if ignore_restricted and role.restricted:
                continue
            if alias in role.aliases:
                return role
        return None

    @classmethod
    def get_discord_role_by_name(cls, guild, name):
        for role in guild.roles.values():
            if role.name == name:
                return role
        return None

    @Plugin.command('add', '<role_name:str> <role_alias:str>', group='role')
    def command_role_add(
            self, event: CommandEvent, role_name: str, role_alias: str
    ):
        if role_name in self.roles:
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

    @Plugin.command('give', '<role_name:str>', group='role')
    def command_role_give(self, event: CommandEvent, role_name):
        role = self.get_by_alias(role_name)
        if role is None:
            event.msg.reply('Unknown role!')
            return
        discord_role = self.get_discord_role_by_name(
            event.guild, role.role_name
        )
        if discord_role is None:
            event.msg.reply('Missing role definition!')
            return
        if discord_role.id in event.member.roles:
            event.msg.reply('You already have this role!')
            return
        event.member.add_role(discord_role)
        event.msg.reply('You\'ve been given the {} role!'.format(role.role_name))

    @Plugin.command('take', '<role_name:str>', group='role')
    def command_role_take(self, event: CommandEvent, role_name):
        role = self.get_by_alias(role_name)
        if role is None:
            event.msg.reply('Unknown role!')
            return
        discord_role = self.get_discord_role_by_name(
            event.guild, role.role_name
        )
        if discord_role is None:
            event.msg.reply('Missing role definition!')
            return
        if discord_role.id not in event.member.roles:
            event.msg.reply('You don\'t have this role!')
            return
        event.member.remove_role(discord_role)
        event.msg.reply('You\'ve lost the {} role!'.format(role.role_name))

    @Plugin.command('list', group='role')
    def command_role_list(self, event: CommandEvent):
        role_description = '**Available Roles**\n\n'
        for role in self.roles:
            if not role.restricted:
                role_description += '* Role `{}` with aliases: `{}`\n'.format(
                    role.role_name, ', '.join(role.aliases)
                )
        event.msg.reply(role_description)
