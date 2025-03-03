from src.work_with_db import DBManager
from src.work_with_api import API

if __name__ == '__main__':

    hh = API()
    data = hh.load_vacancies()
    database = DBManager('db')  # можно назвать бд
    database.create_tables()
    emp = [data[i][0]['employer']['name'] for i in range(len(data))]
    for element in emp:
        print(element)

