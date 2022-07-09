from selenium import webdriver

decoder_book_rubato = "http://decoder.kr/book-rubato/"
driver = webdriver.Chrome(decoder_book_rubato)

xpath = "//html/body/div[4]/table/tbody/tr/td[3]/div/div/div[4]/div/button[23]"
driver.find_element_by_xpath(xpath).click()
