import disnake
from disnake.ext.commands import Cog, InteractionBot, has_role, slash_command

from _logging import get_logger
from config import get_settings
from services.whitelist import Whitelist
from ui.contexts import DefaultEmbed

logger = get_logger(__name__)


class Admin(Cog):
    def __init__(self, bot: InteractionBot):
        self.bot = bot
        self._whitelist = Whitelist()

    @slash_command(name="admin")
    async def admin(self, inter):
        pass

    @has_role(get_settings().role_id)
    @admin.sub_command(name="command", description="⭐ | Run a command on Server")
    async def command(self, inter, command: str):
        await inter.response.send_message(
            (await self._whitelist.exec(command)) or "*Nothing to response*"
        )

    @admin.sub_command_group(name="whitelist")
    async def whitelist(self, inter):
        pass

    @has_role(get_settings().role_id)
    @whitelist.sub_command("list", description="⭐ | List whitelisted players")
    async def whitelist_list(self, inter):
        await inter.response.send_message(
            embed=DefaultEmbed(description=await self._whitelist.list())
        )

    @has_role(get_settings().role_id)
    @whitelist.sub_command("add", description="Add player to whitelist")
    async def whitelist_add(self, inter, username: str):
        await inter.response.defer()

        await self._whitelist.add(username)

        await inter.send(embed=DefaultEmbed(description="Player added to whitelist"))

        logger.info(f"Added {username} to whitelist")

    @has_role(get_settings().role_id)
    @whitelist.sub_command("remove", description="Remove player from whitelist")
    async def whitelist_remove(self, inter, username: str):
        await inter.response.defer()

        await self._whitelist.remove(username)

        await inter.send(
            embed=DefaultEmbed(description="Player removed from whitelist")
        )

        logger.info(f"Removed {username} from whitelist")


def setup(bot: InteractionBot) -> None:
    bot.add_cog(Admin(bot), override=True)
