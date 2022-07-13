from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_decoder_book_instance(chrome_driver: webdriver.Chrome):
    decoder_book_rubato = "http://decoder.kr/book-rubato/"
    chrome_driver.get(decoder_book_rubato)
    month, year = get_month_and_year(chrome_driver)

    time_screen = find_time_screen(chrome_driver)
    buttons = time_screen.find_elements(By.CSS_SELECTOR, value="button")
    can_book_buttons = get_can_book_buttons(buttons)

    chrome_driver.quit()
    return chrome_driver


def get_month_and_year(chrome_driver: webdriver.Chrome):
    month = chrome_driver.find_element(by=By.CLASS_NAME, value="picker__month").text
    year = chrome_driver.find_element(by=By.CLASS_NAME, value="picker__year").text
    return month, year


def find_time_screen(chrome_driver: webdriver.Chrome):
    time_screen = chrome_driver.find_element(by=By.CLASS_NAME, value="ab-time-screen")
    return time_screen


def get_can_book_buttons(buttons: list):
    can_book_buttons = []
    for idx, button in enumerate(buttons):
        class_names = button.get_attribute("class").split(" ")
        class_name = class_names[0]
        if class_name == "ab-available-day" or class_name != "ab-available-hour":
            continue
        can_book_buttons.append(button)
    return can_book_buttons


create_decoder_book_instance(driver)