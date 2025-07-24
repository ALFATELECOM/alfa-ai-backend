from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
import json
from datetime import datetime
from typing import List
import uvicorn
from logging.handlers import RotatingFileHandler
import os

app = FastAPI(title="ALFA Trading Backend")

# CORS setup for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://alfa-ai-trading-dashboard.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced logging setup with WebSocket streaming
class WebSocketLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.connections: List[WebSocket] = []
    
    def add_connection(self, websocket: WebSocket):
        self.connections.append(websocket)
    
    def remove_connection(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)
    
    def emit(self, record):
        if self.connections:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": record.levelname,
                "message": self.format(record),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            
            # Send to all connected WebSocket clients
            for connection in self.connections.copy():
                try:
                    asyncio.create_task(
                        connection.send_text(json.dumps(log_entry))
                    )
                except:
                    self.remove_connection(connection)

# Create global WebSocket handler
websocket_handler = WebSocketLogHandler()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add file handler for persistence
file_handler = RotatingFileHandler('trading_app.log', maxBytes=10485760, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Add WebSocket handler for real-time streaming
websocket_handler.setFormatter(logging.Formatter('%(message)s'))

# Get logger and add handlers
logger = logging.getLogger("TradingApp")
logger.addHandler(file_handler)
logger.addHandler(websocket_handler)
logger.setLevel(logging.INFO)

# WebSocket endpoint for log streaming
@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    websocket_handler.add_connection(websocket)
    
    logger.info(f"🔌 New client connected to log stream")
    
    try:
        # Send recent logs on connection
        await send_recent_logs(websocket)
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "level": "INFO",
                    "message": "pong - connection active",
                    "module": "websocket",
                    "function": "keepalive",
                    "line": 0
                }))
                
    except WebSocketDisconnect:
        websocket_handler.remove_connection(websocket)
        logger.info(f"🔌 Client disconnected from log stream")

async def send_recent_logs(websocket: WebSocket):
    """Send recent logs to newly connected client"""
    try:
        if os.path.exists('trading_app.log'):
            with open('trading_app.log', 'r') as f:
                lines = f.readlines()[-50:]  # Last 50 lines
                
            for line in lines:
                if line.strip():
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "level": "INFO",
                        "message": line.strip(),
                        "module": "historical",
                        "function": "startup",
                        "line": 0
                    }
                    await websocket.send_text(json.dumps(log_entry))
    except Exception as e:
        logger.error(f"Error sending recent logs: {e}")

# Health check endpoint
@app.get("/")
async def health_check():
    logger.info("🏥 Health check requested")
    return {"status": "healthy", "service": "ALFA Trading Backend", "logs": "streaming"}

# Status endpoint
@app.get("/status")
async def get_status():
    active_connections = len(websocket_handler.connections)
    logger.info(f"📊 Status check - {active_connections} active log connections")
    return {
        "status": "running",
        "log_connections": active_connections,
        "timestamp": datetime.now().isoformat()
    }

# Import your existing routes
try:
    from routes import auth, trading  # Adjust based on your structure
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(trading.router, prefix="/trade", tags=["Trading"])
    logger.info("✅ Existing routes imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Could not import existing routes: {e}")
    
    # Fallback demo endpoints
    @app.post("/auth/login")
    async def login(credentials: dict):
        email = credentials.get("email")
        logger.info(f"🔐 Login attempt for user: {email}")
        
        demo_users = {
            "demo@trading.com": "demo123",
            "trader@example.com": "trader123"
        }
        
        if email in demo_users and credentials.get("password") == demo_users[email]:
            logger.info(f"✅ Successful login for: {email}")
            return {"success": True, "user": {"email": email, "name": "Demo Trader"}}
        else:
            logger.warning(f"❌ Failed login attempt for: {email}")
            return {"success": False, "message": "Invalid credentials"}

    @app.get("/trade/signals")
    async def get_signals():
        logger.info("📡 Fetching live trading signals")
        
        signals = [
            {
                "symbol": "RELIANCE",
                "action": "BUY", 
                "price": 2485.50,
                "confidence": 92,
                "timestamp": datetime.now().isoformat()
            },
            {
                "symbol": "TCS",
                "action": "SELL",
                "price": 3695.75,
                "confidence": 88,
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        logger.info(f"📊 Generated {len(signals)} trading signals")
        return {"signals": signals}

    @app.post("/trade/order")
    async def place_order(order: dict):
        symbol = order.get("symbol")
        action = order.get("action")
        quantity = order.get("quantity")
        price = order.get("price")
        
        logger.info(f"📋 New {action} order: {quantity} {symbol} @ ₹{price}")
        
        # Simulate order processing
        await asyncio.sleep(1)
        
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"✅ Order executed successfully - ID: {order_id}")
        
        return {
            "success": True,
            "order_id": order_id,
            "status": "executed",
            "timestamp": datetime.now().isoformat()
        }

    @app.get("/trade/portfolio")
    async def get_portfolio():
        logger.info("💼 Fetching portfolio data")
        
        portfolio = {
            "total_value": 454870.02,
            "daily_pnl": 8750,
            "positions": [
                {"symbol": "RELIANCE", "quantity": 50, "avg_price": 2450.00, "current_price": 2485.50},
                {"symbol": "TCS", "quantity": 25, "avg_price": 3680.00, "current_price": 3695.75}
            ]
        }
        
        logger.info(f"💰 Portfolio value: ₹{portfolio['total_value']:,.2f}")
        return portfolio

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return {"error": "Internal server error", "message": str(exc)}

if __name__ == "__main__":
    logger.info("🚀 Starting ALFA Trading Backend Server")
    logger.info("📡 WebSocket log streaming enabled at /ws/logs")
    logger.info("🌐 CORS configured for Vercel frontend")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 10000)),
        log_level="info"
    )
