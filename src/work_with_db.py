import psycopg2
from src.abc_dbm import ABSManager


class DBManager(ABSManager):
    def __init__(self):
        pass

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


class DB:
    def create_database(self, name: str, params: dict) -> None:
        """
        Создание базы данных
        :params name:
        :return:
        """

    def save_data_to_database(self, data: list, database_name: str, params: dict):
        """
        Сохранение данных в бах данных
        :param data:
        :param database_name:
        :param params:
        :return:
        """
