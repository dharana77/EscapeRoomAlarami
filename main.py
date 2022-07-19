from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_decoder_book_instance(chrome_driver: webdriver.Chrome):
    decoder_book_rubato = "http://decoder.kr/book-rubato/"
    chrome_driver.get(decoder_book_rubato)
    month, year = get_month_and_year(chrome_driver)
    today = datetime.datetime.now()

    current_date = today.day

    while year != "2023" or month != "July":
        print(year, month, current_date)
        calender = find_calender(chrome_driver)
        picker_table = calender.find_element(by=By.CLASS_NAME, value="picker__table")
        table_dates = picker_table.find_elements(by=By.CSS_SELECTOR, value="td")

        current_month_end_date = get_month_end_date(current_month=month)
        current_table_date = get_next_clickable_date(table_dates=table_dates,
                                                     this_month_end_date=current_month_end_date,
                                                     this_month=month, current_date=current_date)
        current_div_date = current_table_date.find_element(by=By.CSS_SELECTOR, value="div")
        current_date = int(current_div_date.text)

        time_screen = find_time_screen(chrome_driver)
        time_buttons = time_screen.find_elements(By.CSS_SELECTOR, value="button")
        can_book_time_buttons = get_can_book_buttons(time_buttons)
        check_can_book_time_buttons(can_book_time_buttons=can_book_time_buttons)
        current_table_date.click()

        this_month, this_year = get_month_and_year(chrome_driver)
        wait_three_seconds_if_month_changed(this_month=this_month, month=month)
        month, year = this_month, this_year
        print("month", month, "year", year)

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


def get_next_clickable_date(table_dates: list, this_month_end_date: str, this_month: str, current_date: int = -1):
    is_first_day_count = 0

    for table_date in table_dates[1:]:
        div_date = table_date.find_element(by=By.CSS_SELECTOR, value="div")
        div_text_date = int(div_date.text)

        can_be_booked = div_date.get_attribute("aria-disabled")
        aria_selected = div_date.get_attribute("aria-selected")
        aria_active_descendant = div_date.get_attribute("aria-activedescendant")

        if can_be_booked is None and (aria_selected != "true" and aria_active_descendant != "true"):
            if is_current_date_in_next_seven_days(current_date=current_date, div_text_date=div_text_date):
                return table_date

            if current_date == 31:
                if int(div_date.text) == 1:
                    is_first_day_count += 1
                    if is_not_first_month(this_month, "July"):
                        if is_first_day_count == 2:
                            print("is_first_day_count")
                            return table_date
                        else:
                            continue
                    return table_date


def is_not_first_month(month: str, start_month):
    if month != start_month:
        return True
    return False


def is_current_date_in_next_seven_days(current_date: int, div_text_date: int):
    diff = div_text_date - current_date
    if 1 <= diff <= 7:
        return True
    return False


def get_month_end_date(current_month: str):
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    month_number = -1
    month_end_dates = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for idx, month in enumerate(months):
        if month == current_month:
            return month_end_dates[month_number]
    print("get_month_end_date errored")
    return 31


def wait_three_seconds_if_month_changed(this_month: str, month: str):
    if this_month != month:
        time.sleep(3)


def check_can_book_time_buttons(can_book_time_buttons: list):
    for book_button in can_book_time_buttons:
        if book_button.get_attribute("disabled") != "true":
            print("can be booked.")


create_decoder_book_instance(driver)
