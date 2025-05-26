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

        # проверяем доступность сервера
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

    def test_find_rub_card_by_multiple_paths(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)

        # добавляем в начало мой xpath с ancestor
        paths = [
            "//h2[normalize-space(text())='Рубли']/ancestor::div[contains(@class, 'g-card_clickable')]",
            '//*[@id="root"]/div/div/div[1]/div[1]',
            '/html/body/div/div/div/div[1]/div[1]',
            '#root > div > div > div:nth-child(1) > div:nth-child(1)'  # css селектор
        ]

        found = False

        for path in paths:
            try:
                if path.startswith("#"):
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, path)))
                elif path.startswith("/"):
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
                else:
                    print(f"Пропускаем неизвестный селектор: {path}")
                    continue

                # проверка текста h2 для xpath путей (кроме css)
                if not path.startswith("#"):
                    h2 = element.find_element(By.TAG_NAME, "h2")
                    if h2.text.strip() != "Рубли":
                        print(f"Элемент найден по пути {path}, но h2 текст не 'Рубли', а '{h2.text.strip()}'")
                        continue

                print(f"Найден элемент по пути: {path}")
                element.click()
                found = True
                break
            except Exception as e:
                print(f"По пути {path} не найден элемент или ошибка: {e}")

        self.assertTrue(found, "Не удалось найти карточку с рублями ни по одному из путей")

if __name__ == "__main__":
    unittest.main()
