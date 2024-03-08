import whisper
import time

model_size = "small"

model = whisper.load_model(model_size)
options = whisper.DecodingOptions(language="ru")

file = open("./result/{model}.txt".format(model = model_size), "w")

start_time = time.time()

for i in range(1, 7):
    result = model.transcribe("./samples/sample_{num}".format(num = i), fp16=False)
    file.write(result["text"] + "\n\n")
    
end_time = time.time()

file.write(str(end_time - start_time))

file.close()
