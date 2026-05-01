from pydantic import BaseModel

class RegisterResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    message: str