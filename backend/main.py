import os
import json
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load API key from the .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebData(BaseModel):
    url: str
    content: str

@app.post("/analyze")
async def analyze_webpage(data: WebData):
    print(f"Analyzing URL with ASI-1: {data.url}")
    
    API_KEY = os.getenv("ASI_ONE_API_KEY")
    API_URL = "https://api.asi1.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Instruct the system to return strictly JSON
    system_prompt = """You are a top-tier cybersecurity AI. Analyze the URL and webpage content for phishing, social engineering, or scam indicators. 
    Provide the output strictly in JSON format with these exact keys:
    - "trust_score": (integer 0-100, where 100 is completely safe and 0 is extremely malicious)
    - "is_scam": (boolean)
    - "threat_type": (e.g., "Phishing", "Fake Crypto", "None")
    - "reason": (1-2 short sentences explaining the score)
    Do NOT output any markdown blocks or extra text, just the raw JSON object."""
    
    # The actual data from the user
    user_prompt = f"URL: {data.url}\nContent Snippet: {data.content}"
    
    payload = {
        "model": "asi1",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        api_result = response.json()
        
        # Extract text using the OpenAI format
        result_text = api_result['choices'][0]['message']['content']
        
        # Clean up (In case the AI accidentally wraps the response in markdown blocks)
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(result_text)
        
    except Exception as e:
        print(f"ASI-1 API Error: {e}")
        return {
            "trust_score": 50,
            "is_scam": False,
            "threat_type": "Connection Error",
            "reason": "Failed to connect to ASI-1 API. Check backend terminal for details."
        }