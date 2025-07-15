from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class TradeRequest(BaseModel):
    strategy: str
    capital: int
    tsl: int
    paper: bool

@app.get("/api/status")
def status():
    return {"status": "ok"}

@app.post("/api/trade")
def trade(data: TradeRequest):
    # replace with actual trade logic
    return {"status": "success", "message": "Trade executed", "data": data}

@app.get("/api/wallet")
def wallet():
    return {"status": "success", "broker": "Zerodha", "funds": 50000}

@app.get("/api/orders")
def orders():
    return {
        "status": "success",
        "broker": "Zerodha",
        "orders": ["Order 1", "Order 2"]
    }
