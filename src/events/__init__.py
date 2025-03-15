from os import listdir

from disnake.ext import commands

from _logging import get_logger

logger = get_logger(__name__)


def register_events(bot: commands.InteractionBot):
    for filename in listdir(f"./events"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                bot.load_extension(f"events.{filename[:-3]}")
                logger.info(f"cog {filename} loaded")

            except Exception as error:
                logger.error(f"cog filename not loaded: {error}")
