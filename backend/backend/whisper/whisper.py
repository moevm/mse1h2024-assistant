import requests

def decode_audio(audio_bytes, whisper_host='whisper', whisper_port=9000):
    payload = {
        "input": {
            "encode": True,
            "task": "transcribe",
            "language": "ru",
            "vad_filter": True,
            "word_timestamps": False,
            "output": "txt",
        },
    }

    whisper_url = "http://{host}:{port}/asr".format(host=whisper_host, port=whisper_port)

    return requests.post(
        whisper_url,
        params=payload,
        files= {
            'audio_file': audio_bytes
        },
    )