from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Dict, List

app = FastAPI()

# Serve the frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

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

# Room-based WebSocket functionality
rooms: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/{room_id}/{user_id}")
async def room_websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(websocket)

    # Notify others in the room about the new connection
    for ws in rooms[room_id]:
        if ws != websocket:
            await ws.send_text(f"{user_id} joined the room.")

    try:
        typing_status = False  # Track if the user is typing
        while True:
            data = await websocket.receive_text()

            # Handle typing events
            if data == "typing start":
                if not typing_status:
                    for ws in rooms[room_id]:
                        if ws != websocket:
                            await ws.send_text(f"{user_id} is typing...")
                    typing_status = True
                continue
            elif data == "typing stop":
                if typing_status:
                    for ws in rooms[room_id]:
                        if ws != websocket:
                            await ws.send_text(f"{user_id} stopped typing.")
                    typing_status = False
                continue

            # Broadcast the actual message to everyone in the room
            print(f"Message from {user_id} in room {room_id}: {data}")
            for ws in rooms[room_id]:
                await ws.send_text(f"{user_id}: {data}")
    except WebSocketDisconnect:
        rooms[room_id].remove(websocket)
        print(f"User {user_id} disconnected from room {room_id}")

        # Notify others in the room about the disconnection
        for ws in rooms[room_id]:
            await ws.send_text(f"{user_id} left the room.")

        # Cleanup the room if it's empty
        if not rooms[room_id]:
            del rooms[room_id]
