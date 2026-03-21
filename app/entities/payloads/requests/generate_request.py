from pydantic import BaseModel

class VideoSettings(BaseModel):
    num_frames: int
    fps: int
    motion_bucket_id: int
    noise_aug_strength: int
    width: int
    height: int

class GenerateRequest(BaseModel):
    prompt: str
    imageURL: str
    settings: VideoSettings
