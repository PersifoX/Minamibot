from disnake.ext.commands import Cog, InteractionBot, slash_command

from _logging import get_logger
from services.rcon import Rcon
from ui.contexts import DefaultEmbed

logger = get_logger(__name__)


class Server(Cog):
    def __init__(self, bot: InteractionBot):
        self.bot = bot
        self.rcon = Rcon()

    @slash_command(name="server")
    async def server(self, inter):
        pass

    @server.sub_command("list", description="⭐ | Check Online Players")
    async def list(self, inter):

        await inter.response.send_message(
            embed=DefaultEmbed(description=await self.rcon.exec(command="list"))
        )

    @server.sub_command("version", description="Check Server Version")
    async def version(self, inter):
        await inter.response.send_message(
            "```\n" + await self.rcon.exec(command="version") + "\n```"
        )

    # @has_role(get_settings().role_id)
    # @server.sub_command("command", description="Execute command on server")
    # async def command(self, inter, command: str):
    #     Rcon().exec(command=command)


def setup(bot: InteractionBot) -> None:
    bot.add_cog(Server(bot), override=True)
