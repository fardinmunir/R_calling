from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for health check
@app.get("/")
def read_root():
    return {"status": "OK"}

# Existing WebSocket endpoint (Optional: Keep or replace)
connected_clients = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_clients[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from {user_id}: {data}")
            for client_id, client_ws in connected_clients.items():
                if client_id != user_id:
                    await client_ws.send_text(f"Message from {user_id}: {data}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        del connected_clients[user_id]

# New WebSocket endpoint for room-based functionality
rooms = {}

@app.websocket("/ws/{room_id}/{user_id}")
async def room_websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from {user_id} in room {room_id}: {data}")
            for ws in rooms[room_id]:
                await ws.send_text(f"{user_id}: {data}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected from room {room_id}")
        rooms[room_id].remove(websocket)
