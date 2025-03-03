import psycopg2
from src.abc_dbm import ABSManager
from data.config import config


class DBManager(ABSManager):
    def __init__(self, name, **params):
        """
        Создание базы данных
        :params name, :
        :params **params:
        :return:
        """
        self.name = name
        self.employer_id = ''
        self.params = config()

        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {self.name}')
        cur.execute(f'CREATE DATABASE {self.name}')

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            company_id INTEGER REFERENCES employers(employer_id),
            salary INTEGER,
            vacancy_url TEXT    
            );
            CREATE TABLE employers (
            employer_id SERIAL PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            count_vacancies INTEGER,
            emp_url TEXT    
            )""")

        conn.commit()
        conn.close()

    def save_employers_to_database(self, data: list[dict]) -> str:
        """
        Сохранение данных в бах данных
        :param data:
        :return:
        """

        conn = psycopg2.connect(dbname=self.name, **self.params)
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
        conn.commit()
        conn.close()
        return self.employer_id

    def save_vacancies_to_database(self, data: list[dict]) -> None:
        """
        Сохранение данных в бах данных
        :param data:
        :param params:
        :return:
        """

        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            for vac in data:
                cur.execute("""
                                    INSERT INTO vacancies (
                                    vacancy_id, title, company_id, salary, vacancy_url)
                                    VALUES (%s, %s, %s, %s, %s)
                                    """,
                            (vac['id'], vac['title'], self.employer_id, vac['sal'], vac['url'])
                            )
        conn.commit()
        conn.close()


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
