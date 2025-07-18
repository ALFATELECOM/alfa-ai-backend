
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()

class SignalResponse(BaseModel):
    symbol: str
    strategy: str
    action: str
    confidence: float
    timestamp: str

@app.get("/get-signal", response_model=SignalResponse)
def get_signal(symbol: str = "NIFTY"):
    strategies = ["RSI", "MACD", "Breakout"]
    actions = ["BUY", "SELL", "HOLD"]
    return SignalResponse(
        symbol=symbol,
        strategy=random.choice(strategies),
        action=random.choice(actions),
        confidence=round(random.uniform(0.7, 0.99), 2),
        timestamp=datetime.now().isoformat()
    )
    