from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from backend.services.securirty import get_current_user_id  # Session Security Guard
from backend.schema.github_agent import GitHubPushRequest
from backend.services.github_oauth import (
    get_github_login_url,
    exchange_code_for_token,
    get_github_connection_status,
)
from backend.services.github_service import push_to_github_repository

router = APIRouter(prefix="/auth", tags=["GitHub OAuth Authentication"])

@router.get("/github/login")
def github_login_endpoint(current_user_id: str = Depends(get_current_user_id)):
    """
    ENDPOINT 1: Frontend is route ko hit karega aur user safely 
    GitHub ke permission page par redirect ho jayega.
    """
    login_url = get_github_login_url(current_user_id)
    return {"status": "success", "redirect_url": login_url}


@router.get("/github/callback", response_class=HTMLResponse)
def github_callback_endpoint(code: str, state: str | None = None):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization denied or invalid temporary exchange token mapping."
        )

    if not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub state missing. Please start GitHub connect again."
        )

    exchange_code_for_token(temporary_code=code, user_id=state)

    return """
    <html>
      <body style="font-family: Arial; padding: 40px;">
        <h2>GitHub connected successfully ✅</h2>
        <p>You can close this tab and return to AI Powered Coding Assistant.</p>
      </body>
    </html>
    """


@router.get("/github/status")
def github_status_endpoint(current_user_id: str = Depends(get_current_user_id)):
    return get_github_connection_status(current_user_id)


@router.post("/github/push")
def github_push_endpoint(
    data: GitHubPushRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    return push_to_github_repository(
        user_id=current_user_id,
        analysis_id=data.analysis_id,
        repo_name=data.repo_name,
        private=data.is_private,
    )
