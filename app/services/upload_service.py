from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, status

from app.entities.payloads.responses.upload_image_response import UploadImageResponse
from app.external.mongodb import MongoRepository

_MAX_BYTES = 15 * 1024 * 1024
_ALLOWED_TYPES = frozenset(
    {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    }
)
_EXT_BY_TYPE = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _uploads_dir() -> Path:
    d = _project_root() / "uploads"
    d.mkdir(parents=True, exist_ok=True)
    return d


class UploadService:
    def __init__(self, repository: MongoRepository | None = None) -> None:
        self._repo = repository or MongoRepository(collection_name="images")

    def upload_image(
        self,
        *,
        data: bytes,
        filename: str | None,
        content_type: str | None,
        uploaded_by: str,
    ) -> UploadImageResponse:
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file",
            )
        if len(data) > _MAX_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large",
            )
        ct = (content_type or "").split(";")[0].strip().lower()
        if ct not in _ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported content type: {content_type!r}",
            )

        ext = _EXT_BY_TYPE[ct]
        stored_name = f"{uuid.uuid4().hex}{ext}"
        path = _uploads_dir() / stored_name
        path.write_bytes(data)

        now = datetime.now(timezone.utc)
        public_path = f"/uploads/{stored_name}"
        doc = {
            "filename": filename or stored_name,
            "stored_name": stored_name,
            "content_type": ct,
            "size": len(data),
            "uploaded_by": uploaded_by,
            "image_url": public_path,
            "created_at": now,
            "updated_at": now,
        }
        inserted_id = self._repo.insert_one(doc)

        return UploadImageResponse(
            id=str(inserted_id),
            image_url=public_path,
            uploaded_by=uploaded_by,
            created_at=now,
            updated_at=now,
        )


def get_upload_service() -> UploadService:
    return UploadService()
