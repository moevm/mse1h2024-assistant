import json
import sys
sys.setrecursionlimit(1000000)
import requests
from bs4 import BeautifulSoup

def check_links(links, viewed_links):
    new_links = []
    for i in links:
        if i not in viewed_links and "?do=login&sectok=" not in i and "?do=diff&rev" not in i and "do=media" not in i:
            new_links.append(i)
    return new_links


def scrape_page(url, viewed_links):
    try:
        response = requests.get("https://se.moevm.info" + url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_data = soup.get_text()
        links = soup.find_all('a', href=True)
        links = check_links([link['href'] for link in links if link['href'].startswith('/')], viewed_links)
        return {'url': url, 'text': text_data, 'links': links}
    except Exception as e:
        print("An error occurred while scraping the page:", e)
        return None

MAX_DEPTH = 10

def recursive_scrape(page, viewed_links, li, depth=0):
    if depth >= MAX_DEPTH:
        return []

    result = []
    if page["url"] not in viewed_links:
        viewed_links.add(page["url"])
        page_data = scrape_page(page['url'], viewed_links)
        if page_data is not None:
            result.append(page_data['text'])
            if 'links' in page_data:
                for link in page_data["links"]:
                    if li in link:
                        result.extend(recursive_scrape({'name': '', 'url': link}, viewed_links, li, depth + 1))
    return result


url = "https://se.moevm.info/doku.php"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

viewed_links = set()

courses_data = {}
course_elems = soup.find_all('li', class_=["level1 node", "level2 node", "level3 node"])
courses_data["info"] = []
for course_elem in course_elems:
    course_name = course_elem.find("div", class_="li").text.strip()
    subjects = course_elem.find_all("a", class_="wikilink1")
    courses_data[course_name] = []
    for subject in subjects:
        subject_name = subject.text.strip()
        subject_url = subject["href"]
        courses_data[course_name].append({"name": subject_name, "url": subject_url})


info_elems = soup.find_all('li', class_="level1")
for info_elem in info_elems:
    course_name = info_elem.find("div", class_="li").text.strip()
    subjects = info_elem.find_all("a", class_="wikilink1")
    for subject in subjects:
        subject_name = subject.text.strip()
        subject_url = subject["href"]
        courses_data["info"].append({"name": subject_name, "url": subject_url})

def find_date(url):
    response = requests.get("https://se.moevm.info" + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    doc_info_elem = soup.find('div', class_='docInfo')
    if doc_info_elem:
        doc_info_text = doc_info_elem.get_text()
        last_modified_index = doc_info_text.find('Last modified:')
        if last_modified_index != -1:
            last_modified_text = doc_info_text[last_modified_index + len('Last modified:'):]
            last_modified_text = last_modified_text.strip()
            return last_modified_text

for i in courses_data:
    for j in courses_data[i]:
        link = j["url"][:j["url"].rfind(":")]
        date_mod = find_date(j["url"])
        data = recursive_scrape(j, viewed_links, link)
        j["date"] = date_mod
        j["data"] = data

courses_data["date"] = find_date("/doku.php")

with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(courses_data, json_file, ensure_ascii=False, indent=4)

