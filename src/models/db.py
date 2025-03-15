from datetime import datetime

from beanie import Document
from pydantic import Field


class Player(Document):
    id: int
    # ~~~~~~~~~~~~~~~~~~~
    username: str
    age: int
    reason: str
    license: bool = False
    # ~~~~~~~~~~~~~~~~~~~
    approved: bool = False
    declined: bool = False
    decline_reason: str | None = None
    # ~~~~~~~~~~~~~~~~~~~
    created_at: datetime = Field(default_factory=datetime.now)
