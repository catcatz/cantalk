"""VoxCPM2 TTS adapter for speech-to-speech.

Wraps the VoxCPM2 HTTP API (http://127.0.0.1:8002) into a TTS engine
compatible with huggingface/speech-to-speech's TTS interface.
"""

import asyncio
from typing import AsyncIterator

import aiohttp


class VoxCPM2TTS:
    """TTS engine wrapping VoxCPM2 HTTP API."""

    def __init__(
        self,
        api_base: str = "http://127.0.0.1:8002/synthesize",
        speaker: str = "default",
        language: str = "zh",
    ):
        self.api_base = api_base.rstrip("/")
        self.speaker = speaker
        self.language = language

    async def synthesize(self, text: str) -> bytes:
        """Generate speech audio from text.

        Returns raw PCM audio bytes from VoxCPM2.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_base,
                json={
                    "text": text,
                    "speaker": self.speaker,
                    "language": self.language,
                },
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                resp.raise_for_status()
                return await resp.read()

    async def stream(self, text: str) -> AsyncIterator[bytes]:
        """Stream audio in chunks for lower latency playback."""
        audio = await self.synthesize(text)
        chunk_size = 4096
        for i in range(0, len(audio), chunk_size):
            yield audio[i : i + chunk_size]
            await asyncio.sleep(0)
