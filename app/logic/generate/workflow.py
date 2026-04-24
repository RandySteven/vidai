from app.logic.generate.execution_data import ExecutionData
from app.repositories.video import VideoRepository
from app.entities.models.video import Video
from temporalio import workflow
from app.entities.payloads.requests.generate_request import GenerateRequest
from app.logic.generate.validate_image_url import validate_image_url

@workflow.defn
class GenerateWorkflow:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    @workflow.run
    async def generate(self, request: GenerateRequest) -> Video:
        execution_data = ExecutionData()
        execution_data.generate_request = request

        execution_data.image = await validate_image_url.execute(execution_data)
        