from fastapi import APIRouter, Request
import os

router = APIRouter()

@router.post("/trade")
def execute_trade(request: Request):
    return {
        "status": "success",
        "message": "Trade executed",
        "data": {
            "strategy": "Breakout Strategy",
            "capital": os.getenv("CAPITAL_PER_TRADE", 500),
            "tsl": "1%",
            "paper": True
        }
    }

@router.get("/funds")
def get_funds(broker: str = "Zerodha"):
    return {"status": "success", "broker": broker, "funds": 50000}

@router.get("/orders")
def get_orders(broker: str = "Zerodha"):
    return {"status": "success", "broker": broker, "orders": ["Order 1", "Order 2"]}
