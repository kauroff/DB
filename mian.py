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

    database.get_companies_and_vacancies_count()
    print(database.get_all_vacancies())