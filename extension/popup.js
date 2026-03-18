document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    const scoreText = document.getElementById('scoreText');
    const reasonText = document.getElementById('reasonText');
    const analyzeBtn = document.getElementById('analyzeBtn');

    analyzeBtn.innerText = "Scanning Page...";
    analyzeBtn.disabled = true;

    try {
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // 1. Current tab ke andar script inject karke page ka text nikalna
        const injectionResults = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                // Sirf first 3000 characters bhej rahe hain taaki API limit cross na ho aur speed fast rahe
                return document.body.innerText.substring(0, 3000);
            }
        });

        const pageContent = injectionResults[0].result;

        analyzeBtn.innerText = "Analyzing with AI...";

        // 2. Data Backend ko bhejna
        // 2. Data Backend ko bhejna
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: tab.url,
                content: pageContent
            })
        });

        const data = await response.json();

        // 3. UI Update karna
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