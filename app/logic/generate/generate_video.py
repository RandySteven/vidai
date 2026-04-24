from temporalio import activity
import torch
import time

dtype = torch.bfloat16
device = "cuda:0"
from diffusers import HunyuanVideo15ImageToVideoPipeline, attention_backend
from diffusers.utils import export_to_video, load_image

@activity.defn
def generate_video(execution_data : ExecutionData):
    generator = torch.Generator(device=device).manual_seed(1)
    image = load_image(execution_data.request.imageURL)
    prompt = execution_data.request.prompt
    ts = time.time()
    video_file_name = f"{ts}" + ".mp4"
    with attention_backend("_flash_3_hub"):
        video = pipe(
            prompt=prompt,
            image=image,
            generator=generator,
            num_frames=121,
            num_inference_steps=12
        ).frames[0]
    export_to_video(video, video_file_name, fps=24)