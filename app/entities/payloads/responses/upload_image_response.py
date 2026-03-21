from datetime import datetime

from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    id: str
    image_url: str
    uploaded_by: str
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
