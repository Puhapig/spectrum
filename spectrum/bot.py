import asyncio
import discord
from discord.ext import commands

import argparse
import platform

client = commands.Bot(
    description='Changes role colour on command',
    command_prefix=commands.when_mentioned_or('!colour '),
    pm_help=False,
)
startup_extensions = ["colour"]


@client.event
async def on_ready():
    print(
        f'Logged in as {client.user.name}\n'
        '--------\n'
        f'Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}'
    )
    return await client.change_presence(game=discord.Game(name='with a colour wheel'))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exception_type = type(e).__name__
            print(f'Failed to load extension {extension}\n{exception_type}: {e}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True, type=str)
    args = parser.parse_args()
    client.run(args.token)
