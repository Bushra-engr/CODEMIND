from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: int = Field(
        gt=0,
        description="Unique user id"
    )

    username: str = Field(
        min_length=3,
        max_length=20,
        description="Username"
    )

    email: EmailStr

    is_active: bool = True

    model_config = {
        "from_attributes": True
    }