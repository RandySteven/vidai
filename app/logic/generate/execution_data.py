from typing import Any
from pydantic import BaseModel
from app.entities.models.video import Video
from app.entities.models.video_generate import VideoGenerate
from app.entities.models.image import Image
from app.entities.payloads.requests.generate_request import GenerateRequest
from app.external import minio
from app.external.rabbitmq.client import RabbitMQClient
from app.repositories.image import ImageRepository
from app.repositories.repository import Repository
from app.repositories.video import VideoRepository
from app.external.minio.client import MinioClient

class ExecutionData(BaseModel):
    generate_request: GenerateRequest

    video: Video | None = None
    image: Image | None = None
    video_generate: VideoGenerate | None = None

    image_repository: ImageRepository
    video_repository: VideoRepository
    minio_client: MinioClient
    rabbitmq_client: RabbitMQClient

    def __init__(self, 
        video: Video, image: Image, video_generate: VideoGenerate, 
        image_repository: ImageRepository, video_repository: VideoRepository,
        rabbitmq_client: RabbitMQClient,
        minio_client: MinioClient
    ):
        self.video = video
        self.image = image
        self.video_generate = video_generate
        self.image_repository = image_repository
        self.video_repository = video_repository
        self.rabbitmq_client = rabbitmq_client
        self.minio_client = minio_client