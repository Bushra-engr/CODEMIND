import os
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from fastapi import HTTPException, status

from backend.databases.connection import SessionLocal
from backend.databases.models import User

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
DEFAULT_GITHUB_REDIRECT_URI = os.getenv(
    "GITHUB_REDIRECT_URI",
    "http://127.0.0.1:8000/auth/github/callback",
)


def _ensure_github_oauth_configured() -> None:
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "GitHub OAuth is not configured. Add GITHUB_CLIENT_ID and "
                "GITHUB_CLIENT_SECRET to your .env file."
            ),
        )


def get_github_login_url(user_id: str, redirect_uri: str | None = None) -> str:
    _ensure_github_oauth_configured()

    callback_url = redirect_uri or DEFAULT_GITHUB_REDIRECT_URI

    query = urlencode(
        {
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": callback_url,
            "scope": "repo",
            "state": user_id,
        }
    )
    return f"https://github.com/login/oauth/authorize?{query}"


def exchange_code_for_token(temporary_code: str, user_id: str, redirect_uri: str | None = None):
    _ensure_github_oauth_configured()

    callback_url = redirect_uri or DEFAULT_GITHUB_REDIRECT_URI

    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": temporary_code,
        "redirect_uri": callback_url,
    }
    headers = {"Accept": "application/json"}

    try:
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            data=payload,
            headers=headers,
            timeout=20,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub OAuth token exchange failed: {exc}",
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub OAuth token endpoint failed: {response.text}",
        )

    token_data = response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authorization failed: {token_data.get('error_description', token_data)}",
        )

    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User context mismatch while saving GitHub token.",
            )

        user.github_token = access_token
        session.commit()

    return {"success": True, "message": "GitHub account successfully connected."}


def get_github_connection_status(user_id: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        return {
            "connected": bool(user.github_token),
            "message": "GitHub connected." if user.github_token else "GitHub not connected.",
        }
