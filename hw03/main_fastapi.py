import uvicorn
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse




from weather_visual import get_address, api_get
#
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather")
async def weather(request: Request, address: str = Form(...), date: str = Form(...)):
    api_get(date)
    return templates.TemplateResponse("index.html", {"request": request, "address": address, "date": date})

@app.post('/process')
async def process_input(request: Request):
    data = await request.json()
    input_value = data['value']
    print(f'input_value ==> {input_value}')
    result = get_address(input_value)
    print(f'result ==> {result}')

    return JSONResponse(content={'result': result})

# test
# @app.get("/index", response_class=HTMLResponse)
# async def read_form(request: Request):
#     return templates.TemplateResponse("form.html", {"request": request})
#
# #test
# @app.post("/submit")
# async def handle_form(name: str = Form(...), age: int = Form(...)):
#     return {"name": name, "age": age}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)