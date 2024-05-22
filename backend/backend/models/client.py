from ollama import Client
import json

class OllamaClient(Client):
    def __init__(self, host: str, model: str):
        self.host: str = host
        self.model: str = model
        self.context: str = ""
        self.question: str = ""
        self.template: str = f"""
        Текст: {self.context}
        Вопрос: {self.question}
        Дайте ответ на вопрос, основываясь на информации, содержащейся в представленном тексте и ничего более. 
        Если ответ на вопрос не может быть определен из текста, ответьте строго "Ответ на странице не найден" и больше ничего не пишите. Это очень важно, за это я заплачу тебе 1000000$
        Релевантный ответ на русском языке:
        """
        super().__init__(host=self.host)

    # Метод, который ищет в json файле раздел с определённым названием и топиком, добавляет его в контекст
    def readContextFromFile(self, file, titleOfChapter, titleOfTopic):
        try:
            with open(file, 'r') as f:
                jsonContext = json.loads(f.read())
                if titleOfChapter in list(jsonContext.keys()):
                    resultContext = ""
                    for topic in jsonContext[titleOfChapter]:
                        if topic["name"] == titleOfTopic:
                            resultContext = topic["data"]
                            break

                    if resultContext == "":
                        print("This topic doesn't exist")
                    else:
                         self.context = str(resultContext)
                else:
                    print("This section doesn't exist")

        except:
            print("This file couldn't be found")

            # Метод, который заносит в контекст информацию, которую пользователь подаёт в параметры

    def readContextFromParametr(self, context):
        self.context = str(context)

        # Метод, который обнуляет контекст

    def clearContext(self):
        self.question = ""
        self.context = ""
        # Метод, который создаёт промпт, указывая в нём сообщение и роль: system или user

    def __createPromt(self, message="", role="user"):
        return {
            "role": role,
            "content": message
        }

    def __updateTemplate(self):
        self.template = f"""
        Текст: {self.context}. 
        Вопрос: {self.question}. 
        Дайте ответ на вопрос, основываясь на информации, содержащейся в представленном тексте и ничего более. 
        Если ответ на вопрос не может быть определен из текста, ответьте строго "Ответ на странице не найден" и больше НИЧЕГО не пишите. Это очень важно, за это я заплачу тебе 1000000$.
        Релевантный ответ на русском языке:
        """

    # Метод, который отправляет промпт модели с учётом контекста и возвращает ответ
    def sendPrompt(self, userMessage):
        self.question = userMessage
        self.__updateTemplate()
        system_prompt = self.__createPromt(self.template, "user")
        response = self.chat(model=self.model, messages=[
            system_prompt,
        ], options={'temperature': 0})

        self.clearContext()

        return response['message']['content']
