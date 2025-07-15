
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TradeRequest(BaseModel):
    strategy: str
    capital: float
    tsl: float
    paper: bool

@router.post("/trade")
async def execute_trade(req: TradeRequest):
    return {"status": "success", "message": "Trade executed", "data": req.dict()}
