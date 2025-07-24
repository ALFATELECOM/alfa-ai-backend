from fastapi import APIRouter

router = APIRouter()

@router.get("/signals")
def get_signals():
    return {"signals": ["RELIANCE BUY", "HDFC SELL"]}

@router.post("/order")
def place_order(data: dict):
    return {"status": "order placed", "details": data}

@router.get("/portfolio")
def get_portfolio():
    return {
        "balance": 452850,
        "holdings": [
            {"symbol": "RELIANCE", "qty": 50, "ltp": 2485.5, "pnl": 1775},
            {"symbol": "TCS", "qty": 25, "ltp": 3695.75, "pnl": 394}
        ]
    }