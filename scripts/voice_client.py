#!/usr/bin/env python3
"""cantalk voice client — record mic → send to cantalk → play response.

Usage: python scripts/voice_client.py
"""

import asyncio
import json
import sys
import base64
import struct
import websockets

import sounddevice as sd
import numpy as np

WS_URL = "ws://127.0.0.1:8765/v1/realtime"
SAMPLE_RATE = 16000
CHANNELS = 1
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 1.5  # seconds of silence before sending


def record_until_silence() -> np.ndarray:
    """Record audio until user stops speaking (silence detection)."""
    print("🎤 講野啦... (安靜 1.5 秒就會 send)", flush=True)

    buffer = []
    silent_frames = 0
    frames_needed = int(SILENCE_DURATION * SAMPLE_RATE / 1024)

    def callback(indata, frames, time_info, status):
        nonlocal silent_frames
        buffer.append(indata.copy())
        volume = np.abs(indata).mean()
        if volume < SILENCE_THRESHOLD:
            silent_frames += 1
        else:
            silent_frames = 0
        if silent_frames > frames_needed:
            raise sd.CallbackStop()

    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=CHANNELS,
        callback=callback, blocksize=1024,
        dtype="float32"
    ):
        try:
            while True:
                sd.sleep(100)
        except sd.CallbackStop:
            pass

    if not buffer:
        return np.array([], dtype=np.float32)

    audio = np.concatenate(buffer).flatten()
    # Trim trailing silence
    non_silent = np.where(np.abs(audio) > SILENCE_THRESHOLD)[0]
    if len(non_silent) > 0:
        audio = audio[: non_silent[-1] + int(0.3 * SAMPLE_RATE)]
    return audio


def encode_pcm16(audio: np.ndarray) -> str:
    """Convert float32 audio to base64 PCM16."""
    int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    return base64.b64encode(int16.tobytes()).decode()


def play_audio(audio: np.ndarray):
    """Play audio through speakers."""
    sd.play(audio, SAMPLE_RATE)
    sd.wait()


async def main():
    print("🔗 連接緊 cantalk...", flush=True)

    async with websockets.connect(WS_URL) as ws:
        print("✅ 已連接！\n", flush=True)

        while True:
            # Record
            audio = record_until_silence()
            if len(audio) < SAMPLE_RATE * 0.3:
                print("⏭️  太短，skip\n", flush=True)
                continue

            duration = len(audio) / SAMPLE_RATE
            print(f"📤 Send {duration:.1f}s 音頻...", flush=True)

            # Send audio
            chunk_size = SAMPLE_RATE // 4  # 0.25s chunks
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i : i + chunk_size]
                b64 = encode_pcm16(chunk)
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": b64
                }))

            # Commit and request response
            await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
            await ws.send(json.dumps({
                "type": "response.create",
                "response": {"modalities": ["text", "audio"]}
            }))

            # Receive response
            print("🤔 諗緊...", end=" ", flush=True)
            text_response = ""
            audio_chunks = []

            async for msg in ws:
                event = json.loads(msg)
                etype = event.get("type", "")

                if etype == "response.output_audio_transcript.done":
                    text_response = event.get("transcript", "")
                    print(f"\n📝 {text_response}", flush=True)

                elif etype == "response.output_audio.delta":
                    delta = event.get("delta", "")
                    if delta:
                        try:
                            pcm = base64.b64decode(delta)
                            samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32767.0
                            audio_chunks.append(samples)
                        except Exception:
                            pass

                elif etype == "response.done":
                    break

                elif etype == "error":
                    print(f"\n❌ {event.get('error', event)}", flush=True)
                    break

            # Play audio response
            if audio_chunks:
                response_audio = np.concatenate(audio_chunks)
                dur = len(response_audio) / SAMPLE_RATE
                print(f"🔊 播放 {dur:.1f}s 回應...", flush=True)
                play_audio(response_audio)
            elif text_response:
                print("🔇 (no audio)", flush=True)

            print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bye!")
