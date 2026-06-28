from typing import Literal
from pydantic import BaseModel,Field

class TokenResponse(BaseModel):
    access_token : str = Field(
        min_length=50,
        description="JWT ACCESS TOKEN"
    )
    
    token_type : Literal["bearer"] = "bearer"