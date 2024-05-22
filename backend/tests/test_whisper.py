import pytest
from backend.whisper.whisper import decode_audio
from backend.settings import config

whisper_test_host = config.whisper_host
whisper_test_port = config.whisper_port

@pytest.mark.integration
def test_decode_audio_successfully():
    f = open("./test_audio.ogg", "rb")
    audio_data = f.read()
    f.close()
    
    response = decode_audio(audio_bytes=audio_data, whisper_host=whisper_test_host, whisper_port=whisper_test_port)
    
    assert response.status_code == 200
    
@pytest.mark.integration
def test_decode_audio_unsuccessfully():
    audio_data = "garbage"
    
    response = decode_audio(audio_bytes=audio_data, whisper_host=whisper_test_host, whisper_port=whisper_test_port)
    
    assert response.status_code == 500