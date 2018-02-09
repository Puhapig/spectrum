import discord
import asyncio

import argparse
import re

from discord.ext import commands
import platform


client = commands.Bot(description='Changes role colour on command', command_prefix=commands.when_mentioned_or('!'), pm_help=False)

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    return await client.change_presence(game=discord.Game(name='with a colour wheel'))

@client.command(pass_context=True)
async def set(ctx, role_name : str, colour_hex : str):
    print('invoked set')
    """Sets a role to the specific colour"""
    author_roles = ctx.message.author.roles
    server = ctx.message.server

    try:
        role = role_available(role_name, author_roles)
        colour = colour_from_hex(colour_hex)
    except ValueError as e:
        await client.say(e)
        return

    await client.edit_role(server, role, colour=colour)
    await client.say("lookin' good, good lookin'")


def colour_from_hex(code):
    if not re.match(r'#[\da-f]{6}$', code):
        raise ValueError('`%s` is not a valid hex colour value' % code)

    # convert hex colour code to decimal value
    value = int(code[1:], 16)
    return discord.Colour(value)


def role_available(role_name, role_list):
    '''Attempt to get a role matching role_name, case insensitive'''
    for role in role_list:
        if role_name.lower() == role.name.lower():
            return role
    raise ValueError("You don't have the `%s` role so I can't help, sorry" % role_name)


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--token', required=True, type=str)
args = parser.parse_args()

client.run(args.token)

