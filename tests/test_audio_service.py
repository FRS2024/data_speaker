"""
Automated test suite for Track E: Voice & Audio Interaction Engine.
Validates speech-to-text audio transcription, executive recap summarization,
and audio speech synthesis endpoints.
"""

import io
import wave
import pytest
from fastapi.testclient import TestClient

from services.api.audio_service import AudioService, audio_service
from services.api.database import create_db_and_tables
from services.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables exist before each test."""
    create_db_and_tables()


@pytest.fixture
def sample_wav_bytes() -> bytes:
    """Generate mock 1-second 16kHz mono WAV audio bytes for testing."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        # 16000 frames of silence/sine
        wav_file.writeframes(b"\x00\x00" * 16000)
    return buf.getvalue()


def test_transcribe_audio_empty(sample_wav_bytes: bytes):
    """Empty audio payload returns 0 duration and empty text."""
    res = audio_service.transcribe_audio(b"")
    assert res.text == ""
    assert res.duration_seconds == 0.0


def test_transcribe_audio_with_bytes(sample_wav_bytes: bytes):
    """Audio bytes return valid transcription response with estimated duration."""
    res = audio_service.transcribe_audio(sample_wav_bytes, filename="test.wav")
    assert len(res.text) > 0
    assert res.duration_seconds > 0.0
    assert res.confidence > 0.0


@pytest.mark.asyncio
async def test_generate_executive_recap_strips_code():
    """Executive recap strips code blocks and formulates high-impact spoken audio script."""
    raw_content = (
        "Here is the breakdown:\n"
        "```python\n"
        "import pandas as pd\n"
        "df.groupby('tier')['arr'].sum()\n"
        "```\n"
        "Enterprise revenue grew by 38.2% reaching $4.8M this quarter. "
        "Customer churn declined to 1.2% across North America. "
        "Recommend expanding sales development reps in EMEA tier."
    )
    recap = await audio_service.generate_executive_recap(content=raw_content)

    assert "```" not in recap.recap_text
    assert "import pandas" not in recap.recap_text
    assert "revenue grew by 38.2%" in recap.recap_text.lower()
    assert recap.estimated_listen_seconds >= 5
    assert len(recap.bullet_highlights) > 0


def test_synthesize_speech_wav_format():
    """Speech synthesizer outputs valid standard WAV audio bytes."""
    text = "Here is your executive recap. Revenue increased by twenty percent."
    wav_bytes = audio_service.synthesize_speech(text=text, voice="neutral", speed=1.0)

    assert len(wav_bytes) > 44  # Standard WAV header is 44 bytes
    assert wav_bytes.startswith(b"RIFF")
    assert b"WAVE" in wav_bytes[:12]

    # Verify wave structure can be opened by wave library
    with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == 16000
        assert wf.getnframes() > 0


def test_api_audio_transcribe_endpoint(sample_wav_bytes: bytes):
    """POST /api/v1/audio/transcribe returns typed transcription payload."""
    files = {"file": ("mic_recording.wav", io.BytesIO(sample_wav_bytes), "audio/wav")}
    res = client.post("/api/v1/audio/transcribe", files=files)
    assert res.status_code == 200
    data = res.json()
    assert "text" in data
    assert "duration_seconds" in data
    assert data["duration_seconds"] > 0


def test_api_audio_recap_endpoint():
    """POST /api/v1/audio/recap returns natural 20-second executive audio script."""
    payload = {
        "session_id": "sess_test_123",
        "content": "Overall ARR increased by 15% with net dollar retention at 118%.",
        "metrics": {"arr_growth": 0.15, "ndr": 1.18},
    }
    res = client.post("/api/v1/audio/recap", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "recap_text" in data
    assert "estimated_listen_seconds" in data
    assert data["estimated_listen_seconds"] > 0


def test_api_audio_synthesize_endpoint():
    """POST /api/v1/audio/synthesize returns streaming audio/wav bytes."""
    payload = {
        "text": "Executive Briefing: Q3 metrics exceed target projections.",
        "speed": 1.25,
    }
    res = client.post("/api/v1/audio/synthesize", json=payload)
    assert res.status_code == 200
    assert "audio/wav" in res.headers["content-type"]
    assert len(res.content) > 100
