from dotenv import load_dotenv
load_dotenv()
import openai
from openai import OpenAI
import os
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def build_prompt(user_input: str) -> str:
        return f"""
            Given this user input: "{user_input}", identify whether the user is asking for weather or news.

            Return ONLY a JSON object with this format:
            {{
            "api": "weather",  // or "news"
            "parameters": {{
                "location": "CityName"  // for weather
                "topic": "TopicName"    // for news
                }}
            }}

            Do not include any text or explanation.
            """





def interpret_user_input(user_input:str) -> dict:    
    prompt = build_prompt(user_input)   

    try: 
        response = client.chat.completions.create(  
            model="gpt-4",
            messages=[   
                {"role": "system", "content": "You are a prompt routing assistant."},    
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  
            max_tokens= 150,
        )    
        
        # reply = response['choices'][0]['message']['content']   
        reply = response.choices[0].message.content
        print("GPT-4 response:", reply) 
        return json.loads(reply)  
    
        
    except json.JSONDecodeError:
        print("Failed to parse the GPT response as JSON.")
        print("Response content:  ", reply)
        return {}   
    
    except Exception as e:
        print("GPT API call failed: ", e)
        return {}   



    # try:
    #     import json
    #     return json.loads(reply)   
    
    # except json.JSONDecodeError:
    #     print("Failed o parse GPT response.")
    #     return {}   
    



# TEST SCRIPT
if __name__ == "__main__":
    user_input = "What's the weather like in Berlin, de today?"
    result = interpret_user_input(user_input)
    
    print("Parsed GPT Output:  ", result)