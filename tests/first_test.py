import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ClickRubCardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)
        cls.url = "http://localhost:8000/dist/?balance=30000&reserved=20001"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_card_click_shows_input(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        driver.get(self.url)

        # находим карточку по тексту "Рубли" и кликаем
        rub_card = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//h2[normalize-space(text())='Рубли']/ancestor::div[contains(@class, 'g-card_clickable')]"
        )))
        rub_card.click()

        # ждём появления поля ввода по placeholder
        card_input = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//input[@placeholder='0000 0000 0000 0000']"
        )))

        # just to confirm test behavior - print attribute
        print("Найдено поле ввода:", card_input.get_attribute("placeholder"))

if __name__ == "__main__":
    unittest.main()
