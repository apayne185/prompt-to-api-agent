from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.prompts import interpret_user_input
from app.api_clients.weather import get_weather
from app.api_clients.news import get_news
import os
from dotenv import load_dotenv



app = FastAPI()

class QueryRequest(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {"message": "Prompt to API Agent is running"}   


@app.post("/query")
async def query_route(request: QueryRequest):
    try:     
        #interpret the user input using GPT4
        parsed = interpret_user_input(request.user_input) 
        print(f"Parsed response: {parsed}") 
        api = parsed.get("api")      
        params = parsed.get("parameters", {})   
           
        #dispatch to correct API client- weather/news 
        if api == "weather":
            result = get_weather(params.get("location")) 
        elif api == "news":   
            result= get_news(params.get("topic", "technology"))       #default fallback
        else:
            raise ValueError(f"Unsupported API type: {api}")
                     
        #return structured result  
        return {
            "success": True,   
            "api": api,
            "data": result  
        }   
       
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))   
    
