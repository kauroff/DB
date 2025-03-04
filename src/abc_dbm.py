from abc import ABC


class ABCManager(ABC):

    def create_tables(self) -> None:
        """
        Создает таблицы в созданной базе данных
        :return: None
        """

    def save_employers_to_database(self, company_name: str, count: int, url: str) -> None:
        """
        Сохранение данных в бах данных
        :param company_name: Название компании
        :param count: Количество вакансий у компании
        :param url: Ссылка на работодателя
        :return: None
        """

    def save_vacancies_to_database(self, title: str, salary: int, url: str) -> None:
        """
        Сохранение данных в бах данных
        :param title: Название вакансии
        :param salary: Заработная плата
        :param url: Ссылка на вакансию
        :return: None
        """

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return: Кортеж компаний и количество вакансий у каждой компании
        """

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return: Список вакансий
        """

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям
        :return: Средняя зарплата
        """

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: Список вакансий
        """

    def get_vacancies_with_keyword(self, word: str) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        :return: Список вакансий
        """
