from typing import Any
from pydantic import BaseModel
from app.entities.models.video import Video
from app.entities.models.video_generate import VideoGenerate
from app.entities.models.image import Image
from app.entities.payloads.requests.generate_request import GenerateRequest
from app.external import minios
from app.external.rabbitmq.client import RabbitMQClient

class ExecutionData(BaseModel):
    generate_request: GenerateRequest

    video: Video | None = None
    image: Image | None = None
    video_generate: VideoGenerate | None = None

    def __init__(self, 
        video: Video, image: Image, video_generate: VideoGenerate, 
    ):
        self.video = video
        self.image = image
        self.video_generate = video_generate
