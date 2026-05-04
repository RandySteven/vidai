from typing import Any
from pydantic import BaseModel
from datetime import datetime
from app.enums.generate_status import GenerateStatus

class Video(BaseModel):
    id: int
    reference_id: str
    video_url: str
    status: GenerateStatus
    prompt: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)