import ollama
import json

class OllamaClient:
    def __init__(self, model):
        self.model = model
        self.context = "Ты русскоязычный бот и отвечаешь только на русском языке. Для ответа используй следующую информацию: "

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

    #Метод, который заносит в контекст информацию, которую пользователь подаёт в параметры
    def readContextFromParametr(self, context):
        self.context += str(context) 

    #Метод, который обнуляет контекст
    def clearContext(self):
        self.context = "Ты русскоязычный бот и отвечаешь только на русском языке. Для ответа используй следующую информацию: " 

    #Метод, который создаёт промпт, указывая в нём сообщение и роль: system или user
    def __createPromt(self, message="", role="user"):
        return {
            "role": role,
            "content": message
        }

    #Метод, который отправляет промпт модели с учётом контекста и возвращает ответ 
    def sendPrompt(self, userMessage):
        response = ollama.chat(model=self.model, messages=[
            self.__createPromt(self.context, "system"),
            self.__createPromt(userMessage, "user")
        ],
        options={
            "temperature": 0
        })

        self.clearContext()

        return(response['message']['content'])