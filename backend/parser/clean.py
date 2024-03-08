from nltk.tokenize import sent_tokenize, word_tokenize
import json

class KeyWords:
    def __init__(self, begin, end=None):
        self.begin = begin
        self.end = end    

def cut(text, key_words):
    if text.find(key_words.begin) == -1:
        return text
    elif not key_words.end:
        return text[:text.find(key_words.begin)]
    else:
        return text[:text.find(key_words.begin)] + text[text.find(key_words.end) + len(key_words.end):]


with open("data.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

keys = list(data.keys())
for label in keys:
    for num in range(len(data[label])):
        all_text = []
        
        try:
            data[label][num]['data']
        except TypeError:
            break

        for i in range(len(data[label][num]['data']) - 2):
            
            text = " ".join(word_tokenize(data[label][num]['data'][i]))
            
            key_words = [KeyWords("Recent Changes "), KeyWords("Last modified "), KeyWords("Backlinks "), KeyWords("Sidebar ", "Автоматизация учебных задач "), KeyWords("[ se.moevm.info ]", "МОЭВМ Вики »"), KeyWords("Sitemap ")]
            
            for elem in key_words:
                text = cut(text, elem)
            
            all_text.append(text)
        data[label][num]['data'] = all_text
    
with open("new_data.json", "w", encoding="utf-8") as w_file:
        json.dump(data, w_file, ensure_ascii=False, indent=4)
        


