import datetime
import json
import sys

sys.setrecursionlimit(1000000000)
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


def recursive_scrape(page, viewed_links, depth, max_depth):
    if depth >= max_depth:
        return []

    result = []
    viewed_links.add(page["url"])
    page_data = scrape_page(page['url'], viewed_links)
    if page_data is not None:
        result.append(page_data['text'])
        if 'links' in page_data:
            for link in page_data["links"]:
                result.extend(
                    recursive_scrape({'name': '', 'url': link}, viewed_links, depth + 1, max_depth))
    return result


def read_courses(viewed_links):
    url = "https://se.moevm.info/doku.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
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
            viewed_links.add(subject_url)
            courses_data[course_name].append({"name": subject_name, "url": subject_url})

    info_elems = soup.find_all('li', class_="level1")
    for info_elem in info_elems:
        course_name = info_elem.find("div", class_="li").text.strip()
        subjects = info_elem.find_all("a", class_="wikilink1")
        for subject in subjects:
            subject_name = subject.text.strip()
            if subject_name != "Программирование" and subject_name != "Информатика":
                subject_url = subject["href"]
                viewed_links.add(subject_url)
                courses_data["info"].append({"name": subject_name, "url": subject_url})
    return courses_data


def find_date(url):
    response = requests.get("https://se.moevm.info" + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    doc_info_elem = soup.find('div', class_='docInfo')
    if doc_info_elem:
        doc_info_text = doc_info_elem.get_text()
        last_modified_index = doc_info_text.find('Last modified:')
        if last_modified_index != -1:
            last_modified_text = doc_info_text[last_modified_index + len('Last modified:'):].strip()
            split_text = last_modified_text.split(' ')
            date = split_text[0] + " " + split_text[1]
            date_format = "%Y/%m/%d %H:%M"
            timestamp = datetime.datetime.strptime(date, date_format)
            return json.dumps(timestamp.strftime(date_format))


def create_data(courses_data, viewed_links, max_depth):
    for courses in courses_data:
        for subject in courses_data[courses]:
            date_mod = find_date(subject["url"])
            data = recursive_scrape(subject, viewed_links, 0, max_depth)
            subject["date"] = date_mod
            subject["data"] = data
    courses_data["date"] = find_date("/doku.php")


viewed_links = set()
courses_data = read_courses(viewed_links)
max_depth = 2
create_data(courses_data, viewed_links, max_depth)

# with open("./data/data.json", "w", encoding="utf-8") as json_file:
#     json.dump(courses_data, json_file, ensure_ascii=False, indent=4)

chunk_size = 40 * 1024 * 1024

chunks = []
current_chunk = []
current_chunk_size = 0
for course_id, course_data in courses_data.items():
    course_data_size = len(json.dumps(course_data, ensure_ascii=False, indent=4).encode('utf-8'))
    if current_chunk_size + course_data_size > chunk_size:
        chunks.append(current_chunk)
        current_chunk = []
        current_chunk_size = 0
    current_chunk.append((course_id, course_data))
    current_chunk_size += course_data_size
if current_chunk:
    chunks.append(current_chunk)

for i, chunk in enumerate(chunks):
    with open(f"./data/data_{i}.json", "w", encoding="utf-8") as chunk_file:
        json.dump(dict(chunk), chunk_file, ensure_ascii=False, indent=4)