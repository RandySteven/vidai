from app.external.mysql.repository import MySQLRepository
from app.entities.models.user import User

class UserRepository:
    def __init__(self) -> None:
        self.mysql_repository = MySQLRepository()

    def save(self, user: User) -> None:
        query = """
        INSERT INTO users (username, email, password, status, created_at, updated_at)
        VALUES (:username, :email, :password, :status, :created_at, :updated_at)
        """
        self.mysql_repository.execute(
            query,
            {
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "status": user.status,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            },
            commit=True,
        )

    def find_by_id(self, id: str) -> User:
        query = "SELECT * FROM users WHERE id = :id"
        return self.mysql_repository.fetch_one(query, {"id": id})
    
    def find_by_email(self, email: str) -> User:
        query = "SELECT * FROM users WHERE email = :email"
        return self.mysql_repository.fetch_one(query, {"email": email})