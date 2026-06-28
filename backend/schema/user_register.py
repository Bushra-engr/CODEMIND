from pydantic import BaseModel,Field,EmailStr,field_validator


class UserRegister(BaseModel):
    username:str=Field(
        description="username",
        min_length=3,
        max_length=20
        )
    
    email:EmailStr
    
    password:str = Field(
        min_length=8,
        max_length=30
    )
    
    @field_validator("username")
    def validate_username(cls,value):
        
        if " " in value:
            raise ValueError(
                "Username cannot contain spaces."
            )
        return value
    
    @field_validator("password")
    def password_validator(cls,value):
        if len(value)<8:
            raise ValueError("Password is too short!")
        
        return value