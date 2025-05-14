import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



def build_prompt(user_input: str) -> str:
    return (
        f"You are an assistant that determines the type of API to call based on user input.  \n"  
        f"Given the user's request: \"{user_input}\", identify the API ('weather' or 'news') "   
        f"and the necessary parameters.\n"   
        f"Respond strictly in this exact JSON format:\n"     
        f"{{\"api\": \"weather\", \"parameters\": {{\"location\": \"Madrid\"}}}}"    
    )    





def interpret_user_input(user_input:str) -> dict:    
    prompt = build_prompt(user_input)   

    try: 
        response = openai.ChatCompletion.create(  
            model="gpt-4",
            messages=[   
                {"role": "system", "content": "You are a prompt routing assistant."},    
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  
            max_tokens=150,
        )    
        
        reply = response['choices'][0]['message']['content']   
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