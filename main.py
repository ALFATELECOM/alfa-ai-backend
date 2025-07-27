from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from trading import router as trading_router
from auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "OK"}

@app.get("/status")
def status():
    return {"status": "OK"}

@app.get("/get-signal")
def get_signal():
    return {"signal": "BUY", "confidence": 0.85}

@app.get("/get-price")
def get_price(symbol: str = Query(...)):
    dummy_prices = {"WIPRO": 488.3, "HDFC": 1620.5}
    if symbol.upper() in dummy_prices:
        return {"symbol": symbol.upper(), "price": dummy_prices[symbol.upper()]}
    return JSONResponse(status_code=404, content={"error": "Symbol not found"})

# Mount routers (if you use trading.py and auth.py)
app.include_router(trading_router, prefix="/trade")
app.include_router(auth_router, prefix="/auth")
