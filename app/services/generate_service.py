import asyncio
from datetime import datetime, timezone

from app.entities.payloads.requests.generate_request import GenerateRequest
from app.entities.payloads.responses.generate_response import GenerateResponse
from app.enums.generate_status import GenerateStatus
from app.external.minio.client import MinioClient
from app.external.rabbitmq.client import RabbitMQClient
from app.logic.generate.workflow import GenerateWorkflow
from app.repositories.image import ImageRepository
from app.repositories.video import VideoRepository


class GenerateService:

    def __init__(self,
        video_repository: VideoRepository,
        image_repository: ImageRepository,
        rabbitmq_client: RabbitMQClient,
        minio_client: MinioClient
    ) -> None:
        self.workflow = GenerateWorkflow(
            video_repository,
            image_repository,
            minio_client
        )
        self.video_repository = video_repository
        self.image_repository = image_repository
        self.rabbitmq_client = rabbitmq_client
        self.minio_client = minio_client

    def start_generation(self, request: GenerateRequest) -> GenerateResponse:
        now = datetime.now(timezone.utc)
        asyncio.run(self.workflow.generate(request))
        return GenerateResponse(
            video_url="",
            reference_id=request.idempotency_key,
            status=GenerateStatus.QUEUED,
            prompt=request.prompt,
            created_at=now,
            updated_at=now,
        )

    def get_by_reference_id(self, reference_id: str) -> GenerateResponse:
        video = self.video_repository.find_by_reference_id(reference_id)
        generate_response = GenerateResponse(
            video_url=video.video_url,
            status=video.status,
            prompt=video.prompt,
            reference_id=video.reference_id,
            created_at=video.created_at,
            updated_at=video.updated_at
        )
        return generate_response



def get_generate_service(
    video_repository: VideoRepository,
    image_repository: ImageRepository,
    rabbitmq_client: RabbitMQClient,
    minio_client: MinioClient
) -> GenerateService:
    return GenerateService(
        video_repository,
        image_repository,
        rabbitmq_client,
        minio_client
    )
