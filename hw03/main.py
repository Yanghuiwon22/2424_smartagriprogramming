from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time

weather_url = 'https://weather.naver.com/'
browser = webdriver.Chrome()

browser.get(weather_url)

print('========== brower 접속 ==========')
soup = BeautifulSoup(browser.page_source, 'html.parser')
time.sleep(10)
webdriver_element = browser.find_element(By.XPATH, '//*[@id="header"]/div/div/div[3]/button/span[1]')
webdriver_element.click()
time.sleep(10)

