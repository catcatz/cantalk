#!/bin/bash
# Setup cantalk — install dependencies on Mac
set -e

echo "=== cantalk setup ==="

# Check prerequisites
echo "Checking prerequisites..."
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found"
    exit 1
fi

echo "  ✅ python3: $(python3 --version)"

# Use Homebrew Python 3.11+ (system default is 3.9)
if [ -f /opt/homebrew/bin/python3.11 ]; then
    PYTHON=/opt/homebrew/bin/python3.11
    echo "  ✅ Using Homebrew Python: $($PYTHON --version)"
else
    PYTHON=python3
fi

# Check existing services
echo ""
echo "Checking VoxCPM2 (:8002)..."
curl -s --connect-timeout 3 http://127.0.0.1:8002/ &>/dev/null && echo "  ✅ VoxCPM2 running" || echo "  ⚠️  VoxCPM2 not responding"

echo "Checking OMLX (:8000)..."
curl -s --connect-timeout 3 http://127.0.0.1:8000/v1/models &>/dev/null && echo "  ✅ OMLX running" || echo "  ⚠️  OMLX not responding (may need API key)"

# Install Python deps
echo ""
echo "Installing Python dependencies..."
$PYTHON -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e "."

# Pre-cache STT model
echo ""
echo "Caching Cantonese STT model (first run will download)..."
python -c "
from faster_whisper import WhisperModel
model = WhisperModel('XA9/faster-whisper-large-v2-cantonese-2', device='cpu', compute_type='int8')
print('  ✅ STT model cached')
"

echo ""
echo "=== Setup complete ==="
echo "Run: ./scripts/run.sh"
