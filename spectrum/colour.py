import discord
import asyncio

import argparse
import re
import math

from discord.ext import commands
import platform


def all_valid_colours():
    dict = discord.Colour.__dict__
    return [key for key, val in dict.items() if type(val) == classmethod]

valid_colours = ', '.join(all_valid_colours())


class Colour():

    def __init__(self, client):
        self.client = client

    @commands.command(
        pass_context=True,
        help='Set role to a named colour or a 6-digit hex value\n\n'
        'Valid colour values are:\n\n'
        f'{valid_colours}',
    )
    async def set(self, ctx, role_name: str, colour_input: str):
        """Sets a role to the specific colour"""

        author_roles = ctx.message.author.roles
        server = ctx.message.server

        try:
            role = self.role_available(role_name, author_roles)
            if colour_input[0] == '#':
                colour = self.colour_from_hex(colour_input)
            else:
                colour = self.colour_by_name(colour_input)
        except (AttributeError, ValueError) as e:
            await self.client.say(str(e) + f'\nSee `@{self.client.user.name} help set` for details.')
            return

        await self.client.edit_role(server, role, colour=colour)
        await self.client.say("lookin' good, good lookin'")

    @commands.command(help='Brighten your day with a rainbow')
    async def rainbow(self):
        return await self.client.say(':rainbow:')  # disabled until further notice

    def role_available(self, role_name, role_list):
        '''Attempt to get a role matching role_name, case insensitive'''
        for role in role_list:
            if role_name.lower() == role.name.lower():
                return role

        raise ValueError(f"You don't have the `{role_name}` role so I can't help, sorry")

    def rgb_to_hex(self, rgb):
        rgb = tuple(x for x in map(round, rgb))
        return '#%02x%02x%02x' % rgb

    @staticmethod
    def colour_by_name(name):
        try:
            colour = getattr(discord.Colour, name)
            return colour()
        except AttributeError:
            raise ValueError(f'The colour `{name}` was not found.')

    def colour_from_hex(self, code):
        if not re.match(r'#[\da-fA-F]{6}$', code):
            raise ValueError('`%s` is not a valid hex colour value' % code)

        # convert hex colour code to decimal value
        value = int(code[1:], 16)
        return discord.Colour(value)


def setup(client):
    client.add_cog(Colour(client))
