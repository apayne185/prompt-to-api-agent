import os
import httpx
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")   



def get_weather(location: str) -> dict:
    if not OPENWEATHER_API_KEY:
        return {"error": "OpenWeatherMap API key is not set. "}    

    base_url = "https://api.openweathermap.org/data/2.5/weather"     
    params = {
        "q": location,    
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  
    }  
       
    try:
        response = httpx.get(base_url, params= params, timeout=10)  
        response.raise_for_status()
        data = response.json()    
            
        return { 
            "location": data["name"], 
            "temperature": data["main"]["temp"],  
            "description": data["weather"][0]["description"],   
            "humidity": data["main"]["humidity"],     
            "wind_speed": data["wind"]["speed"]  
        } 
    
      
    except httpx.RequestError as e:   
        return {"error": f"Network error during the fetching weather data:  {str(e) }"}
    
       
    except httpx.HTTPStatusError as e:
        return {"error": f"API response error: {e.response.status_code} - {e.response.text}"}
         
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}   
    
