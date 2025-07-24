from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import asyncio
import os

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store WebSocket connections
connections = []

@app.get("/")
async def root():
    return {
        "status": "healthy", 
        "service": "ALFA Trading Backend", 
        "logs": "streaming",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def status():
    return {
        "status": "running",
        "log_connections": len(connections),
        "timestamp": datetime.now().isoformat()
    }

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    
    # Send welcome message
    welcome = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": "🎉 Connected to ALFA Trading Backend",
        "module": "websocket",
        "function": "connect",
        "line": 0
    }
    await websocket.send_text(json.dumps(welcome))
    
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                pong = {
                    "timestamp": datetime.now().isoformat(),
                    "level": "INFO", 
                    "message": "pong - Backend connection active",
                    "module": "websocket",
                    "function": "keepalive",
                    "line": 0
                }
                await websocket.send_text(json.dumps(pong))
    except WebSocketDisconnect:
        connections.remove(websocket)

@app.post("/auth/login")
async def login(credentials: dict):
    email = credentials.get("email")
    password = credentials.get("password")
    
    # Broadcast login attempt to all connected clients
    log_msg = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": f"🔐 Login attempt for user: {email}",
        "module": "auth",
        "function": "login",
        "line": 1
    }
    await broadcast_log(log_msg)
    
    # Demo auth
    if email == "demo@trading.com" and password == "demo123":
        success_msg = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": f"✅ Successful login for: {email}",
            "module": "auth", 
            "function": "login",
            "line": 2
        }
        await broadcast_log(success_msg)
        
        return {
            "success": True,
            "user": {"email": email, "name": "Demo Trader"}
        }
    else:
        fail_msg = {
            "timestamp": datetime.now().isoformat(),
            "level": "WARNING",
            "message": f"❌ Failed login attempt for: {email}",
            "module": "auth",
            "function": "login", 
            "line": 3
        }
        await broadcast_log(fail_msg)
        
        return {"success": False, "message": "Invalid credentials"}

@app.post("/trade/order")
async def place_order(order: dict):
    symbol = order.get("symbol", "UNKNOWN")
    action = order.get("action", "UNKNOWN")
    quantity = order.get("quantity", 1)
    price = order.get("price", 0)
    
    # Broadcast order to all connected clients
    order_msg = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": f"📋 New {action} order: {quantity} {symbol} @ ₹{price}",
        "module": "trading",
        "function": "place_order",
        "line": 1
    }
    await broadcast_log(order_msg)
    
    # Simulate processing
    await asyncio.sleep(1)
    
    order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    success_msg = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": f"✅ Order executed successfully - ID: {order_id}",
        "module": "trading",
        "function": "place_order",
        "line": 2
    }
    await broadcast_log(success_msg)
    
    return {
        "success": True,
        "order_id": order_id,
        "status": "executed",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trade/portfolio")
async def get_portfolio():
    portfolio_msg = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": "💼 Fetching portfolio data",
        "module": "trading",
        "function": "get_portfolio",
        "line": 1
    }
    await broadcast_log(portfolio_msg)
    
    portfolio = {
        "total_value": 454870.02,
        "daily_pnl": 8750,
        "positions": [
            {"symbol": "RELIANCE", "quantity": 50, "avg_price": 2450.00, "current_price": 2485.50},
            {"symbol": "TCS", "quantity": 25, "avg_price": 3680.00, "current_price": 3695.75}
        ]
    }
    
    value_msg = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "message": f"💰 Portfolio value: ₹{portfolio['total_value']:,.2f}",
        "module": "trading",
        "function": "get_portfolio", 
        "line": 2
    }
    await broadcast_log(value_msg)
    
    return portfolio

async def broadcast_log(log_entry):
    """Broadcast log to all connected WebSocket clients"""
    if connections:
        disconnected = []
        for websocket in connections:
            try:
                await websocket.send_text(json.dumps(log_entry))
            except:
                disconnected.append(websocket)
        
        # Remove disconnected clients
        for ws in disconnected:
            if ws in connections:
                connections.remove(ws)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
