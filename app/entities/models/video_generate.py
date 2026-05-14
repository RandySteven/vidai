from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.enums.generate_status import GenerateStatus


class VideoGenerateSettings(BaseModel):
    id: int
    request_id: str
    num_frames: int
    fps: int


class VideoGenerateInput(BaseModel):
    id: int
    request_id: str
    image_url: str
    prompt: str
    settings: VideoGenerateSettings


class VideoGenerateOutput(BaseModel):
    id: int
    request_id: str
    video_url: str


class VideoGenerate(BaseModel):
    id: int
    request_id: str
    job_id: str
    input: VideoGenerateInput
    output: VideoGenerateOutput
    status: GenerateStatus
    created_at: datetime
    finished_at: datetime | None = None
    updated_at: datetime
    deleted_at: datetime | None = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)