import os
import httpx
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
   
   
def get_news(query: str) -> dict:
    if not NEWSAPI_KEY:
        return {"error": "NewsAPI key isnt set."}
     
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query, 
        "apiKey": NEWSAPI_KEY,   
        "language": "en",
        "pageSize": 5,       #limit for brevity  
        "sortBy": "relevancy"
    }  
       
    try:
        response = httpx.get(base_url, params=params, timeout= 10)  
        response.raise_for_status()   
        data = response.json() 
      
        articles = [
            { 
                "title": article["title"],  
                "source": article["source"]["name"],  
                "url": article["url"]  
            }
            for article in data.get("articles", [])  
        ] 
       
        return {"results": articles}      
    


    except httpx.RequestError as e:   
        return {"error": f"Network error while fetching the news: {str(e)}"}  
        
    except httpx.HTTPStatusError as e:   
        return {"error":f"API response error: {e.response.status_code} - {e.response.text}"}    
      
    except Exception as e:   
        return {"error":f"Unexpected error: {str(e)}"}     
    
