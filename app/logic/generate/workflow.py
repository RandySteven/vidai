from datetime import timedelta
from temporalio.common import RetryPolicy
from app.entities.models.image import Image
from app.entities.models.video_generate import VideoGenerate
from app.external import minio
from app.logic.generate.execution_data import ExecutionData
from app.repositories.video import VideoRepository
from app.repositories.image import ImageRepository
from app.entities.models.video import Video
from temporalio import workflow
from app.entities.payloads.requests.generate_request import GenerateRequest
from app.logic.generate.activities import GenerateActivity
from app.external.minio.client import MinioClient

@workflow.defn
class GenerateWorkflow:
    def __init__(self, 
        video_repository: VideoRepository, 
        image_repository: ImageRepository,
        minio_client: MinioClient
    ):    
        self.image_repository = image_repository
        self.video_repository = video_repository
        self.minio_client = minio_client
        self.execution_data = ExecutionData(
            video_generate=VideoGenerate(),
            video=Video(),
            image=Image(),
            image_repository=self.image_repository,
            video_repository=self.video_repository,
            minio_client=self.minio_client
        )

    @workflow.run
    async def generate(self, request: GenerateRequest) -> Video:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
            non_retryable_error_types=[]
        )

        self.execution_data.generate_request = request

        validate_image_output = await workflow.execute_activity_method(
            GenerateActivity.validate_image_url,
            self.execution_data,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )

        generate_video_output = await workflow.execute_activity_method(
            GenerateActivity.generate_video,
            self.execution_data,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )
