import ollama
import json

class OllamaClient:
    def __init__(self, model):
        self.model = model
        self.context = "Ты умеешь говорить только на русском языке. Для ответа используй следующую информацию: "

    #Метод, который ищет в json файле раздел с определённым названием и топиком, добавляет его в контекст 
    def readContextFromFile(self, file, titleOfChapter, titleOfTopic):
        try:
            with open(file, 'r') as f:
                jsonContext = json.loads(f.read())
                if(titleOfChapter in list(jsonContext.keys())):
                    resultContext = ""
                    for topic in jsonContext[titleOfChapter]:
                        if(topic["name"] == titleOfTopic): 
                            resultContext = topic["data"]
                            break          
                        
                    if(resultContext == ""): 
                        print("This topic doesn't exist")
                    else: 
                        self.context += str(resultContext)
                else:
                    print("This section doesn't exist")

        except:
            print("This file couldn't be found") 

    #Метод, который обнуляет контекст
    def clearContext(self):
        self.context = "Ты умеешь говорить только на русском языке. Для ответа используй следующую информацию: " 

    #Метод, который создаёт промпт, указывая в нём сообщение и роль: system или user
    def __createPromt(self, message="", role="user"):
        return {
            "role": role,
            "content": message
        }

    #Метод, который отправляет промпт модели, получает ответ и выводит его
    def sendPrompt(self, userMessage):
        print(len(self.context))

        response = ollama.chat(model=self.model, messages=[
            self.__createPromt(self.context, "system"),
            self.__createPromt(userMessage, "user")
        ], 
        options={
            "temperature": 0
        })

        print(response['message']['content'])

def main():
    testModel = OllamaClient("llama2")
    testModel.readContextFromFile("/home/azazzzel/mse1h2024-assistant/backend/parser/new_data.json", "info", "Регистрация первокурсников")
    testModel.sendPrompt("Какие действия по регистрации на moemv надо выполнить?")

if __name__ == "__main__":
    main()