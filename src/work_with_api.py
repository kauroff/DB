import requests
import json


class API:
    """
    Класс для работы с API хэдхантера
    """

    def __init__(self) -> None:
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'per_page': 100,
            'page': 0,
            'only_with_salary': True
        }
        self.vacancies_data = []
        self.ids_data = self.__get_ids()

    def __get_ids(self) -> list:
        """
        Получает id компаний из файла
        :return: Список id
        """
        with open('data/employer_ids.json') as file:
            self.ids_data = json.load(file)['id']
        return self.ids_data

    def load_vacancies(self) -> list:
        """
        Выгружает по API вакансии с сайта
        :return: Список вакансий
        """
        for unit in self.ids_data:
            url = f'https://api.hh.ru/vacancies?employer_id={unit}'
            response = requests.get(url, headers=self.headers, params=self.params)
            data = response.json()['items']
            self.vacancies_data.append(data)
        return self.vacancies_data
