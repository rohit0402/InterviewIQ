from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str

    password: str = Field(
        min_length=8,
        max_length=128,
    )