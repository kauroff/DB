from abc import ABC


class APIManager(ABC):
    def __get_ids(self) -> list:
        """
        Получает id компаний из файла
        :return: Список id
        """

    def load_vacancies(self) -> list:
        """
        Выгружает по API вакансии с сайта
        :return: Список вакансий
        """