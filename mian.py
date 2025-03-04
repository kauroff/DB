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
        print('''
Введите:
AE - если хотите получить список всех компаний и количество вакансий у каждой компании
AV - если хотите получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки
AS - если хотите получить среднюю зарплату по вакансиям
HS - если хотите получить список всех вакансий, у которых зарплата выше средней
KW - если хотите получить список всех вакансий, в названии которых содержатся переданное слово
Q - если хотите выйти''')
        answer = input()
        if answer.upper() == 'AE':
            all_employers = database.get_companies_and_vacancies_count()
            for emp, count in all_employers:
                print(f'{emp}, количество вакансий: {count}')
        elif answer.upper() == 'AV':
            all_vacancies = database.get_all_vacancies()
            for company, vacancy, salary, url in all_vacancies:
                print(f'{company}, {vacancy}, {salary} р., {url}')
        elif answer.upper() == 'AS':
            salary = database.get_avg_salary()
            print(f'{round(salary)} р.')
        elif answer.upper() == 'HS':
            high_salary = database.get_vacancies_with_higher_salary()
            for vacancy, salary, url in high_salary:
                print(f'{vacancy}, {salary} р., {url}')
        elif answer.upper() == 'KW':
            word = input('Введите слово для поиска: ')
            vacancies = database.get_vacancies_with_keyword(word)
            for vacancy, salary, url in vacancies:
                print(f'{vacancy}, {salary} р., {url}')
        elif answer.upper() == 'Q':
            break
        else:
            print('Нет такой команды, попробуйте еще раз')
