from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, trading

app = FastAPI()

origins = [
    "https://alfa-ai-frontend.vercel.app",  # Update to your actual Vercel frontend URL
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(trading.router, prefix="/trade")

@app.get("/")
def root():
    return {"message": "Backend is live"}

@app.get("/status")
def status():
    return {"status": "ok"}