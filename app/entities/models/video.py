from pydantic import BaseModel
from datetime import datetime
from app.enums.generate_status import GenerateStatus

class Video(BaseModel):
    id: int
    video_url: str
    status: GenerateStatus
    prompt: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None