from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from trading import router as trading_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(trading_router, prefix="/trade")

@app.get("/")
def root():
    return {"status": "OK"}

@app.get("/status")
def status():
    return {"live": True}



@app.get("/get-signal")
def get_signal():
    return {"strategy": "Momentum", "action": "BUY"}

@app.get("/get-price")
def get_price(symbol: str = Query(...)):
    dummy_prices = {
        "WIPRO": 492.5,
        "RELIANCE": 2841.2,
        "BANKNIFTY": 49720.0
    }
    price = dummy_prices.get(symbol.upper(), 0.0)
    return {"symbol": symbol, "price": price}
