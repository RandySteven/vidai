from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.entities.payloads.requests.generate_request import GenerateRequest
from app.entities.payloads.responses.generate_response import GenerateResponse
from app.entities.payloads.responses.upload_image_response import UploadImageResponse
from app.services.generate_service import GenerateService, get_generate_service
from app.services.upload_service import UploadService, get_upload_service

router = APIRouter()


@router.post("/generate")
async def generate_video(
    request: GenerateRequest,
    service: GenerateService = Depends(get_generate_service),
) -> GenerateResponse:
    return service.start_generation(request)


@router.post("/upload-image")
async def upload_image(
    image: UploadFile = File(..., description="Image bytes (jpeg, png, gif, or webp)"),
    uploaded_by: str = Form(..., min_length=1),
    service: UploadService = Depends(get_upload_service),
) -> UploadImageResponse:
    data = await image.read()
    return service.upload_image(
        data=data,
        filename=image.filename,
        content_type=image.content_type,
        uploaded_by=uploaded_by,
    )
