from fastapi import APIRouter,HTTPException,Response,status
from backend.schema.user_register import UserRegister
from backend.services.registeruser import insert_user

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/register")
def UserRegister(data:UserRegister):
    
    response = insert_user(data)
        
    if response["success"]==True:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response["message"]
        )
    