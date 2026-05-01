from fastapi import APIRouter, Depends

from app.entities.payloads.requests.onboarding_request import RegisterRequest, LoginRequest
from app.entities.payloads.responses.onboarding_response import RegisterResponse, LoginResponse
from app.services.onboarding_service import OnboardingService, get_onboarding_service

router = APIRouter()

@router.post("/onboarding/register")
async def register(
    request: RegisterRequest,
    service: OnboardingService = Depends(get_onboarding_service),
) -> RegisterResponse:
    return service.register(request)

@router.post("/onboarding/login")
async def login(
    request: LoginRequest,
    service: OnboardingService = Depends(get_onboarding_service),
) -> LoginResponse:
    return service.login(request)