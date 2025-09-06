from fastapi import FastAPI, HTTPException, Depends,Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from main import agent, system_prompt
from auth import get_current_user

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Allow CORS for all origins (for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_endpoint(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    user_query = request.query
    prompt_text = f"system: {system_prompt}\nhuman: {user_query}"
    try:
        response = agent(prompt_text)
        return {"result": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root(current_user: dict = Depends(get_current_user)):
    print("Current user:", current_user)
    return {"status": "ok", "user": current_user}


