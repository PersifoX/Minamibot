import disnake
from disnake import Colour, Embed
from disnake.ext.commands import Cog, InteractionBot

from _logging import get_logger
from models import init_db
from ui.contexts import DefaultEmbed, RequestView

logger = get_logger(__name__)


class Ping(Cog):
    def __init__(self, bot: InteractionBot):
        self.bot = bot

    @Cog.listener()
    async def on_start(self):
        pass

    @Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.bot.user}")

        await init_db()

        logger.info("Database initialized: OK")

    @Cog.listener()
    async def on_slash_command_error(self, inter, error):
        logger.exception(error, exc_info=error)

        await inter.send(
            embed=Embed(
                description="Some error here! Check you permissions! ❌",
                color=Colour.brand_red(),
            ),
            ephemeral=True,
        )

    @Cog.listener()
    async def on_button_click(self, inter: disnake.Interaction):

        if inter.component.custom_id != "request_event":
            return

        await inter.response.send_message(
            embed=DefaultEmbed(
                description="Прочтите правила и нажмите ✅. Если вы ошиблись в заявке или ее отклонили, вы можете повторно отправить заявку."
            ),
            view=RequestView(),
            ephemeral=True,
        )


def setup(bot: InteractionBot) -> None:
    bot.add_cog(Ping(bot), override=True)
