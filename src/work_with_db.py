import psycopg2
from src.abc_dbm import ABSManager
from data.config import config


class DBManager(ABSManager):
    def __init__(self, name):
        """
        Создание базы данных
        :params name, :
        :return:
        """
        self.name = name
        self.employer_id = ''
        self.params = config()

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {self.name}')
        cur.execute(f'CREATE DATABASE {self.name}')

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE employers (
            employer_id SERIAL PRIMARY KEY,
            company_name VARCHAR(50) NOT NULL,
            count_vacancies INTEGER,
            emp_url TEXT    
            );
            CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            company_id INTEGER REFERENCES employers(employer_id),
            salary INTEGER,
            vacancy_url TEXT    
            )""")

        conn.commit()
        conn.close()

    def save_employers_to_database(self, company_name, count, url) -> None:
        """
        Сохранение данных в бах данных
        :param company_name:
        :param count:
        :param url:
        :return:
        """

        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO employers (
                        company_name, count_vacancies, emp_url)
                        VALUES (%s, %s, %s)
                        RETURNING employer_id
                        """,
                        (company_name, count, url)
                        )
            self.employer_id = cur.fetchone()[0]
        conn.commit()
        conn.close()

    def save_vacancies_to_database(self, title, salary, url) -> None:
        """
        Сохранение данных в бах данных
        :param title:
        :param salary:
        :param url:
        :return:
        """

        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                                INSERT INTO vacancies (
                                title, company_id, salary, vacancy_url)
                                VALUES (%s, %s, %s, %s)
                                """,
                        (title, self.employer_id, salary, url)
                        )
        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT company_name, count_vacancies FROM employers
                        """
                        )
            data = cur.fetchall()[0]
        conn.commit()
        conn.close()
        return data

    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT company_name, title, salary, vacancy_url FROM vacancies
                        LEFT JOIN employers ON vacancies.company_id=employers.employer_id
                        """
                        )
            data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
