"""
Minecraft Server Manager with discord bot
"""

from ui.console.logo import get_logo

print(get_logo())

import disnake
from disnake.ext import commands

from _logging import get_logger
from commands import register_commands
from config import get_settings
from events import register_events

logger = get_logger(__name__)


bot = commands.InteractionBot(
    intents=disnake.Intents.all(),
    test_guilds=[get_settings().guild_id],
    sync_commands_debug=True,
)

register_commands(bot)
register_events(bot)

bot.run(get_settings().discord_token)
