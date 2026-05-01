from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Image(BaseModel):
    id: str
    image_url: str 
    uploaded_by: str
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)