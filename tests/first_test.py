import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class BankTransferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get("http://localhost:8000/?balance=30000&reserved=20001")
        # не используем implicitly_wait, т.к. лучше ждать явно
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def save_screenshot_on_failure(self, test_name):
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        filepath = os.path.join(screenshots_dir, f"{test_name}.png")
        self.driver.save_screenshot(filepath)
        print(f"Скриншот сохранён: {filepath}")

    def test_card_input_shows_amount_input(self):
        driver = self.driver
        wait = WebDriverWait(driver, 15)

        try:
            # нажимаем на карточку с рублями - ждём кликабельность
            account_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]'))
            )
            account_button.click()

            # вводим валидный номер карты - ждём появление поля ввода
            card_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/input[1]'))
            )
            card_input.clear()
            card_input.send_keys("1111222233334444")

            # проверяем, появилось ли поле суммы
            amount_inputs = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/input[2]'))
            )
            self.assertTrue(len(amount_inputs) > 0, "Поле ввода суммы не появилось после ввода корректного номера карты")

            # очищаем и вводим неправильный номер
            card_input.clear()
            card_input.send_keys("123")

            # проверяем, что поле суммы пропало
            # здесь надо подождать, пока элемент исчезнет
            wait.until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/input[2]'))
            )

        except Exception as e:
            self.save_screenshot_on_failure(self._testMethodName)
            raise e


if __name__ == "__main__":
    unittest.main()
