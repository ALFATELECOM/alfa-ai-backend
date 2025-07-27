from fastapi import APIRouter

router = APIRouter()


@router.get("/signals")
def get_signals():
    # Replace with more signals as needed; demo for now
    return {
        "signals": [
            {"time": "14:32:15", "symbol": "TCS", "signal": "Buy Signal", "type": "Technical", "confidence": 89, "action": "BUY"},
            {"time": "14:31:00", "symbol": "RELIANCE", "signal": "Sell Signal", "type": "Technical", "confidence": 75, "action": "SELL"}
        ]
    }


@router.post("/order")
def place_order(data: dict):
    # Here you can add logic to record order history if needed
    return {"status": "order placed", "details": data}


@router.get("/portfolio")
def get_portfolio():
    return {
        "balance": 452850,
        "available_cash": 125000,
        "pnl_today": 18340,
        "holdings": [
            {"symbol": "RELIANCE", "qty": 50, "avg_price": 2450, "ltp": 2485, "market_value": 124250, "day_pnl": 1750, "total_pnl": 8900, "weight": 27.4},
            {"symbol": "TCS", "qty": 25, "avg_price": 3680, "ltp": 3695.75, "market_value": 92394, "day_pnl": 375, "total_pnl": 4500, "weight": 18.1},
            {"symbol": "INFY", "qty": 40, "avg_price": 1420, "ltp": 1435, "market_value": 57400, "day_pnl": 600, "total_pnl": 2140, "weight": 12.9},
        ],
    }
