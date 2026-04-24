from pydantic import BaseModel
from app.entities.models.video import Video
from app.entities.models.video_generate import VideoGenerate
from app.entities.models.image import Image

class ExecutionData(BaseModel):
    generate_request: GenerateRequest | None = None

    video: Video | None = None
    image: Image | None = None
    video_generate: VideoGenerate | None = None
