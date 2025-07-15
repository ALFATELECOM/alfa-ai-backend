
from fastapi import APIRouter

router = APIRouter()

@router.get("/orders")
async def get_orders(broker: str):
    return {"status": "success", "broker": broker, "orders": ["Order 1", "Order 2"]}
