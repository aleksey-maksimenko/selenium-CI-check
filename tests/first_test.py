import unittest
from selenium import webdriver

class PrintPageSourceTest(unittest.TestCase):
    def test_print_page_source(self):
        driver = webdriver.Chrome()
        driver.get("https://example.com")  # замени на нужный адрес
        print(driver.page_source)
        driver.quit()

if __name__ == "__main__":
    unittest.main()
