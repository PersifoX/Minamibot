from rcon.source import rcon

from config import get_settings


class Rcon:
    def __init__(self) -> None:
        self.config = get_settings()

    async def exec(self, command) -> str:
        return await rcon(
            command=command,
            host=self.config.minecraft_server_ip,
            port=self.config.minecraft_server_port,
            passwd=self.config.minecraft_server_password,
        )
