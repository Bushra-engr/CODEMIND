from fastapi import HTTPException, status
from backend.core import run_assistant
from backend.schema.coderunresponse import CodeAnalysisResponse
from backend.databases.models import AnalysisRun, User
from backend.databases.connection import SessionLocal


def code_analyze(
    project_name: str,
    code: str,
    language: str,
    github: bool,
    id: str
):
    # Verify user
    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.id == id).first()

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User context mapping failed! Register first."
            )

        user_db_id = existing_user.id

    try:
        # Run AI Assistant
        response = run_assistant(
            project_name=project_name,
            code=code,
            language=language,
            github_push=github
        )

        # Save analysis in database
        with SessionLocal() as session:
            new_code_data = AnalysisRun(
                user_id=user_db_id,
                project_name=project_name,
                original_code=code,
                language=language,
                github_push=github,
                review_report=response["analysis"]["review_report"],
                bugs_found=response["analysis"]["bugs_found"],
                fixed_code=response["code"]["fixed"],
                optimized_code=response["code"]["optimized"],
                explanation=response["output"]["explanation"],
                readme_content=response["output"]["github_readme_file"]
            )

            session.add(new_code_data)
            session.commit()

            # VERY IMPORTANT
            session.refresh(new_code_data)

        print("💾 Analysis report successfully mapped to Neon Postgres!")
        print("Analysis ID:", new_code_data.id)
        return CodeAnalysisResponse(
            analysis_id=str(new_code_data.id),   # <-- FIX

            success=True,
            message="Successfully inserted code data report",

            project_name=project_name,
            code=code,
            language=language,

            review_report=response["analysis"]["review_report"],
            bugs_found=response["analysis"]["bugs_found"],

            fixed_code=response["code"]["fixed"],
            optimized_code=response["code"]["optimized"],

            github_push=github,

            explanation=response["output"]["explanation"],

            documentation=response["output"].get(
                "documentation",
                response["output"].get("github_readme_file", "")
            )
        )

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database or Assistant crash trace: {str(e)}"
        )