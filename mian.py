import requests


class API:
    """
    Класс для работы с API хэдхантера
    """
    BASE_URL = 'https://api.hh.ru/vacancies'

    EMPLOYER_URL = 'https://api.hh.ru/employers'

    def __init__(self) -> None:
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'per_page': 100,
            'page': 0,
            'only_with_salary': True
        }
        self.data = []

    def load_vacancies(self) -> None:
        # self.params['employer_id'] = employer_id
        self.params['page'] = 0
        #
        # response = requests.get(self.EMPLOYER_URL, headers=self.headers, params=self.params)
        # self.data = response.json()['items']

        # while self.params.get('page') != 50:
        while True:
            while self.params['page'] != 500:
                response = requests.get(self.EMPLOYER_URL, headers=self.headers, params=self.params)
                data = response.json()['items']
                print(data)
                self.data.extend(data)
                self.params['page'] += 1
        # return self.data



hh = API()
print(hh.load_vacancies())