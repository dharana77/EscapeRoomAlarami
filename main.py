from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_decoder_book_instance(chrome_driver: webdriver.Chrome):
    decoder_book_rubato = "http://decoder.kr/book-rubato/"
    chrome_driver.get(decoder_book_rubato)

    month = driver.find_element(by=By.CLASS_NAME, value="picker__month").text
    year = driver.find_element(by=By.CLASS_NAME, value="picker__year").text

    chrome_driver.quit()

    return chrome_driver


create_decoder_book_instance(driver)