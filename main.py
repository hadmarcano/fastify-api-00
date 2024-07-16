from fastapi import FastAPI

app = FastAPI()

app.title = "FASTAPI Server"
app.version = "0.0.1"


@app.get("/", tags=['Utils'])
async def message():
    return {"message": "Hello World"}