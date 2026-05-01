from app.repositories.user import UserRepository
from app.entities.models.user import User
from app.entities.payloads.requests.onboarding_request import RegisterRequest, LoginRequest
from app.entities.payloads.responses.onboarding_response import RegisterResponse, LoginResponse
from datetime import datetime, timezone
from fastapi import HTTPException

class OnboardingService:
    
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def register(self, request: RegisterRequest) -> RegisterResponse:
        user = User(
            id=None,
            username=request.username,
            email=request.email,
            password=request.password,
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.user_repository.save(user)
        return RegisterResponse(message="User registered successfully")

    def login(self, request: LoginRequest) -> LoginResponse:
        user = self.user_repository.find_by_email(request.email)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if user.password != request.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return LoginResponse(message="User logged in successfully")

def get_onboarding_service() -> OnboardingService:
    return OnboardingService()