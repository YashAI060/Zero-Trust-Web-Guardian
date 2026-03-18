import requests
import json
import os

def test_asi_one_api():
    # Replace with your actual ASI:One API key, or set it as an environment variable
    # e.g., os.environ['ASI_ONE_API_KEY'] = 'your_api_key_here'
    api_key = os.environ.get("ASI_ONE_API_KEY", "enter your api key")
    
    if api_key == "enter your api key":
        print("Warning: Please replace 'enter your api key' with your actual API key.")
    
    url = "https://api.asi1.ai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Payload compatible with OpenAI's Chat Completions API
    payload = {
        "model": "asi1-mini", # You might need to change the model name to the one you want to use
        "messages": [
            {
                "role": "user",
                "content": "Hello! This is a test message. Please respond with a short greeting."
            }
        ],
        "max_tokens": 50
    }
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, headers=headers, json=payload)
        
        # Check if the request was successful
        response.raise_for_status()
        
        response_data = response.json()
        print("\nSuccess! API Response:")
        print(json.dumps(response_data, indent=2))
        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            print("\nModel Reply:")
            print(response_data["choices"][0]["message"]["content"])
            
    except requests.exceptions.HTTPError as err:
        print(f"\nHTTP Error: {err}")
        print("Response body:", response.text)
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    test_asi_one_api()
