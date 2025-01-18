import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/123"  # Local testing URL
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(f"Response from server: {response}")

asyncio.run(test_websocket())
