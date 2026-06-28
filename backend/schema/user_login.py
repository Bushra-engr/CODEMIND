from pydantic import field_validator,Field,BaseModel

class UserLogin(BaseModel):
    username_or_email : str
    password:str
    