from rcon.source import rcon

from _logging import get_logger
from config import get_settings

logger = get_logger(__name__)


class Rcon:
    def __init__(self) -> None:
        self.config = get_settings()

    async def exec(self, command) -> str:
        logger.info(
            f"Executing command: {command} on {self.config.minecraft_server_ip}"
        )

        res = await rcon(
            command=command,
            host=self.config.minecraft_server_ip,
            port=self.config.minecraft_server_port,
            passwd=self.config.minecraft_server_password,
        )

        logger.info(
            f"Command {command} executed on {self.config.minecraft_server_ip}: {res}"
        )

        return res
