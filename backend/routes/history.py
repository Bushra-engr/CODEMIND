from fastapi import APIRouter,HTTPException,Depends,status
from backend.services.history import get_user_history, delete_user_analysis, clear_user_history
from backend.services.securirty import get_current_user_id

router = APIRouter(
    prefix="/assistant",
    tags=["assistant"]
)

@router.get("/me")
def fetch_user_history(user_uuid:str = Depends(get_current_user_id)):
    
    response = get_user_history(user_id=user_uuid)
    
    return response


@router.delete("/history/{analysis_id}")
def delete_specific_history(
    analysis_id: str,
    user_uuid: str = Depends(get_current_user_id)
):
    return delete_user_analysis(user_id=user_uuid, analysis_id=analysis_id)


@router.delete("/history")
def clear_history(user_uuid: str = Depends(get_current_user_id)):
    return clear_user_history(user_id=user_uuid)
