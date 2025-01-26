from fastapi import APIRouter, HTTPException
from Models.main import LoginUser, RegisterUser
from bson.objectid import ObjectId
from DB.main import get_collection
from datetime import datetime, timedelta
from jose import JWTError, jwt
from Utils.utils import settings

router = APIRouter()

collection = get_collection("users")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta):
    return create_access_token(data, expires_delta)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None

@router.post("/register", response_model=dict)
async def register_user(user: RegisterUser):
    user = collection.insert_one(user.dict())
    if not user:
        raise HTTPException(status_code=400, detail="User not created")
    return {
        "message": "User created successfully",
        "user_id": str(user.inserted_id)
    }

@router.post("/login", response_model = dict)
async def login_user(user: LoginUser):
    registeredUser = collection.find_one({"email": user.email})
    if not user:
        raise HTTPException(status_code=400, detail="User not Registered")
    if user.password != registeredUser["password"]:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    access_token = create_access_token(data = {"sub" : registeredUser["email"]}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {
        "message": "User logged in successfully",
        "access_token" : access_token,
    }