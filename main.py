from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for all origins (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class OrderRequest(BaseModel):
    symbol: str
    signal: str
    capital: float

@app.get("/")
def home():
    return {"status": "OK"}

@app.get("/status")
def get_status():
    return {"status": "OK"}

@app.get("/get-signal")
def get_signal():
    return {"strategy": "Momentum", "action": "BUY"}

@app.get("/get-price")
def get_price(symbol: str = Query(...)):
    prices = {
        "WIPRO": 489.4,
        "HDFC": 1621.2,
        "RELIANCE": 2842.8
    }
    price = prices.get(symbol.upper(), None)
    if price:
        return {"symbol": symbol.upper(), "price": price}
    return JSONResponse(status_code=404, content={"error": "Symbol not found"})

@app.post("/trade/order")
async def place_order(order: OrderRequest):
    # Log the received order for debug
    print("Received Order:", order.dict())
    return {"message": "Order Placed", "data": order.dict()}
