from .rcon import Rcon


class Whitelist(Rcon):

    async def add(self, username: str):
        await self.exec(f"whitelist add {username}")

    async def remove(self, username: str):
        await self.exec(f"whitelist remove {username}")

    async def list(self) -> str:
        return await self.exec(f"whitelist list")
