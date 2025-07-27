from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    symbol: str
    signal: str
    capital: float

@app.get("/status")
def get_status():
    return {"status": "ok"}

@app.post("/trade/order")
async def place_order(order: OrderRequest):
    return {
        "status": "Order placed",
        "symbol": order.symbol,
        "signal": order.signal,
        "capital": order.capital
    }