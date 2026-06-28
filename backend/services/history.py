from backend.databases.models import AnalysisRun, User
from backend.schema.coderunresponse import CodeAnalysisResponse
from backend.databases.connection import SessionLocal
from fastapi import HTTPException,status

records = []
def get_user_history(user_id:str):
    
    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.id == user_id).first()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist ! Register first."
            )
        user_db_id = existing_user.id
        
        records = session.query(AnalysisRun).filter(
            AnalysisRun.user_id==user_db_id
        ).all()

        return records


def delete_user_analysis(user_id: str, analysis_id: str):
    with SessionLocal() as session:
        record = session.query(AnalysisRun).filter(
            AnalysisRun.id == analysis_id,
            AnalysisRun.user_id == user_id
        ).first()

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Selected analysis record not found."
            )

        session.delete(record)
        session.commit()

        return {"success": True, "message": "Analysis record deleted successfully."}


def clear_user_history(user_id: str):
    with SessionLocal() as session:
        deleted_count = session.query(AnalysisRun).filter(
            AnalysisRun.user_id == user_id
        ).delete(synchronize_session=False)
        session.commit()

        return {
            "success": True,
            "message": f"Cleared {deleted_count} analysis record(s)."
        }
