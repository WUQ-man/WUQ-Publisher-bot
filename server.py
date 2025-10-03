from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "bot is alive"}
