from temporalio import activity
from typing import Any, cast
import torch
import time
from app.logic.generate.execution_data import ExecutionData

dtype = torch.bfloat16
device = "cuda:0"
from diffusers.models.attention_dispatch import attention_backend
from diffusers.pipelines.hunyuan_video1_5.pipeline_hunyuan_video1_5_image2video import (
    HunyuanVideo15ImageToVideoPipeline,
)
from diffusers.utils.export_utils import export_to_video
from diffusers.utils.loading_utils import load_image

pipe = HunyuanVideo15ImageToVideoPipeline.from_pretrained("hunyuanvideo-community/HunyuanVideo-1.5-Diffusers-480p_i2v_step_distilled", torch_dtype=dtype)
pipe.enable_model_cpu_offload()
pipe.vae.enable_tiling()

@activity.defn
def generate_video(execution_data : ExecutionData) -> str:
    generate_request = execution_data.generate_request
    if generate_request is None:
        raise ValueError("generate_request is required")

    generator = torch.Generator(device=device).manual_seed(1)
    image = load_image(generate_request.imageURL)
    prompt = generate_request.prompt
    ts = time.time()
    video_file_name = f"{ts}" + ".mp4"
    with attention_backend("_flash_3_hub"):
        result = pipe(
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
    return export_to_video(video, video_file_name, fps=24)