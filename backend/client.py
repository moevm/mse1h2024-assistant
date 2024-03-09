import ollama
import json

class OllamaClient:
    def __init__(self, model):
        self.model = model
        self.context = "Ты умеешь говорить только на русском языке. Для ответа используй следующую информацию: "

    def readContextFromFile(self, file):
        try:
            with open(file, 'r') as f:
                self.context += f.read()
        except:
            print("This file couldn't be found") 

    def clearContext(self):
        self.context = "" 

    def createPromt(self, message="", role="user"):
        return {
            "role": role,
            "content": message
        }

    def sendPrompt(self, userMessage):
        response = ollama.chat(model=self.model, messages=[
            self.createPromt(self.context, "system"),
            self.createPromt(userMessage, "user")
        ], 
        options={
            "temperature": 0
        })

        print(response['message']['content'])

def main():
    testModel = OllamaClient("llama2")
    testModel.sendPrompt("Что такое Солнце?")

if __name__ == "__main__":
    main()