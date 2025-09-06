from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from main import agent, system_prompt

load_dotenv()

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
async def query_endpoint(request: QueryRequest):
    user_query = request.query
    prompt_text = f"system: {system_prompt}\nhuman: {user_query}"
    try:
        response = agent(prompt_text)
        return {"result": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"status": "ok"}
