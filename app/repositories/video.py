from app.entities.models.video import Video
from app.external import MySQLRepository
from app.repositories.repository import Repository


class VideoRepository(Repository):
    def __init__(self):
        self.mysql_repository = MySQLRepository()

    def save(self, video: Video):
        query = "INSERT INTO video () VALUES (NULL, %s, %s)"
        self.mysql_repository.execute(query, video)

    def find_by_id(self, id: str):
        query = "SELECT * FROM video WHERE id = %s"
        return self.mysql_repository.fetch_one(query, id)

    def find_all(self):
        query = "SELECT * FROM video"
        return self.mysql_repository.fetch_all(query)

    def delete(self, id: str):
        query = "DELETE FROM video WHERE id = %s"
        self.mysql_repository.execute(query, id)