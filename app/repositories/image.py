from app.entities.models.image import Image
from app.external.mysql.repository import MySQLRepository
from app.repositories.repository import Repository


class ImageRepository(Repository):

    def __init__(self):
        self.mysql_repository = MySQLRepository()

    def save(self, entity: Image):
        query = "INSERT INTO images (image_url, uploaded_by) VALUES (%s, %s)"
        self.mysql_repository.execute(query, (entity.image_url, entity.uploaded_by))

    def find_by_id(self, id: str):
        query = "SELECT * FROM images WHERE id = %s"
        return self.mysql_repository.fetch_one(query, id)

    def find_all(self):
        query = "SELECT * FROM images"
        return self.mysql_repository.fetch_all(query)

    def delete(self, id: str):
        query = "DELETE FROM images WHERE id = %s"
        self.mysql_repository.execute(query, id)