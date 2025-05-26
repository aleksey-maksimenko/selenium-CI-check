import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

class PrintPageSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "http://localhost:8000/?balance=30000&reserved=20001"

        # проверяем, доступен ли сервер
        try:
            response = requests.get(cls.url)
            if response.status_code != 200:
                raise Exception(f"Сервер вернул статус: {response.status_code}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка доступа к серверу: {e}")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(cls.url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_print_page_source(self):
        # выводим весь HTML-код страницы
        print("\n=== PAGE SOURCE START ===\n")
        print(self.driver.page_source)
        print("\n=== PAGE SOURCE END ===\n")

if __name__ == "__main__":
    unittest.main()
