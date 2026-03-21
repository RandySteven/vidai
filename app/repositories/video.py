from app.entities.models.video import Video
from app.external import MySQLRepository
from app.repositories.repository import Repository


class VideoRepository(Repository):
    def __init__(self):
        self.mysql_repository = MySQLRepository()

    def save(self, video: Video):
        query = "INSERT INTO videos (video_url, status, prompt) VALUES (%s, %s, %s)"
        self.mysql_repository.execute(query, (video.video_url, video.status, video.prompt))

    def find_by_id(self, id: str):
        query = "SELECT * FROM videos WHERE id = %s"
        return self.mysql_repository.fetch_one(query, id)

    def find_all(self):
        query = "SELECT * FROM videos"
        return self.mysql_repository.fetch_all(query)

    def delete(self, id: str):
        query = "DELETE FROM videos WHERE id = %s"
        self.mysql_repository.execute(query, id)