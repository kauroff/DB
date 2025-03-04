import psycopg2
from abc_dbm import ABCManager
from data.config import config


class DBManager(ABCManager):
    def __init__(self, name) -> None:
        """
        Создание базы данных
        :params name: Название базы данных
        :return: None
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
        """
        Создает таблицы в созданной базе данных
        :return: None
        """
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

    def save_employers_to_database(self, company_name: str, count: int, url: str) -> None:
        """
        Сохранение данных в бах данных
        :param company_name: Название компании
        :param count: Количество вакансий у компании
        :param url: Ссылка на работодателя
        :return: None
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

    def save_vacancies_to_database(self, title: str, salary: int, url: str) -> None:
        """
        Сохранение данных в бах данных
        :param title: Название вакансии
        :param salary: Заработная плата
        :param url: Ссылка на вакансию
        :return: None
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

    def get_companies_and_vacancies_count(self) -> tuple:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return: Кортеж компаний и количество вакансий у каждой компании
        """
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

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return: Список вакансий
        """
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

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям
        :return: Средняя зарплата
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT AVG(salary) FROM vacancies
                        """
                        )
            salary = cur.fetchall()[0][0]
        conn.commit()
        conn.close()
        return salary

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: Список вакансий
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                                SELECT title, company_id, salary, vacancy_url FROM vacancies
                                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                                """
                        )
            data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, word: str) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        :return: Список вакансий
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""
                        SELECT vacancy_id, title, company_id, salary, vacancy_url FROM vacancies
                        WHERE title LIKE '%{word}%'  
                        """
                        )
            data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
