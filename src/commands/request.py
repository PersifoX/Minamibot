import disnake
from beanie.operators import And
from disnake.ext.commands import (
    Cog,
    InteractionBot,
    Param,
    has_role,
    slash_command,
    user_command,
)
from disnake.ui.button import Button

from _logging import get_logger
from config import get_settings
from models.db import Player
from services.whitelist import Whitelist
from ui.contexts import DefaultEmbed, WarningEmbed

logger = get_logger(__name__)


class Request(Cog):
    def __init__(self, bot: InteractionBot):
        self.bot = bot
        self.whitelist = Whitelist()

    @slash_command(name="request")
    async def request(self, inter):
        pass

    @has_role(get_settings().role_id)
    @request.sub_command(
        "list", description="⭐ | List declined or new requests on Minami"
    )
    async def list(self, inter):
        players = await Player.find(And(Player.approved == False)).to_list()

        formatted = (
            f"\n".join(
                [
                    f"<@{player.id}> - {player.username} ({ '**declined**' if player.declined else 'new'})"
                    for player in players
                ]
            )
            if players
            else "**No requests yet!**"
        )

        await inter.response.send_message(
            embed=DefaultEmbed(
                title="Declined and new requests",
                description=formatted,
            )
        )

    @has_role(get_settings().role_id)
    @request.sub_command("approve", description="Approve request on Minami")
    async def approve(self, inter, member: disnake.Member, quiet: bool = False):
        await inter.response.defer()

        player = await Player.get(member.id)

        if not player:
            return await inter.send(
                embed=WarningEmbed(description="Player not found"), ephemeral=quiet
            )

        if player.approved:
            return await inter.send(
                embed=DefaultEmbed(
                    description="Player already approved", ephemeral=quiet
                )
            )

        player.approved = True
        await player.save()

        await self.whitelist.add(player.username)

        await inter.send(
            embed=DefaultEmbed(description="Player approved"), ephemeral=quiet
        )

        await member.create_dm()
        await member.dm_channel.send(
            embed=DefaultEmbed(
                title="Ваша заявка была принята",
                description=f"Добро пожаловать на сервер, **{player.username}**!\nАдрес сервера: **{get_settings().minecraft_server_url}**",
            )
        )

    @has_role(get_settings().role_id)
    @user_command("approve")
    async def approve_user(self, inter, member: disnake.Member):
        await self.approve(inter, member, quiet=True)

    @has_role(get_settings().role_id)
    @request.sub_command("decline", description="Decline request on Minami")
    async def decline(
        self, inter, member: disnake.Member, reason: str = None, quiet: bool = False
    ):
        await inter.response.defer()

        player = await Player.get(member.id)

        if not player:
            return await inter.send(
                embed=WarningEmbed(description="Player not found"), ephemeral=quiet
            )

        if player.declined:
            return await inter.send(
                embed=DefaultEmbed(
                    description="Player already declined", ephemeral=quiet
                )
            )

        player.declined = True
        player.decline_reason = reason
        await player.save()

        await self.whitelist.remove(player.username)

        await inter.send(
            embed=DefaultEmbed(description="Player declined"), ephemeral=quiet
        )

        await member.create_dm()
        await member.dm_channel.send(
            embed=WarningEmbed(
                title="Ваша заявка была отклонена",
                description="Причина:\n\n```\n"
                + reason
                + "\n```\n\nВы можете изменить текущую анкету в прежнем канале.",
            )
        )

    @has_role(get_settings().role_id)
    @user_command("decline")
    async def decline_user(self, inter, member: disnake.Member):
        await self.decline(inter, member, quiet=True)

    @has_role(get_settings().role_id)
    @request.sub_command("find", description="Find request on Minami")
    async def find(self, inter, member: disnake.Member):
        await inter.response.defer()

        player = await Player.get(member.id)

        if not player:
            return await inter.send(embed=WarningEmbed(description="Player not found"))

        embed = DefaultEmbed(title=player.username)

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.description = (
            f"**Username:** {player.username}\n"
            f"**Age:** {player.age}\n"
            f"**Reason:** {player.reason}"
            "\n\n"
            f"**Approved**: {'✅' if player.approved else '❌'}\n"
            f"**Declined**: {'✅' if player.declined else '❌'}"
            "\n\n"
            f"**Date:** <t:{player.created_at}:R>"
        )

        await inter.send(embed=embed)

    @has_role(get_settings().role_id)
    @request.sub_command(
        "create", description="Create request dialog on discord server"
    )
    async def create(
        self,
        inter,
        channel: disnake.TextChannel = Param(description="Канал для запроса"),
        title: str = Param(
            "Подать заявку на сервер MinamiCraft", description="Заголовок запроса"
        ),
        description: disnake.Attachment = Param(
            None, description="Описание запроса [текстовый файл]"
        ),
        image: str = Param(None, description="Большое изображение эмбеда"),
        thumbnail: str = Param(None, description="Малое изображение эмбеда"),
        button_name: str = Param("Открыть", description="Кнопка запроса"),
        button_emoji: disnake.Emoji = Param(None, description="Эмодзи на кнопке"),
    ):
        await inter.response.defer(ephemeral=True)

        description = (
            (await description.read()).decode()
            if description
            else "Кликните на кнопку и пройдите небольшую анкету!"
        )

        embed = disnake.Embed(
            title=title, description=description, colour=disnake.Colour.brand_green()
        )

        embed.set_image(url=image)
        embed.set_thumbnail(url=thumbnail)

        await channel.send(
            embed=embed,
            components=[
                Button(
                    style=disnake.ButtonStyle.green,
                    label=button_name,
                    emoji=button_emoji,
                    custom_id="request_event",
                )
            ],
        )

        await inter.send(
            embed=DefaultEmbed(description=f"Заявка создана в канал {channel.mention}")
        )


def setup(bot: InteractionBot) -> None:
    bot.add_cog(Request(bot), override=True)
