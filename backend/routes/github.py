from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse

from backend.schema.github_agent import GitHubPushRequest
from backend.services.github_oauth import (
    exchange_code_for_token,
    get_github_connection_status,
    get_github_login_url,
)
from backend.services.github_service import push_to_github_repository
from backend.services.securirty import get_current_user_id

router = APIRouter(prefix="/auth", tags=["GitHub OAuth Authentication"])
github_alias_router = APIRouter(prefix="/github", tags=["GitHub OAuth Authentication"])


@router.get("/github/login")
@github_alias_router.get("/login")
def github_login_endpoint(current_user_id: str = Depends(get_current_user_id)):
    login_url = get_github_login_url(current_user_id)
    return {"status": "success", "redirect_url": login_url}


@router.get("/github/connect")
@github_alias_router.get("/connect")
def github_connect_endpoint(current_user_id: str = Depends(get_current_user_id)):
    login_url = get_github_login_url(current_user_id)
    return {"status": "success", "redirect_url": login_url}


@router.get("/github/callback", response_class=HTMLResponse)
@github_alias_router.get("/callback", response_class=HTMLResponse)
def github_callback_endpoint(code: str, state: str | None = None):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub authorization code missing.",
        )

    if not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub OAuth state missing. Please connect GitHub again.",
        )

    exchange_code_for_token(temporary_code=code, user_id=state)

    return """
    <html>
      <head>
        <title>GitHub Connected</title>
      </head>
      <body style="font-family: Arial, sans-serif; padding: 40px; background: #f8fafc; color: #111827;">
        <div style="max-width: 560px; margin: 0 auto; background: white; border: 1px solid #e5e7eb; border-radius: 18px; padding: 28px;">
          <h2>GitHub connected successfully ✅</h2>
          <p>Your GitHub access has been saved for this account. You can close this tab and return to CodeMind.</p>
        </div>
      </body>
    </html>
    """


@router.get("/github/status")
@github_alias_router.get("/status")
def github_status_endpoint(current_user_id: str = Depends(get_current_user_id)):
    return get_github_connection_status(current_user_id)


@router.post("/github/push")
@github_alias_router.post("/push")
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
