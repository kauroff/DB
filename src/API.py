import requests


class API:
    """
    Класс для работы с API хэдхантера
    """
    BASE_URL = 'https://api.hh.ru/vacancies'

    # EMPLOYER_URL = 'https://api.hh.ru/employers'

    def __init__(self) -> None:
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'per_page': 50,
            'page': 0,
            'only_with_salary': True
        }
        self.data = []

    def load_vacancies(self) -> None:
        # self.params['employer_id'] = employer_id
        self.params['page'] = 0

        response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
        self.data = response.json()['items']

        while True:
            response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
            data = response.json()
            vacancies = data['items']
            self.data.extend(vacancies)

            if self.params['page'] >= data['pages'] - 1:
                break
            self.params['page'] += 1
        return self.data


hh = API()
print(hh.load_vacancies())