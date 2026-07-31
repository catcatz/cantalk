#!/bin/bash
# Start cantalk voice agent
set -e

cd "$(dirname "$0")/.."

if [ ! -d venv ]; then
    echo "venv not found. Run ./scripts/setup.sh first."
    exit 1
fi

source venv/bin/activate

echo "╔══════════════════════════════════════════╗"
echo "║        🎙️  cantalk — 廣東話 Agent       ║"
echo "╠══════════════════════════════════════════╣"
echo "║  VAD : Silero                            ║"
echo "║  STT : faster-whisper-cantonese (MPS)    ║"
echo "║  LLM : Qwen3.5-4B via OMLX :8000        ║"
echo "║  TTS : VoxCPM2 :8002                     ║"
echo "║  WS  : ws://localhost:8765/v1/realtime   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

python3 -m speech_to_speech \
    --config cantalk.yaml \
    --host 0.0.0.0 \
    --port 8765
