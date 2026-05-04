from app.entities.models.video import Video
from app.external import MySQLRepository
from app.repositories.repository import Repository


class VideoRepository(Repository):
    def __init__(self):
        self.mysql_repository = MySQLRepository()

    def save(self, video: Video):
        query = "INSERT INTO videos (video_url, status, prompt, reference_id) VALUES (:video_url, :status, :prompt, :reference_id)"
        self.mysql_repository.execute(
            query,
            {"video_url": video.video_url, "status": video.status, "prompt": video.prompt, "reference_id": video.reference_id},
            commit=True,
        )

    def find_by_id(self, id: str):
        query = "SELECT * FROM videos WHERE id = :id"
        return self.mysql_repository.fetch_one(query, {"id": id})

    def find_by_reference_id(self, reference_id: str) -> Video:
        query = "SELECT * FROM videos WHERE reference_id = :reference_id"
        return self.mysql_repository.fetch_one(query, {"reference_id": reference_id})

    def find_all(self):
        query = "SELECT * FROM videos"
        return self.mysql_repository.fetch_all(query)

    def delete(self, id: str):
        query = "DELETE FROM videos WHERE id = :id"
        self.mysql_repository.execute(query, {"id": id}, commit=True)