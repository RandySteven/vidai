import asyncio
from datetime import datetime, timezone
from app.entities.payloads.requests.generate_request import GenerateRequest
from app.entities.payloads.responses.generate_response import GenerateResponse
from app.enums.generate_status import GenerateStatus
from app.external import get_minio_client
from app.external.minios.client import MinioClient
from app.external.rabbitmq.client import RabbitMQClient
from app.logic.generate.workflow import GenerateWorkflow
from app.repositories.image import ImageRepository
from app.repositories.video import VideoRepository


class GenerateService:

    def __init__(self) -> None:
        self.video_repository = VideoRepository()
        self.image_repository = ImageRepository()
        self.rabbitmq_client = RabbitMQClient()
        self.minio_client = get_minio_client()

        self.workflow = GenerateWorkflow()

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

def get_generate_service() -> GenerateService:
    return GenerateService()
