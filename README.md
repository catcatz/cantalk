# 🎙️ cantalk — 廣東話 Voice Agent

Cantonese-first voice agent built on [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech).

> 講廣東話嘅本地語音助手。VAD → STT → LLM → TTS，全部 Mac 本地行。

## Architecture

```
Mic → [VAD: Silero] → [STT: faster-whisper-cantonese] → [LLM: Qwen3.5-4B] → [TTS: VoxCPM2] → Speaker
```

## Requirements

- Mac with Apple Silicon (M1/M2/M3/M4)
- Python 3.11+
- Running services:
  - [OMLX](https://omlx.ai) on `:8000` with `Qwen3.5-4B-MLX-4bit`
  - VoxCPM2 on `:8002`

## Quick Start

```bash
# 1. Clone
git clone https://github.com/catcatz/cantalk.git
cd cantalk

# 2. Setup
./scripts/setup.sh

# 3. Run
./scripts/run.sh
```

Then connect any OpenAI Realtime client to `ws://localhost:8765/v1/realtime`.

## Configuration

Edit `cantalk.yaml` to customize:

| Section | What it controls |
|---------|-----------------|
| `stt.model` | Cantonese STT model |
| `llm.system_prompt` | AI persona / personality |
| `tts.speaker` | VoxCPM2 voice |
| `server.port` | WebSocket port |

Voice personas live in `voices/` — swap them in `cantalk.yaml`.

## License

Apache 2.0 — same as huggingface/speech-to-speech.
