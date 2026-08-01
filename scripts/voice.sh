#!/bin/bash
# cantalk voice mode — use Mac mic directly, speak and hear response
set -e

cd "$(dirname "$0")/.."
source venv/bin/activate

echo "╔══════════════════════════════════════════╗"
echo "║     🎙️  cantalk — 語音對話 mode         ║"
echo "║     對住 Mac 講野 → 喇叭出聲             ║"
echo "╚══════════════════════════════════════════╝"
echo ""

exec speech-to-speech \
    --mode local \
    --llm_backend chat-completions \
    --stt faster-whisper \
    --faster_whisper_stt_model_name "XA9/faster-whisper-large-v2-cantonese-2" \
    --faster_whisper_stt_device auto \
    --faster_whisper_stt_gen_language yue \
    --model_name "ThinkingCap-Qwen3.6-27B-oQ4e-DWQ-MTP-Vision-MLX" \
    --responses_api_base_url "http://127.0.0.1:8000/v1" \
    --responses_api_api_key "sk-123456" \
    --init_chat_prompt "你係 Lucille，小強嘅 AI 助手同好朋友。講廣東話，語氣溫暖直接、簡潔唔長氣。用口語廣東話，唔好扮書面語。回應要短，一兩句夠就唔好講多。" \
    --qwen3_tts_model_name "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice" \
    --qwen3_tts_device mps \
    --qwen3_tts_language zh
