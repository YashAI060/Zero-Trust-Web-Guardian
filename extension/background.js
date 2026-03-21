// Background Worker: Monitors all newly opened or updated tabs
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    // Checks if the page has fully loaded and ensures it is not a Chrome internal page
    if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
        
        try {
            // 1. Silently scrape the text content of the page
            const injection = await chrome.scripting.executeScript({
                target: { tabId: tabId },
                func: () => document.body.innerText.substring(0, 3000)
            });
            
            const pageContent = injection[0].result;

            // 2. Send the scraped data to the Python AI backend for analysis
            const response = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: tab.url, content: pageContent })
            });

            const data = await response.json();

            // 3. THE QUARANTINE TRIGGER (If the AI determines the page is dangerous)
            if (data.trust_score < 30) {
                console.log("🚨 Threat Detected! Initiating Quarantine...");
                
                // Inject the Quarantine UI into the current page
                chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    func: executeQuarantine,
                    args: [data.reason, data.trust_score] // Passing the AI's reasoning along with the score
                });
            }

        } catch (error) {
            console.error("Auto-scan error:", error);
        }
    }
});

// This function is executed directly on the user's page to freeze it and display a warning
function executeQuarantine(aiReason, score) {
    // 1. Freeze the entire DOM (Prevents clicking, typing, or interaction)
    document.body.style.pointerEvents = 'none';
    document.body.style.overflow = 'hidden'; // Blocks scrolling
    
    // Blur the page content with an overlay
    const wrapper = document.createElement('div');
    wrapper.style.position = 'fixed';
    wrapper.style.top = '0';
    wrapper.style.left = '0';
    wrapper.style.width = '100vw';
    wrapper.style.height = '100vh';
    wrapper.style.backdropFilter = 'blur(8px)';
    wrapper.style.backgroundColor = 'rgba(0, 0, 0, 0.6)'; // Dark overlay
    wrapper.style.zIndex = '999998';
    document.body.appendChild(wrapper);

    // 2. Display the Danger Alert Box
    const alertBox = document.createElement('div');
    alertBox.style.position = 'fixed';
    alertBox.style.top = '50%';
    alertBox.style.left = '50%';
    alertBox.style.transform = 'translate(-50%, -50%)';
    alertBox.style.backgroundColor = '#2b0000';
    alertBox.style.color = '#ff4d4d';
    alertBox.style.padding = '40px';
    alertBox.style.borderRadius = '12px';
    alertBox.style.boxShadow = '0 0 30px rgba(255, 0, 0, 0.5)';
    alertBox.style.zIndex = '999999';
    alertBox.style.textAlign = 'center';
    alertBox.style.fontFamily = 'Arial, sans-serif';
    alertBox.style.maxWidth = '500px';

    alertBox.innerHTML = `
        <h1 style="font-size: 40px; margin-bottom: 10px;">🛑</h1>
        <h2 style="margin-top: 0; color: #ff4d4d;">QUARANTINE ACTIVATED</h2>
        <p style="color: #fff; font-size: 16px;">Zero-Trust Guardian has blocked this page to protect your credentials.</p>
        <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; margin-top: 20px;">
            <strong style="color: #ff9999;">Trust Score: ${score}/100</strong><br><br>
            <span style="color: #ccc; font-size: 14px;">AI Analysis: ${aiReason}</span>
        </div>
    `;

    document.body.appendChild(alertBox);
}
