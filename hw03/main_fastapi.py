import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse


from weather_visual import get_address, api_get, get_button
#
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather")
async def weather(request: Request):
    try:
        # 요청 본문이 ®비어있을 경우를 대비해 예외 처리
        data = await request.json()
        print(f'data => {data}')
        address = data.get('address')
        date = data.get('date')

        if not address or not date:
            return JSONResponse({"error": "Invalid data received"}, status_code=400)

        # API 호출 및 추가 작업 수행
        api_get(date, address)

        return templates.TemplateResponse("index.html",
                                          {"request": request, "address": address, "date": date})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.post("/button")
async def make_button(request: Request):
    data = await request.json()
    input_value = data['value']
    buttons = get_button(input_value)
    result = buttons.to_dict(orient='records')  # DataFrame을 리스트 형태의 딕셔너리로 변환
    return JSONResponse(content={"result": result})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)