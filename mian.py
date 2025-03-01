import requests


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self) -> None:
        """
        Метод инициализации для запроса по API
        """
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def get_vacancies(self, keyword) -> list:
        """
        Получение вакансий с hh.ru
        :param keyword: ключевое слово
        :return: Список словарей с вакансиями
        """
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies


hh = HeadHunterAPI()
print(hh.get_vacancies('python'))