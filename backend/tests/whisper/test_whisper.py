import pytest
from backend.whisper.whisper import decode_audio

whisper_test_host = "localhost"
whisper_test_port = 9001

@pytest.mark.integration
def test_decode_audio_successfully():
    f = open("./tests/whisper/test_audio.ogg", "rb")
    audio_data = f.read()
    f.close()
    
    response = decode_audio(audio_bytes=audio_data, whisper_host=whisper_test_host, whisper_port=whisper_test_port)
    
    assert response.status_code == 200
    
@pytest.mark.integration
def test_decode_audio_unsuccessfully():
    audio_data = "garbage"
    
    response = decode_audio(audio_bytes=audio_data, whisper_host=whisper_test_host, whisper_port=whisper_test_port)
    
    assert response.status_code == 500