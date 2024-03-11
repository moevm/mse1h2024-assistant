import re
import json

def cut(text, regex):
    return " ".join(re.split(regex, text, maxsplit=0))

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

        for i in range(len(data[label][num]['data'])):
            
            text = " ".join(data[label][num]['data'][i].split("\n"))

            regex = [r'\[se.moevm.info\][\s\S]*?You are here: (\S+\s)*', r'Recent Changes[\s\S]*', r'Last modified[\s\S]*', r'Backlinks[\s\S]*', r'Sidebar[\s\S]*?Автоматизация учебных задач', r'Sitemap [\s\S]*', r'[\S]+:(?!\/)[\S]+', r'Table of Contents', r'[\S]*.txt', r'Таблица[\s\S]* \$ [\S\s]* \$']
            
            for elem in regex:
                text = cut(text, elem)

            if text.find("✎") != -1:
                break
            elif text.find("Permission Denied") != -1 or text.find("This topic does not exist yet") != -1:
                continue
            
            all_text.append(text)
        data[label][num]['data'] = cut(" ".join(all_text), r'\s+')

with open("new_data.json", "w", encoding="utf-8") as w_file:
        json.dump(data, w_file, ensure_ascii=False, indent=4)
        


