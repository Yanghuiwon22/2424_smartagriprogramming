import uvicorn
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from weather_visual import fetch_weather_data, api_get, draw_graph

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather")
async def weather(request: Request, address: str = Form(...), date: str = Form(...)):
    # 입력된 주소를 다시 템플릿으로 넘겨서 화면에 표시
    return templates.TemplateResponse("index.html", {"request": request, "address": address, "date": date})

# test
@app.get("/index", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

#test
@app.post("/submit")
async def handle_form(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}



# ===================================================
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
# ===================================================

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)