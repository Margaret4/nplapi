from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from app.core.firebase import verify_token

router = APIRouter()

def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Dependency to verify the Firebase ID token from the Authorization header.
    Expects format: 'Bearer <token>'
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
    token = parts[1]
    
    try:
        decoded_token = verify_token(token)
        return decoded_token
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    A protected endpoint that returns the current authenticated user's information
    extracted from the Firebase token.
    """
    return {"user_id": current_user.get("uid"), "email": current_user.get("email")}
