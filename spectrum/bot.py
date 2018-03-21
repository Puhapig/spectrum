import asyncio
import discord
from discord.ext import commands

import argparse
import logging
import platform
import os

TOKEN_ENV_VAR = 'DISCORD_TOKEN'
STARTUP_EXTENSIONS = ["colour"]

logger = logging.getLogger('discord-spectrum')
formatter = logging.Formatter('%(asctime)s %(levelname)8s - %(message)s')
ch = logging.StreamHandler()

logger.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', type=str)
    parser.add_argument('-p', '--prefix', type=str, default='colour')
    args = parser.parse_args()
    command_prefix = f'!{args.prefix} '

    client = commands.Bot(
        description='Changes role colour on command',
        command_prefix=commands.when_mentioned_or(command_prefix),
        pm_help=False,
    )

    @client.event
    async def on_ready():
        client_info = [
            'CONNECTED',
            f'Current Python Version: {platform.python_version()}',
            f'Current Discord.py Version: {discord.__version__}',
            f'Logged in as {client.user.name}',
            f'Command prefix: {command_prefix}',
        ]
        for line in client_info: logger.info(line)
        return await client.change_presence(game=discord.Game(name='with a colour wheel'))


    logger.info(f'loading extensions {STARTUP_EXTENSIONS}')
    for extension in STARTUP_EXTENSIONS:
        try:
            client.load_extension(extension)
            logger.info(f'loaded {extension}')
        except Exception as e:
            exception_type = type(e).__name__
            logger.error(f'Failed to load extension {extension}\n{exception_type}: {e}')

    if (TOKEN_ENV_VAR in os.environ):
        token = os.environ[TOKEN_ENV_VAR]
        logger.debug(f'Using Discord client token from {TOKEN_ENV_VAR}')
    else:
        token = args.token
        logger.debug(f'Using Discord client token set using -t, --token')
    client.run(token)
