import whisper
import time
import torch

print(torch.cuda.is_available())

model_size = "tiny"

model = whisper.load_model(model_size, device="cuda")

file = open("./result/{model}.txt".format(model = model_size), "w")

start_time = time.time()

for i in range(1, 10):
    result = model.transcribe("./samples/sample_{num}.ogg".format(num = i), fp16=False)
    file.write(result["text"] + "\n\n")
    
end_time = time.time()

file.write(str(end_time - start_time))

file.close()
