# ALFA Backend

## Features
- FastAPI-based trading backend
- Supports login, signal fetch, paper trade order, and portfolio API
- CORS enabled for Vercel frontend

## Deploy to Render
1. Upload to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add environment variables from `.env.example`

## API Routes
- `GET /` - Health Check
- `GET /status` - Live status
- `POST /auth/login` - Login with demo credentials
- `GET /trade/signals` - Sample signals
- `POST /trade/order` - Place mock order
- `GET /trade/portfolio` - Get portfolio