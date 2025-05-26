import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time

class BankTransferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "http://localhost:8000/?balance=30000&reserved=20001"

        # предварительная проверка доступности сервера
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
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_card_input_shows_amount_input(self):
        driver = self.driver

        # нажимаем на карточку с рублями (по тексту "Рубли")
        account_button = driver.find_element(By.XPATH, "//div[h2[text()='Рубли']]")
        account_button.click()
        time.sleep(1)

        # вводим валидный номер карты
        card_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/input[1]')
        card_input.send_keys("1111222233334444")
        time.sleep(1)

        # проверяем, появилось ли поле суммы
        amount_inputs = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[2]/input[2]')
        self.assertTrue(len(amount_inputs) > 0, "Поле ввода суммы не появилось после ввода корректного номера карты")

        # очищаем и вводим неправильный номер
        card_input.clear()
        card_input.send_keys("123")
        time.sleep(1)

        # проверяем, что поле суммы пропало
        amount_inputs = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[2]/input[2]')
        self.assertEqual(len(amount_inputs), 0, "Поле суммы не исчезло при вводе некорректного номера")

if __name__ == "__main__":
    unittest.main()
