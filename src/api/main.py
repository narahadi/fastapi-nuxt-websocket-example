from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from typing import Dict
import jwt
import logging
from datetime import datetime, timedelta
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
BACKGROUND_JOB_WAIT_TIME = 5

api_key_header = APIKeyHeader(name="Authorization")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.debug(f"User {user_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        del self.active_connections[user_id]
        logger.debug(f"User {user_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, user_id: str):
        print('sending message')
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
            logger.debug(f"Message sent to user {user_id}: {message}")
        else:
            logger.warning(f"Attempted to send message to non-existent user {user_id}")

manager = ConnectionManager()

def create_token(user_id: str):
    expires_delta = timedelta(hours=1)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": user_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str = Depends(api_key_header)):
    try:
        used_token = token
        if token and token.startswith("Bearer "):
            used_token = token[7:]
        payload = jwt.decode(used_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            return
        
        user_id = decode_token(token)
        await manager.connect(websocket, user_id)
        
        try:
            while True:
                data = await websocket.receive_text()
                logger.debug(f"Received message from user {user_id}: {data}")
                await manager.send_personal_message(f"You wrote: {data}", user_id)
        except WebSocketDisconnect:
            manager.disconnect(user_id)
    except HTTPException:
        await websocket.close(code=1008)

async def background_job(user_id: str):
    logger.info(f"Starting background job for user {user_id}")
    await asyncio.sleep(BACKGROUND_JOB_WAIT_TIME)
    await manager.send_personal_message(f"Background job completed for {user_id} after {BACKGROUND_JOB_WAIT_TIME} seconds!", user_id)
    logger.info(f"Completed background job for user {user_id}")

@app.post("/start-job")
async def start_job(user_id: str = Depends(decode_token)):
    logger.debug(f"Received job start request for user {user_id}")
    if user_id not in manager.active_connections:
        logger.warning(f"Job start request rejected: User {user_id} not connected")
        raise HTTPException(status_code=404, detail="User not connected")
    asyncio.create_task(background_job(user_id))
    logger.info(f"Job started for user {user_id}")
    return {"message": f"Job started for user {user_id}"}

from pydantic import BaseModel
class LoginRequest(BaseModel):
    username: str

@app.post("/login")
async def login(request: LoginRequest):
    token = create_token(request.username)
    return {"access_token": token, "token_type": "bearer"}