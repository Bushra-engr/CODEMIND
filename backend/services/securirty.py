import jwt
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
from fastapi.security import APIKeyHeader
from backend.schema.tokendata import TokenData
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=1)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_id(token: str = Depends(api_key_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing ! first register / login."
        )
    
    try:
        # Agar token me 'Bearer ' text likha ho toh use clean karo
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uuid: str = payload.get("sub")
        
        if user_uuid is None or user_uuid == "User.id": # Purana bug control check
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token data format"
            )
        
        return user_uuid
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials / Token Expired"
        )
