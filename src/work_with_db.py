import psycopg2
from src.abc_dbm import ABSManager


class DBManager(ABSManager):
    def __init__(self, name):
        self.name = name

    def create_database(self, params: dict) -> None:
        """
        Создание базы данных
        :params database_name:
        :return:
        """
        conn = psycopg2.connect(dbname=self.name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {self.name}')
        cur.execute(f'CREATE DATABASE {self.name}')

        cur.close()
        conn.close()

    def create_table(self, table_name: str, params: dict) -> None:
        if table_name == 'vacancies':
            conn = psycopg2.connect(dbname=self.name, **params)
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                title VARCHAR NOT NULL,
                company_id INTEGER REFERENCES employers(employer_id),
                salary INTEGER,
                vacancy_url TEXT    
                )""")

            conn.commit()
            conn.close()
        else:
            conn = psycopg2.connect(dbname=self.name, **params)
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                title VARCHAR(50) NOT NULL,
                count_vacancies INTEGER,
                emp_url TEXT    
                )""")

            conn.commit()
            conn.close()

    def save_data_to_database(self, table_name: str, data: list[dict], params: dict):
        """
        Сохранение данных в бах данных
        :param table_name:
        :param data:
        :param params:
        :return:
        """

        if table_name == 'employers':
            conn = psycopg2.connect(dbname=self.name, **params)
            with conn.cursor() as cur:
                for emp in data:
                    cur.execute("""
                                INSERT INTO employers (
                                employer_id, title, count_vacancies, emp_url)
                                VALUES (%s, %s, %s, %s)
                                RETURNING employer_id
                                """,
                                (emp['id'], emp['title'], emp['count'], emp['url'])
                                )
                    self.employer_id = cur.fetchone()[0]
        else:
            conn = psycopg2.connect(dbname=self.name, **params)
            with conn.cursor() as cur:
                for vac in data:
                    cur.execute("""
                                INSERT INTO vacancies (
                                vacancy_id, title, company_id, salary, vacancy_url)
                                VALUES (%s, %s, %s, %s, %s)
                                """,
                                (vac['id'], vac['title'], employer_id, vac['sal'], vac['url'])
                                )

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
