import bcrypt
from backend.databases.connection import SessionLocal
from backend.databases.models import User

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Ye function plain password ko Neon database ke secure hashed password se verify karta hai.
    """
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def authenticate_user(username_or_email: str, plain_pass: str):
    """
    Neon Postgres me user account search karne aur credentials check karne ka main logic function.
    """
    with SessionLocal() as session:
        try:
            
            user = session.query(User).filter(
                (User.email == username_or_email) | (User.username == username_or_email)
            ).first()
            
           
            if not user:
                return {
                    "success": False,
                    "message": "User does not exist with this username or email!"
                }
            
            is_password_correct = verify_password(plain_pass, user.password)
            
            if not is_password_correct:
                return {
                    "success": False,
                    "message": "Invalid password"
                }

            return {
                "success": True,
                "message": f"Welcome back {user.username}!",
                "user_id": str(user.id)  
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Internal database fetch error: {str(e)}"
            }


# --- Script Level Terminal Automated Mock Test Block ---
if __name__ == "__main__":
    print("--- TESTING LOGIN AUTHENTICATION SERVICE ---")
    
    # Apne Neon DB ke kisi active user credentials ke hisab se change karke test kar sakte hain:
    print(authenticate_user("bushra", "bushra123"))
    print(authenticate_user("alice", "123"))
