from fastapi import APIRouter,HTTPException,Response,status
from backend.schema.user_login import UserLogin
from backend.services.loginuser import authenticate_user
from backend.schema.tokenaccess import TokenResponse
from backend.services.securirty import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/login",response_model = TokenResponse)
def UserLogin(data:UserLogin):
    
    response = authenticate_user(
        username_or_email=data.username_or_email,
        plain_pass=data.password
    )
        
    if response["success"]==True:
        user_uuid = response["user_id"]
        generated_token =  create_access_token(user_id=user_uuid)
        return {
            "access_token":generated_token,
            "token_type":"bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )
    