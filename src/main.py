import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from src.logic import calculate_scorecard, Scorecard

app = FastAPI(title="Git Health Scorer - Static Mock Mode")

# 1. Setup Security (Defaulting to your devops secret)
API_KEY = os.getenv("INTERNAL_API_KEY", "devops-secret-123")

# 2. Define the Request Body
class ScanRequest(BaseModel):
    owner: str
    repo: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/scan", response_model=Scorecard)
async def api_scan(request: ScanRequest, x_api_key: str = Header(None)):
    # --- Security Layer ---
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized Access")