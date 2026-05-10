from abc import abstractmethod

from pydantic import BaseModel

from app.repositories import get_user_repository, get_video_generate_repository, get_video_repository
from app.repositories.image import ImageRepository, get_image_repository
from app.repositories.user import UserRepository
from app.repositories.video import VideoRepository
from app.repositories.video_generate import VideoGenerateRepository


class Repository:

    @abstractmethod
    def save(self, entity: BaseModel):
        pass

    @abstractmethod
    def find_by_id(self, id: str):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def update(self, entity: BaseModel):
        pass

class Repositories:
    image_repository : ImageRepository
    video_repository : VideoRepository
    user_repository : UserRepository
    video_generate_repository : VideoGenerateRepository

    def __init__(self) -> None:
        self.image_repository = get_image_repository()
        self.video_generate_repository = get_video_generate_repository()
        self.video_repository = get_video_repository()
        self.user_repository = get_user_repository()

def get_all_repositories() -> Repositories:
    return Repositories()