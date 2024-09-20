import uvicorn
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from weather_visual import fetch_weather_data, api_get, draw_graph

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather")
async def weather(request: Request, address: str = Form(...), date: str = Form(...)):
    api_get(date)
    draw_graph()
    return templates.TemplateResponse("index.html", {"request": request, "address": address, "date": date})

# test
@app.get("/index", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

#test
@app.post("/submit")
async def handle_form(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)