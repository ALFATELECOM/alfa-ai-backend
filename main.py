
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend running"}

class LoginRequest(BaseModel):
    api_key: str
    api_secret: str
    token: str

@app.post("/login")
def login(data: LoginRequest):
    if data.api_key and data.api_secret and data.token:
        return {"status": "success", "message": "Zerodha login simulated"}
    raise HTTPException(status_code=400, detail="Invalid credentials")
