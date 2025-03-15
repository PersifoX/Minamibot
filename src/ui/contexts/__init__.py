import datetime

import disnake
from disnake.ui import View, button

from ..dialogs import ModalRequest


class DefaultEmbed(disnake.Embed):
    def __init__(self, *, title=None, type="rich", description=None, url=None):
        super().__init__(
            title=title,
            type=type,
            description=description,
            url=url,
            timestamp=datetime.datetime.now(),
            color=disnake.Colour.brand_green(),
        )

        self.set_footer(
            text="MinamiBot",
            icon_url="https://cdn.discordapp.com/icons/1163234591595843585/68fb6b7f6c33134fd311c718a2e08174.webp?size=96",
        )


class WarningEmbed(disnake.Embed):
    def __init__(self, *, title=None, type="rich", description=None, url=None):
        super().__init__(
            title=title,
            type=type,
            description=description,
            url=url,
            timestamp=datetime.datetime.now(),
            color=disnake.Colour.yellow(),
        )

        self.set_footer(
            text="MinamiBot",
            icon_url="https://cdn.discordapp.com/icons/1163234591595843585/68fb6b7f6c33134fd311c718a2e08174.webp?size=96",
        )


def genembed(
    title: str,
    description: str,
    color=disnake.Colour.blurple(),
    thumbnail: str = None,
    image=None,
    author_url=None,
    author_name="MinamiBot",
    author_icon=None,
    footer=None,
) -> disnake.Embed:

    embed = disnake.Embed(
        title=title,
        description=description,
        colour=color,
        timestamp=datetime.datetime.now(),
    )

    if author_name:
        embed.set_author(name=author_name, icon_url=author_icon, url=author_url)

    if thumbnail:
        embed.set_thumbnail(thumbnail)

    if image:
        if isinstance(image, disnake.File):
            embed.set_image(file=image)
        else:
            embed.set_image(image)

    if footer:
        embed.set_footer(text=footer)

    return embed


class RequestView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(emoji="✅")
    async def open_request(self, button, interaction):
        await interaction.response.send_modal(ModalRequest())
