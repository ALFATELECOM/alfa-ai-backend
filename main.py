
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import trade, funds, orders

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trade.router)
app.include_router(funds.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "ALFA AI Backend Live"}
