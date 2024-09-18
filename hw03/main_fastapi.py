import uvicorn
from fastapi import FastAPI
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time

app = FastAPI()
@app.get("/")
def index():
    return {"Hello": "World"}

@app.get('/address/')
def address(address_input: str):
    return {'address_text': address_input}

@app.get('/weather/')
def weather(address_input: str):
    weather_url = 'https://weather.naver.com/'
    browser = webdriver.Chrome()

    browser.get(weather_url)

    if browser == 200:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        time.sleep(100)
        webdriver_element = browser.find_element(By.XPATH, '//*[@id="header"]/div/div/div[3]/button/span[1]')
        webdriver_element.click()
        time.sleep(100)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)