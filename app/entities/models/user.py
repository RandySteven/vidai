from datetime import datetime, timezone

from pydantic import BaseModel, Field

class User(BaseModel):
    id: int | None
    username: str
    email: str
    password: str
    status: str = "active"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None