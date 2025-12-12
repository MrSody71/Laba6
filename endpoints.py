from fastapi import FastAPI

app = FastAPI(title="Laba")

@app.get("/hello")
def hello():
    return {"hello": "world!"}
