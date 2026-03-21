from app.repositories.video import VideoRepository
from app.entities.models.video import Video
from temporalio import workflow

@workflow.defn
class GenerateWorkflow:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    @workflow.run
    async def generate(self, request: GenerateRequest) -> Video:
        execution_data = ExecutionData()
        execution_data.image = await validate_image_url.execute(execution_data)
        pass