import time
import requests
from bs4 import BeautifulSoup


def get_links(text):
    data = requests.get(
        url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page=1",
        headers={"User-Agent": "User-Agent"}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        pages = int(soup.find("div", attrs={"class":"pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        return
    for page in range(1, pages):
        try:
            data = requests.get(
                url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page={page}",
                headers={"User-Agent": "User-Agent"}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"data-qa":"serp-item__title"}):
                yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")


def get_data(link):
    data = requests.get(
        url=link,
        headers={"User-Agent": "User-Agent"}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class":"resume-block__title-text"}).text
    except:
        name = ""
    try:
        age = soup.find(attrs={"data-qa":"resume-personal-age"}).text.replace("\xa0", "")
    except:
        age = ""
    try:
        salary = soup.find(attrs={"class":"resume-block__salary"}).text.replace("\u2009", "").replace("\xa0", "")
    except:
        salary = ""
    try:
        tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={"class":"bloko-tag__section_text"})]
    except:
        tags = []
    resume = {
        "name": name,
        "age": age,
        "salary": salary,
        "tags": tags,
        "link": link
    }
    return resume


for a in get_links("python"):
    print(get_data(a))
    time.sleep(1)
