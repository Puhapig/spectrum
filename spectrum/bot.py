import discord
import asyncio

import argparse
import re
import math

from discord.ext import commands
import platform

client = commands.Bot(description='Changes role colour on command', command_prefix=commands.when_mentioned_or('clr '), pm_help=False)
startup_extensions = ["colour"]

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    return await client.change_presence(game=discord.Game(name='with a colour wheel'))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True, type=str)
    args = parser.parse_args()

    client.run(args.token)

