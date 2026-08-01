#!/usr/bin/env python3
"""Quick test client for cantalk WebSocket server.

Sends a text-to-speech test via the OpenAI Realtime API.
"""
import asyncio
import json
import websockets
import base64
import wave
import io

WS_URL = "ws://192.168.1.59:8765/v1/realtime"


async def main():
    async with websockets.connect(WS_URL) as ws:
        # Send session update with OpenAI Realtime format
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": "你係 Lucille，講廣東話。",
                "voice": "alloy",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": None,
            }
        }))

        print("✅ Connected to cantalk")
        print("Send a message (type 'quit' to exit):")

        while True:
            try:
                text = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            except (EOFError, KeyboardInterrupt):
                break

            if text.lower() in ("quit", "exit", "q"):
                break

            if not text.strip():
                continue

            # Send text message
            await ws.send(json.dumps({
                "type": "conversation.item.create",
                "item": {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": text}]
                }
            }))

            # Request response
            await ws.send(json.dumps({
                "type": "response.create",
                "response": {"modalities": ["text"]}
            }))

            # Read response
            print("Lucille: ", end="", flush=True)
            async for msg in ws:
                event = json.loads(msg)
                etype = event.get("type", "")

                if etype == "response.text.delta":
                    print(event["delta"], end="", flush=True)
                elif etype == "response.text.done":
                    print()
                    break
                elif etype == "error":
                    print(f"\n❌ {event.get('error', event)}")
                    break

        print("\n👋 Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
