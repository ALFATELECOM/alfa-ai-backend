from fastapi import FastAPI
from routes import trade_routes, auth_routes

app = FastAPI()

app.include_router(trade_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def home():
    return {"message": "ALFA AI Backend running!"}
