import asyncio
import websockets

async def main():
    async with websockets.connect('ws://localhost:8765') as websocket:
        while True:
            payload = await websocket.recv()
            print(f"{payload}")

asyncio.get_event_loop() \
    .run_until_complete(main())
