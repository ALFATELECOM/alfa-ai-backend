from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    if req.email == "demo@trading.com" and req.password == "demo123":
        return {"token": "demo-token"}
    return {"error": "Invalid credentials"}