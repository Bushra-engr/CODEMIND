import bcrypt  
from backend.schema.user_register import UserRegister
from backend.databases.connection import SessionLocal
from backend.databases.models import User

def hash_password(password: str) -> str:
    # Convert string to bytes, hash it, and decode it back to a clean string
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def insert_user(user_data: UserRegister):
    with SessionLocal() as session:
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.email == user_data.email) | (User.username == user_data.username)
            ).first()
            
            if existing_user:
                return {"success": False, "message": "Username or Email already registered"}

            # Securely hash using raw bcrypt
            hashed_pass = hash_password(user_data.password)
            
            # Map parameters explicitly to your SQLAlchemy table
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                password=hashed_pass  
            )
            
            session.add(new_user)
            session.commit()
            return {"success": True, "message": f"Successfully inserted: {new_user.username}"}

        except Exception as e:
            session.rollback()
            return {"success": False, "message": str(e)}

        
if __name__ == "__main__":
    mock_pydantic_input = UserRegister(
        username="alice",
        email = "alice123@gmail.com",
        password = "alice123hello"
    )
    
    print(insert_user(mock_pydantic_input))