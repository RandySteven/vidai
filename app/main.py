from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as v1_router
from app.config import get_settings

from temporalio.client import Client
from temporalio.worker import Worker

from app.external import RedisPubSub, get_minio_client, get_temporal_client
from app.logic.generate.activities import GenerateActivity
from app.logic.generate.workflow import GenerateWorkflow
from app.repositories import get_all_repositories

def _uploads_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "uploads"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    repositories = get_all_repositories()
    temporal_client = get_temporal_client()
    minio_client = get_minio_client()

    generate_activity_instance = GenerateActivity(
        image_repository=repositories.image_repository,
        video_repository=repositories.video_generate_repository,
        pubsub=RedisPubSub(),
        minio_client=minio_client
    )

    worker = Worker(
        temporal_client,
        task_queue="generate-video-queue",
        workflows=[GenerateWorkflow],
        activities=[
            generate_activity_instance.init_video,
            generate_activity_instance.publish,
            generate_activity_instance.validate_image_url,
            generate_activity_instance.generate_video,
            generate_activity_instance.upload_video,
            generate_activity_instance.update_video
        ]
    )

    _app.state.temporal_client = temporal_client

    async with worker:
        yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )
    if settings.cors_origin_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origin_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.include_router(v1_router, prefix="/api/v1")
    uploads = _uploads_dir()
    uploads.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(uploads)), name="uploads")
    return app


app = create_app()
