import whisper
import torch
from backend.settings import whisper_config
import os, tempfile

print(torch.cuda.is_available())
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model(whisper_config.size, device=device)

def trunscribe(file):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        print(tmp.name)
        tmp.write(file.read())
        result = model.transcribe(tmp.name, fp16=False)
        return result["text"]
    
    finally:
        tmp.close()
        os.unlink(tmp.name)
