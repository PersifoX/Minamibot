from disnake.ext.commands import Cog, InteractionBot, slash_command

from _logging import get_logger

logger = get_logger(__name__)


class Help(Cog):
    def __init__(self, bot: InteractionBot):
        self.bot = bot

    @slash_command(name="ping", description="Ping the bot")
    async def ping(self, inter):
        await inter.response.send_message(f"Pong! `{self.bot.latency * 1000:.2f}ms`")


def setup(bot: InteractionBot) -> None:
    bot.add_cog(Help(bot), override=True)
