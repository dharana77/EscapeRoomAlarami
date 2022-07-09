from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_decoder_book_instance(chrome_driver: webdriver.Chrome):
    decoder_book_rubato = "http://decoder.kr/book-rubato/"
    chrome_driver.get(decoder_book_rubato)
    chrome_driver.quit()
    return chrome_driver


create_decoder_book_instance(driver)

# xpath = "//html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[23]"
# driver.find_element_by_xpath(xpath).click()
