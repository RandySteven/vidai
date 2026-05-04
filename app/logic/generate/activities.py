import asyncio

from temporalio import activity

from app.entities.models.video import Video
from app.enums.generate_status import GenerateStatus
from app.logic.generate.execution_data import ExecutionData
from app.repositories.image import ImageRepository
from app.errors.error import Error
from temporalio import activity
from typing import Any, cast
import importlib
import torch
import time
from app.logic.generate.execution_data import ExecutionData
from app.repositories.video import VideoRepository
from app.external.minio.client import MinioClient

dtype = torch.bfloat16
device = "cuda:0"
from diffusers.models.attention_dispatch import attention_backend
from diffusers.pipelines.hunyuan_video1_5.pipeline_hunyuan_video1_5_image2video import (
    HunyuanVideo15ImageToVideoPipeline,
)
from diffusers.utils.loading_utils import load_image

class GenerateActivity:
    def __init__(self) -> None:
        self.export_utils = cast(Any, importlib.import_module("diffusers.utils.export_utils"))
        self.pipe = HunyuanVideo15ImageToVideoPipeline.from_pretrained("hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_i2v_step_distilled", torch_dtype=dtype)
        
        self.pipe.enable_model_cpu_offload()
        self.pipe.vae.enable_tiling()

    @activity.defn
    async def init_video(self, execution_data: ExecutionData) -> ExecutionData:
        video_repository = VideoRepository()
        video = Video(
            reference_id=execution_data.generate_request.idempotency_key,
            status=GenerateStatus.QUEUED,
            prompt=execution_data.generate_request.prompt
        )
        video = video_repository.save(video)
        execution_data.video = video
        return execution_data

    @activity.defn
    async def publish(self, execution_data: ExecutionData) -> ExecutionData:
        execution_data.rabbitmq_client.publish('generate_video', execution_data.video)

    @activity.defn
    async def validate_image_url(self, execution_data : ExecutionData) -> ExecutionData:
        image_repository = ImageRepository()
        image = image_repository.find_by_url(execution_data.image.image_url if execution_data.image is not None else "")
        if image is None:
            image_repository.save(image)
            execution_data.image = image
        return execution_data
    
    @activity.defn
    async def generate_video(self, execution_data : ExecutionData) -> ExecutionData:
        generate_request = execution_data.generate_request
        if generate_request is None:
            raise ValueError("generate_request is required")

        generator = torch.Generator(device=device).manual_seed(1)
        image = load_image(generate_request.imageURL)
        prompt = generate_request.prompt
        ts = time.time()
        video_file_name = f"{ts}" + ".mp4"
        with attention_backend("_flash_3_hub"):
            result = self.pipe(
                prompt=prompt,
                image=image,
                generator=generator,
                num_frames=121,
                num_inference_steps=12
            )

        if hasattr(result, "frames"):
            frames = cast(Any, result).frames
        else:
            frames = cast(Any, result)[0]
        video = frames[0]
        video_path = self.export_utils.export_to_video(video, video_file_name, fps=24)

        if execution_data.video is not None:
            execution_data.video.video_url = video_path
        
        return execution_data

    @activity.defn
    async def upload_video(self, execution_data: ExecutionData) -> ExecutionData:
        if execution_data.video is not None:
            execution_data.minio_client.upload_file_path(execution_data.video.video_url, "vidai-video", execution_data.video.video_url)
        return execution_data

    async def save_video(self, execution_data: ExecutionData) -> ExecutionData:
        return execution_data