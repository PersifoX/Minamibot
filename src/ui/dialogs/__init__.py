import disnake

from config import get_settings
from models.db import Player


class ModalRequest(disnake.ui.Modal):
    def __init__(
        self,
        *,
        title: str = "Заполнить заявку",
        custom_id: str = "request_modal",
        timeout: float = 600,
    ) -> None:

        components = [
            disnake.ui.TextInput(
                label="Имя игрока в minecraft",
                placeholder="Jynow",
                custom_id="name",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Ваш возраст",
                placeholder="17",
                custom_id="age",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Лицензионная версия? (по умолчанию нет)",
                placeholder="да",
                custom_id="license",
                style=disnake.TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Что вы собираетесь делать на сервере?",
                placeholder="В кратце расскажите, что собираетесь делать",
                custom_id="reason",
                style=disnake.TextInputStyle.long,
            ),
        ]

        super().__init__(
            title=title, components=components, custom_id=custom_id, timeout=timeout
        )

    async def callback(self, inter):
        await inter.response.defer(ephemeral=True)

        values = list(inter.text_values.values())

        from ui.contexts import DefaultEmbed, WarningEmbed

        try:
            await Player(
                id=int(inter.user.id),
                username=values[0],
                age=int(values[1]),
                license=bool(values[2]),
                reason=values[3],
            ).save()

        except:
            return await inter.send(
                embed=WarningEmbed(description="Неверные данные"), ephemeral=True
            )

        channel = inter.guild.get_channel(get_settings().channel_id)

        await channel.send(
            embed=DefaultEmbed(
                title="Новая заявка",
                description=(
                    f"Кликните на {inter.user.mention} правой мышкой и нажмите `approve`, чтобы принять заявку"
                    "\n**OR**\n"
                    "Используйте команду `/request approve` для принятия заявки"
                ),
            )
            .set_thumbnail(url=inter.user.display_avatar.url)
            .add_field(
                name="Имя",
                value=values[0],
            )
            .add_field(
                name="Возраст",
                value=values[1],
            )
            .add_field(
                name="Лицензия",
                value=values[2],
            )
            .add_field(
                name="Причина",
                value=values[3],
            )
            .add_field(
                name="Автор",
                value=inter.user.mention,
            )
        )

        await inter.send(
            embed=DefaultEmbed(
                description="Заявка отправлена. В скором времени она будет рассмотрена, ожидайте!"
            ),
            ephemeral=True,
        )
