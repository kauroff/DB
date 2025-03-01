import requests
import json


class API:
    """
    Класс для работы с API хэдхантера
    """
    BASE_URL = 'https://api.hh.ru/vacancies'

    EMPLOYER_URL = 'https://api.hh.ru/employers'

    # https: // api.hh.ru / vacancies?employer_id = 3529

    def __init__(self) -> None:
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'per_page': 50,
            'page': 0,
            'only_with_salary': True
        }
        self.vacancies_data = []
        self.ids_data = self.get_ids()

    def get_ids(self):
        with open('../data/ids.json') as f:
            self.ids_data = json.load(f)['id']
        return self.ids_data

    def load_vacancies(self) -> None:
        for unit in self.ids_data:
            url = f'https://api.hh.ru/vacancies?employer_id={unit}'
            response = requests.get(url, headers=self.headers, params=self.params)
            data = response.json()['items']
            print(data)
            self.vacancies_data.extend(data)


hh = API()
print(hh.load_vacancies())
