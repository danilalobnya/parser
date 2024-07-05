
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
import json

app = Flask(__name__)
CORS(app)

# Функция для создания таблицы в базе данных
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

# Функция для парсинга вакансий и записи их в базу данных
def parse_vacancies(text, experience, schedule, area):
    create_table()
    url = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "Your User Agent"
    }

    # Очистка таблицы перед добавлением новых вакансий
    db = sqlite3.connect('vacancies.db')
    c = db.cursor()
    c.execute("DELETE FROM vacancies")
    db.commit()
    db.close()

    for page in range(1, 21):
        params = {
            "text": text,
            "page": page,
            "per_page": 100
        }
        if experience != 'any':
            params['experience'] = experience
        if schedule != 'any':
            params['schedule'] = schedule
        if area != 'any':
            params['area'] = area
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            vacancies = response.json()['items']
            db = sqlite3.connect('vacancies.db')
            c = db.cursor()
            for vacancy in vacancies:
                # Добавление новых вакансий, игнорирование дубликатов
                c.execute('''INSERT OR IGNORE INTO vacancies 
                             (id, title, url, requirements, responsibilities, company_name) 
                             VALUES (?, ?, ?, ?, ?, ?)''',
                          (vacancy['id'], vacancy['name'], vacancy['alternate_url'],
                           vacancy['snippet']['requirement'], vacancy['snippet']['responsibility'],
                           vacancy['employer']['name']))
            db.commit()
            db.close()
        else:
            print(f"Request failed with status code: {response.status_code}")

# Маршрут для добавления параметров поиска вакансий через POST-запрос
@app.route('/add_search_parameters', methods=['POST'])
def add_search_parameters():
    data = request.json
    parse_vacancies(data['text'], data['experience'], data['schedule'], data['area'])
    return jsonify({'message': 'Параметры поиска добавлены и вакансии обновлены'}), 201


# Маршрут для получения списка вакансий из базы данных
@app.route('/vacancies', methods=['GET'])
def get_vacancies_from_db():
    db = sqlite3.connect('vacancies.db')
    c = db.cursor()
    c.execute("SELECT * FROM vacancies")
    vacancies = c.fetchall()
    db.close()
    result = [{'id': vacancy[0],
               'title': vacancy[1],
               'url': vacancy[2],
               'requirements': vacancy[3],
               'responsibilities': vacancy[4],
               'company_name': vacancy[5]} for vacancy in vacancies]
    return jsonify(result)

if __name__ == '__main__':
    app.run()
