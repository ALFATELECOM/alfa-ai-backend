from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def read_status():
    return {"status": "OK"}

@app.get("/get-signal")
def get_signal():
    return {"signal": "BUY", "confidence": 0.82}

@app.get("/get-price")
def get_price(symbol: str = Query(...)):
    dummy_prices = {
        "WIPRO": 488.3,
        "HDFC": 1620.5,
        "RELIANCE": 2840.0
    }
    price = dummy_prices.get(symbol.upper(), None)
    if price:
        return {"symbol": symbol.upper(), "price": price}
    return JSONResponse(status_code=404, content={"error": "Symbol not found"})
