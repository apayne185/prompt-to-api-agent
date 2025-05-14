from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

@app.get("/")   
async def root():
    return {"message": "Prompt example 1"}
