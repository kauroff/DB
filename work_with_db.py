"""
Модуль для работы с БД
"""

import psycopg2


def work_with_db(db_name: str) -> None:
    with psycopg2.connect(dbname=db_name) as conn:
        with conn.cursir() as cur:
            cur.execute("""
            CREATE TABLE vacancies(
            vacancy_id INT PRIMARY KEY,
            vacancy_name VARCHAR NOT NULL,
            vacancy_salary INT,
            vacancy_url TEXT,
            employ_id INT REFERENCES employees(employee_id))
            """)
        conn.commit()
        conn.close()

