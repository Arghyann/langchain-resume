from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Use service role key for backend validation

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

security = HTTPBearer()

# Whitelisted users
ALLOWED_USERS = {
    "aryanmane2016@gmail.com",
    "seconduser@gmail.com",
    "thirduser@gmail.com",
}

def get_current_user(credentials=Depends(security)):
    token = credentials.credentials

    # Validate token with Supabase
    try:
        user_resp = supabase.auth.get_user(token)
        user = user_resp.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not user or not user.email:
        raise HTTPException(status_code=401, detail="Invalid token: no email found")

    if user.email not in ALLOWED_USERS:
        raise HTTPException(status_code=403, detail="User not allowed")

    return user  # contains user info like email, id, etc