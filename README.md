# 🛡️ Zero-Trust Web Guardian

An AI-powered, proactive dual-layer cybersecurity shield. It protects users from zero-day phishing attacks in the browser and defends servers against malicious network activities using the ASI-1 AI model.

---

## 🚀 Features

* **Proactive Web Quarantine:** Zero-click background scanning of web pages. Automatically freezes the DOM and blurs the screen if social engineering or phishing is detected.
* **Contextual AI Analysis:** Uses the ASI-1 model to understand the *intent* of a webpage or server log, rather than just relying on legacy blocklists.
* **Autonomous Security Agent:** A backend daemon that continuously monitors server logs and blocks threats (like Port Scans and Brute Force attacks) in real-time.

---

## 📂 Project Structure

\`\`\`text
Zero-Trust-Guardian/
│
├── backend/                  # Server-side & Autonomous Agent
│   ├── main.py               # FastAPI server to connect Extension with AI
│   ├── agent.py              # Background agent monitoring server logs
│   ├── log_generator.py      # Simulator for dummy network traffic
│   ├── prompts.txt           # System instructions for ASI-1
│   ├── server_logs.json      # Live log file
│   └── .env                  # API Keys (Create this file)
│
├── extension/                # Client-side Chrome Extension
│   ├── manifest.json         # Extension config (Manifest V3)
│   ├── background.js         # Service worker for zero-click auto-scanning
│   ├── popup.html            # Manual analysis UI
│   ├── popup.js              # Manual analysis logic
│   └── popup.css             # UI styling
│
└── fake-scam.html            # A honeypot page for live demonstration
\`\`\`

---

## 🛠️ Step 1: Backend Setup & API Key Configuration

1. **Install Python Libraries:**
   Open your terminal, navigate to the `backend` folder, and install the required dependencies:
   \`\`\`bash
   cd backend
   pip install fastapi uvicorn requests python-dotenv
   \`\`\`

2. **Configure ASI-1 API Key:**
   Inside the `backend` folder, create a new file named exactly `.env`.
   Paste your ASI-1 API key into this file like this:
   \`\`\`env
   ASI_ONE_API_KEY=your_actual_api_key_here
   \`\`\`

---

## 🧩 Step 2: Install the Chrome Extension

1. Open Google Chrome and go to `chrome://extensions/`.
2. Turn on **Developer mode** (toggle switch in the top right corner).
3. Click on the **Load unpacked** button in the top left.
4. Select the `extension` folder from this project directory.
5. The **Zero-Trust Guardian** icon will appear in your browser. Pin it for easy access.

---

## 🎯 Step 3: How to Test & Demo the Project

To see the full Zero-Trust architecture in action, follow these steps:

### Demo 1: The Browser Quarantine (Frontend)
1. Start the FastAPI backend server:
   \`\`\`bash
   cd backend
   uvicorn main:app --reload
   \`\`\`
2. Open the `fake-scam.html` file in your Chrome browser.
3. **Watch the magic:** You don't need to click anything. The extension's background worker will auto-scan the page, detect the cryptocurrency phishing attempt, and instantly lock/blur the screen with a Red Quarantine Alert.

### Demo 2: The Autonomous Agent (Backend)
1. Open a new terminal window and start the log simulator to generate fake hacker traffic:
   \`\`\`bash
   cd backend
   python log_generator.py
   \`\`\`
2. Open another terminal window and start the AI Security Agent:
   \`\`\`bash
   cd backend
   python agent.py
   \`\`\`
3. **Watch the magic:** The agent will read the live logs, analyze them using ASI-1, and print real-time Green (Allowed) or Red (Blocked) alerts based on the threat level.

---

## 💻 Tech Stack
* **Frontend:** HTML, CSS, JavaScript (Chrome Extension Manifest V3)
* **Backend:** Python, FastAPI, Uvicorn
* **AI Engine:** ASI-1 API (`/v1/chat/completions`)