from datetime import datetime, timezone

from app.entities.payloads.requests.generate_request import GenerateRequest
from app.entities.payloads.responses.generate_response import GenerateResponse
from app.enums.generate_status import GenerateStatus


class GenerateService:
    def start_generation(self, request: GenerateRequest) -> GenerateResponse:
        now = datetime.now(timezone.utc)
        return GenerateResponse(
            video_url="",
            status=GenerateStatus.QUEUED,
            prompt=request.prompt,
            created_at=now,
            updated_at=now,
        )


def get_generate_service() -> GenerateService:
    return GenerateService()
