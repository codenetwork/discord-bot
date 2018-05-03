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
        if role.parent is not None:
            if not has_discord_role(event.member, self.get_discord_role_by_name(event.guild, role.parent)):
                event.msg.reply('You aren\'t in the parent role `{}`!'.format(role.parent))
                return
        if has_discord_role(event.member, discord_role):
            event.msg.reply('You already have this role!')
            return
        event.member.add_role(discord_role)
        event.msg.reply('You\'ve been given the {} role!'.format(role.role_name))

    @Plugin.command('remove', '<role_name:str>', group='role')
    def command_role_remove(self, event: CommandEvent, role_name):
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
        if not has_discord_role(event.member, discord_role):
            event.msg.reply('You don\'t have this role!')
            return
        for other_role in self.roles:
            if other_role.parent == role.role_name:
                event.member.remove_role(self.get_discord_role_by_name(event.guild, other_role.role_name))
                event.msg.reply('You\'ve lost the {} role!'.format(other_role.role_name))
        event.member.remove_role(discord_role)
        event.msg.reply('You\'ve lost the {} role!'.format(role.role_name))

    @Plugin.command('list', group='role')
    def command_role_list(self, event: CommandEvent):
        role_description = '**Available Roles**\n\n'
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
            role_description += '* Role `{}` with aliases: `{}`\n'.format(
                role_name, ', '.join(role.aliases)
            )
        role_description += '\n\nTo give yourself a new role use `!role add <group alias>`'
        event.msg.reply(role_description)
