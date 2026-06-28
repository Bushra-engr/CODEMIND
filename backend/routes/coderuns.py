from fastapi import APIRouter,HTTPException,Response,status,Depends
from backend.services.securirty import get_current_user_id
from backend.schema.coderuncreate import CodeRunCreate
from backend.services.coderunss import code_analyze

router = APIRouter(
    prefix="/assistant",
    tags=["assistant"]
)


@router.post("/analyze")
def userAnalyzeCode(
    data:CodeRunCreate,
    current_user_id:str=Depends(get_current_user_id)
):
    response = code_analyze(
        project_name=data.project_name,
        code = data.code,
        language= data.language,
        github = data.github,
        id =current_user_id
    )
    
    return response
    
    
    