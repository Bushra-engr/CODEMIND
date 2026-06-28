import os
import requests
from fastapi import HTTPException, status
from urllib.parse import urlencode
from backend.databases.connection import SessionLocal
from backend.databases.models import User

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")


def get_github_login_url(user_id: str) -> str:
    query = urlencode(
        {
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": GITHUB_REDIRECT_URI,
            "scope": "repo",
            "state": user_id,
        }
    )
    return f"https://github.com/login/oauth/authorize?{query}"



def exchange_code_for_token(temporary_code: str, user_id: str):
    """
    GitHub se temporary code lekar use Client Secret ke sath mix karta hai,
    permanent access_token nikalta hai aur Neon Database me save karta hai.
    """
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": temporary_code
    }
    headers = {"Accept": "application/json"}
    
    # GitHub ke token endpoint par raw handshake POST request mari
    token_url = "https://github.com/login/oauth/access_token"
    response = requests.post(token_url, data=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="GitHub OAuth core authentication handshake timed out."
        )
        
    token_data = response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth Authorization Failed: {token_data.get('error_description', 'Invalid Code')}"
        )
        
    # --- SAVE TO NEON POSTGRES DATABASE ---
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User context mismatch inside session storage.")
            
        user.github_token = access_token  # Token securely mapped to user profile row
        session.commit()
        
    return {"success": True, "message": "GitHub account successfully linked with automated session access token!"}


def get_github_connection_status(user_id: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        return {
            "connected": bool(user.github_token),
            "message": "GitHub connected." if user.github_token else "GitHub not connected.",
        }
