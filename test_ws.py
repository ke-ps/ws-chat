"""Test WebSocket connection to various scenarios."""
import asyncio
import json
import os
from dotenv import load_dotenv
load_dotenv("backend/.env")

async def test_ws(room_id, email, display_name="", label=""):
    uri = f"ws://localhost:8005/ws/{room_id}?email={email}&displayName={display_name}"
    print(f"\n{'='*50}")
    print(f"Test: {label}")
    print(f"  URL: ws://localhost:8005/ws/{room_id}?email={email}&displayName={display_name}")
    try:
        import websockets
        async with websockets.connect(uri, close_timeout=5) as ws:
            print(f"  [CONNECTED] Handshake OK")
            # Try receiving a message (user_list broadcast)
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=3)
                data = json.loads(msg)
                print(f"  [RECEIVED] type={data.get('type')}, data={data}")
            except asyncio.TimeoutError:
                print(f"  [NO MESSAGE] No message received within 3s (might be no other users)")
            # Send a test message
            await ws.send(json.dumps({"id": "test-1", "content": "hello", "sender": email}))
            print(f"  [SENT] test message")
            # Clean close
            await ws.close()
            print(f"  [CLOSED] Clean disconnect")
    except Exception as e:
        print(f"  [FAILED] {type(e).__name__}: {e}")

async def main():
    # Test 1: Normal connection (valid room, valid email)
    await test_ws(room_id=1, email="test@test.com", display_name="Test", label="Normal connection")
    
    # Test 2: Room does not exist
    await test_ws(room_id=99999, email="test@test.com", display_name="Test", label="Non-existent room")
    
    # Test 3: Empty email
    await test_ws(room_id=1, email="", display_name="Test", label="Empty email")
    
    # Test 4: Missing displayName
    await test_ws(room_id=1, email="test@test.com", label="Missing displayName")

asyncio.run(main())
