from app.entities.models.image import Image
from app.external.mysql.repository import MySQLRepository
from app.repositories.repository import Repository


class ImageRepository(Repository):

    def __init__(self):
        self.mysql_repository = MySQLRepository()

    def save(self, entity: Image):
        query = "INSERT INTO images (image_url, uploaded_by) VALUES (%s, %s)"
        self.mysql_repository.execute(query, (entity.image_url, entity.uploaded_by))