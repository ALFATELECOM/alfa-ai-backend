
from fastapi import APIRouter

router = APIRouter()

@router.get("/funds")
async def get_funds(broker: str):
    return {"status": "success", "broker": broker, "funds": 50000}
