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

# WebSocket endpoint
connected_clients = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_clients[user_id] = websocket
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            print(f"Message from {user_id}: {data}")
            # Broadcast to all connected clients
            for client_id, client_ws in connected_clients.items():
                if client_id != user_id:
                    await client_ws.send_text(f"Message from {user_id}: {data}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        del connected_clients[user_id]
