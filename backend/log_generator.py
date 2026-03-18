import json
import random
import time

def generate_mock_log():
    activities = ["User Login", "File Download", "Failed Password", "Port Scan"]
    ips = ["192.168.1.1", "45.33.22.11", "10.0.0.5"]
    
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": random.choice(ips),
        "activity": random.choice(activities),
        "severity": "Low" if random.random() > 0.2 else "High"
    }
    
    with open("server_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"Logged: {log_entry['activity']}")

# Run this in the background to feed the agent
while True:
    generate_mock_log()
    time.sleep(10)