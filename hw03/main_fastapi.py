import uvicorn
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def index():
    return {"Hello": "World"}

@app.get('/address/')
def address(address_input: str):
    return {'address_text': address_input}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)