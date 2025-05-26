import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class FindRubCardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "http://localhost:8000/?balance=30000&reserved=20001"

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

    def test_find_rub_card_by_text_and_role(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)

        try:
            rub_card = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[@role='button'][.//h2[normalize-space(text())='Рубли']]"
                ))
            )
            print("Карточка найдена по XPath с role и h2")
            rub_card.click()
        except Exception as e:
            self.fail(f"Карточка с рублями не найдена: {e}")

if __name__ == "__main__":
    unittest.main()
