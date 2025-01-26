from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    name : str
    email : EmailStr
    password : str

class LoginUser(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None