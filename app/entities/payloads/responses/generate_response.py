from pydantic import BaseModel
from datetime import datetime
from app.enums.generate_status import GenerateStatus

class GenerateResponse(BaseModel):
    video_url: str
    status: GenerateStatus
    reference_id: str
    prompt: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None