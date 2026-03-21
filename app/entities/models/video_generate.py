from datetime import datetime

from pydantic import BaseModel

from app.enums.generate_status import GenerateStatus


class VideoGenerateSettings(BaseModel):
    num_frames: int
    fps: int


class VideoGenerateInput(BaseModel):
    image_url: str
    prompt: str
    settings: VideoGenerateSettings


class VideoGenerateOutput(BaseModel):
    video_url: str


class VideoGenerate(BaseModel):
    id: str
    job_id: str
    input: VideoGenerateInput
    output: VideoGenerateOutput
    status: GenerateStatus
    created_at: datetime
    finished_at: datetime | None = None
    updated_at: datetime
    deleted_at: datetime | None = None
