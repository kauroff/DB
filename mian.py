from src.work_with_db import DBManager
from src.work_with_api import API

if __name__ == '__main__':

    hh = API()
    data = hh.load_vacancies()
    database_name = input('Введите название для новой базы данных: ')
    database = DBManager(database_name)
    database.create_tables()
    for element in data:
        company_name = element[0]['employer']['name']
        count = len(element)
        url = element[0]['employer']['url']
        database.save_employers_to_database(company_name, count, url)
        for vacancy in element:
            title = vacancy['name']
            salary = vacancy['salary']['from']
            if salary is None:
                salary = vacancy['salary']['to']
            url = vacancy['alternate_url']
            database.save_vacancies_to_database(title, salary, url)
    while True:
        answer = input('''
Введите:
AE - если хотите получить список всех компаний и количество вакансий у каждой компании
AV - если хотите получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
AS - если хотите получить среднюю зарплату по вакансиям
HS - если хотите получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
KV - если хотите получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python
Q - если хотите выйти
''')
        if answer == 'AE':
            print(database.get_companies_and_vacancies_count)
        elif answer == 'AV':
            print(database.get_all_vacancies)
        elif answer == 'AS':
            print(database.get_avg_salary)
        elif answer == 'HS':
            print(database.get_vacancies_with_higher_salary)
        elif answer == 'KV':
            print(database.get_vacancies_with_keyword)
        elif answer == 'Q':
            break
        else:
            print('Нет такой команды, попробуйте еще раз')