from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_decoder_book_instance(chrome_driver: webdriver.Chrome):
    decoder_book_rubato = "http://decoder.kr/book-rubato/"
    chrome_driver.get(decoder_book_rubato)
    month, year = get_month_and_year(chrome_driver)

    time_screen = find_time_screen(chrome_driver)
    time_buttons = time_screen.find_elements(By.CSS_SELECTOR, value="button")
    can_book_time_buttons = get_can_book_buttons(time_buttons)

    calender = find_calender(chrome_driver)
    next_month_calender_button = calender.find_element(by=By.CLASS_NAME, value="picker__nav--next")

    current_date = -1
    end_date = 31

    while True:
        picker_table = calender.find_element(by=By.CLASS_NAME, value="picker__table")
        table_dates = picker_table.find_elements(by=By.CSS_SELECTOR, value="td")
        current_table_date = get_next_clickable_date(table_dates, current_date)
        if current_table_date is None:
            break
        current_div_date = current_table_date.find_element(by=By.CSS_SELECTOR, value="div")
        current_date = int(current_div_date.text)
        current_table_date.click()
        print(current_date)

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


def find_calender(chrome_driver: webdriver.Chrome):
    picker_holder = chrome_driver.find_element(by=By.CLASS_NAME, value="picker__holder")
    return picker_holder


def get_next_clickable_date(table_dates: list, current_date: int = -1):
    for table_date in table_dates:
        div_date = table_date.find_element(by=By.CSS_SELECTOR, value="div")

        can_be_booked = div_date.get_attribute("aria-disabled")
        aria_selected = div_date.get_attribute("aria-selected")
        aria_active_descendant = div_date.get_attribute("aria-activedescendant")

        if can_be_booked is None and (aria_selected != "true" and aria_active_descendant != "true"):
            if current_date < int(div_date.text):
                current_date = int(div_date.text)
                return table_date
        if table_date.text == "31":
            return None


create_decoder_book_instance(driver)
