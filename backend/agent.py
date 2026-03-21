import os
import time
import json
import requests
from dotenv import load_dotenv

# Load the API Key
load_dotenv()
API_KEY = os.getenv("ASI_ONE_API_KEY")
API_URL = "https://api.asi1.ai/v1/chat/completions"

# Terminal Colors for Hackathon Demo Vibe
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def load_system_prompt():
    # Read instructions from prompts.txt
    try:
        with open("prompts.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"{RED}Error: prompts.txt file not found. Please create it.{RESET}")
        exit()

def analyze_log_with_asi(log_entry, system_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "asi1",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this log: {json.dumps(log_entry)}"}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Extract JSON from ASI-1 response
        result_text = response.json()['choices'][0]['message']['content']
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(result_text)
    except Exception as e:
        return {"status": "ERROR", "reason": f"API Connection failed: {str(e)}"}

def start_agent():
    print(f"\n{YELLOW}🛡️ ASI-1 Zero-Trust Security Agent Started...{RESET}")
    print(f"{YELLOW}📡 Monitoring server_logs.json for live threats...{RESET}\n")
    
    system_prompt = load_system_prompt()
    log_file = "server_logs.json"
    
    # Open the file and seek to the end to only read new logs
    try:
        with open(log_file, "r") as f:
            f.seek(0, os.SEEK_END)
            
            while True:
                line = f.readline()
                
                # Wait for 1 second if there are no new logs
                if not line:
                    time.sleep(1)
                    continue
                
                # Cleanup (In case the file is in JSON array or JSONL format)
                clean_line = line.strip().strip(',').strip('[').strip(']')
                if not clean_line: 
                    continue
                
                try:
                    log_entry = json.loads(clean_line)
                    print(f"⏳ Analyzing Activity: {log_entry.get('activity')} from IP {log_entry.get('ip_address')}...")
                    
                    # Send the log to the AI
                    analysis = analyze_log_with_asi(log_entry, system_prompt)
                    
                    # Print result with corresponding colors
                    if analysis.get('status') == 'ALERT' or analysis.get('status') == 'CRITICAL':
                        print(f"{RED}🚨 [THREAT BLOCKED] Reason: {analysis.get('reason')}{RESET}\n")
                    else:
                        print(f"{GREEN}✅ [TRAFFIC ALLOWED] Reason: {analysis.get('reason')}{RESET}\n")
                        
                except json.JSONDecodeError:
                    pass # Ignore lines with invalid JSON
                    
    except FileNotFoundError:
        print(f"{RED}Error: server_logs.json not found. Run log_generator.py first.{RESET}")

if __name__ == "__main__":
    start_agent()