from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# Store connected clients
connected_clients = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Internet Calling App!"}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_clients[user_id] = websocket
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            print(f"Message from {user_id}: {data}")
            # Broadcast to all connected clients (example signaling)
            for client_id, client_ws in connected_clients.items():
                if client_id != user_id:
                    await client_ws.send_text(f"Message from {user_id}: {data}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        del connected_clients[user_id]
