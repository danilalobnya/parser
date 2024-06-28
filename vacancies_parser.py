import requests
import sqlite3


'''
db = sqlite3.connect('vacancies.db')

c = db.cursor()

c.execute("""CREATE TABLE vacancies (
    id integer,
    title text,
    url text,
    requirments text,
    responsibilities text,
    company_name text
    )
""")

db.commit()

db.close()
'''

def get_vacancies(text, area, pages):
    url = "https://api.hh.ru/vacancies"
    for page in range(pages):
        params = {
            "text": text,  # ключевое слово для поиска вакансии
            "area": area,  # регион (1 - Москва)
            # "experience": experience, # опыт работы
            # "employment": employment, # тип занятости
            # "schedule": schedule, # график работы
            "page": page, # номер страницы
            "per_page": 10 # количество вакансий на одну страницу
        }
        headers = {
            "User-Agent": "User-Agent"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            for vacancy in vacancies:
                id = vacancy.get("id")
                title = vacancy.get("name")
                url = vacancy.get("alternate_url")
                requirments = vacancy.get("snippet", {}).get("requirment")
                responsibilities = vacancy.get("snippet", {}).get("responsibility")
                company_name = vacancy.get("employer", {}).get("name")
                print(f"ID: {id}\nНазвание: {title}\nКомпания: {company_name}\nТребования: {requirments}\nОбязанности: {responsibilities}\nСсылка: {url}\n")
        else:
            print(f"Request failed with status code: {response.status_code}")


get_vacancies("python", 1, 1)
