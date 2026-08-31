from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, get_password_hash, verify_password

# Yeh line boht important hai! Variable ka naam exact 'router' hona chahiye
router = APIRouter()

# Simple In-Memory Mock database testing ke liye
MOCK_USERS_DB = {
    "testuser": {
        "username": "testuser",
        "hashed_password": get_password_hash("password123"), 
        "user_id": "test_customer_123"
    }
}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT Token banana jisme User ID shamil ho
    access_token = create_access_token(data={"sub": user["username"], "user_id": user["user_id"]})
    return {"access_token": access_token, "token_type": "bearer"}