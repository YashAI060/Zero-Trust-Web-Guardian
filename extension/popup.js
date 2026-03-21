document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    const scoreText = document.getElementById('scoreText');
    const reasonText = document.getElementById('reasonText');
    const analyzeBtn = document.getElementById('analyzeBtn');

    analyzeBtn.innerText = "Scanning Page...";
    analyzeBtn.disabled = true;

    try {
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // 1. Inject script into the current tab to extract page text
        const injectionResults = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                // Only send the first 3000 characters to avoid API limits and ensure fast performance
                return document.body.innerText.substring(0, 3000);
            }
        });

        const pageContent = injectionResults[0].result;

        analyzeBtn.innerText = "Analyzing with AI...";

        // 2. Send data to the backend
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: tab.url,
                content: pageContent
            })
        });

        const data = await response.json();

        // 3. Update the UI
        resultDiv.style.display = 'block';

        if (data.trust_score < 40) {
            resultDiv.className = 'danger'; // Red
        } else if (data.trust_score < 70) {
            resultDiv.className = 'safe';
            resultDiv.style.backgroundColor = '#fff3cd'; // Yellow warning for medium score
            resultDiv.style.color = '#856404';
        } else {
            resultDiv.className = 'safe'; // Green
        }

        scoreText.innerText = `Trust Score: ${data.trust_score}/100`;
        reasonText.innerText = data.reason;

    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'danger';
        scoreText.innerText = "Error!";
        reasonText.innerText = "Extension failed to scan or connect to server.";
        console.error(error);
    } finally {
        analyzeBtn.innerText = "Analyze Page";
        analyzeBtn.disabled = false;
    }
});