from pydantic import BaseModel


class ExecutionData(BaseModel):
    prompt: str
    image_url: str
