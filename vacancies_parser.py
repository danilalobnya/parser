import requests
import sqlite3
import json


# создание базы данных
def create_table():

    db = sqlite3.connect('vacancies.db')

    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS vacancies (
        id integer PRIMARY KEY,
        title text,
        url text,
        requirements text,
        responsibilities text,
        company_name text
        )
    """)

    db.commit()

    db.close()

    print("таблица создана")


# запись данных в базу данных


def get_vacancies(text):

    create_table()

    url = "https://api.hh.ru/vacancies"
    for page in range(1):
        params = {
            "text": text,  # ключевое слово для поиска вакансии
            "area": 1,  # регион (1 - Москва)
            # "experience": experience, # опыт работы
            # "employment": employment, # тип занятости
            # "schedule": schedule, # график работы
            "page": page, # номер страницы
            "per_page": 100 # количество вакансий на одну страницу
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.content.decode()
            vacancies = json.loads(data)['items']
            for vacancy in vacancies:
                id = vacancy.get("id")
                title = vacancy.get("name")
                url = vacancy.get("alternate_url")
                requirements = vacancy.get("snippet", {}).get("requirement")
                responsibilities = vacancy.get("snippet", {}).get("responsibility")
                company_name = vacancy.get("employer", {}).get("name")

                print(f"ID: {id}\nНазвание: {title}\nКомпания: {company_name}\nТребования: {requirements}\nОбязанности: {responsibilities}\nСсылка: {url}\n")

                # запись в базу данных

        else:
            print(f"Request failed with status code: {response.status_code}")
