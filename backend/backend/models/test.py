from ollama import Client
client = Client(host='http://127.0.0.1:11434')
response = client.chat(model='mistral', messages=[
    {
            "role": 'user',
            "content": 'Привет!'
    }]
)

print(response)