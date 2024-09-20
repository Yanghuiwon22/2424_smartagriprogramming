import uvicorn
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from fastapi.responses import HTMLResponse


app = FastAPI()

templates = Jinja2Templates(directory="templates")






@app.get("/index", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def handle_form(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}

# @app.get('/address/')
# def address(address_input: str):
#     return {'address_text': address_input}
#
# @app.get('/weather/')
# def weather(address_input: str):
#     weather_url = 'https://weather.naver.com/'
#     browser = webdriver.Chrome()
#
#     browser.get(weather_url)
#
#     if browser == 200:
#         soup = BeautifulSoup(browser.page_source, 'html.parser')
#         time.sleep(100)
#         webdriver_element = browser.find_element(By.XPATH, '//*[@id="header"]/div/div/div[3]/button/span[1]')
#         webdriver_element.click()
#         time.sleep(100)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)