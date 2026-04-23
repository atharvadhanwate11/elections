let currentContext = "General Inquiry";
let currentCountry = "USA";

const chatToggle = document.getElementById('chatToggle');
const chatWidget = document.getElementById('chatWidget');
const closeChat = document.getElementById('closeChat');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

// Toggle Chat Visibility
chatToggle.addEventListener('click', () => {
    chatWidget.classList.add('open');
});

closeChat.addEventListener('click', () => {
    chatWidget.classList.remove('open');
});

// Update Country Selection
function changeCountry() {
    const select = document.getElementById('countrySelect');
    currentCountry = select.value;
    
    if (currentCountry === 'USA') {
        document.getElementById('step1-desc').textContent = "Confirm your age, citizenship status, and state residency. Must be 18+ and a US citizen.";
        document.getElementById('step2-desc').textContent = "Register to vote before state deadlines. Can often be done online, by mail, or at the DMV.";
        document.getElementById('step3-desc').textContent = "Research candidates, propositions, and local measures. Use Ballotpedia or state voter guides.";
        document.getElementById('step4-desc').textContent = "Locate your polling place or drop box. Check if your state requires Voter ID.";
    } else if (currentCountry === 'India') {
        document.getElementById('step1-desc').textContent = "Confirm your age (18+) and ensure your name is on the Electoral Roll. Must be an Indian citizen.";
        document.getElementById('step2-desc').textContent = "Register via Form 6 on the Voter Helpline App or NVSP portal. You need this to get your EPIC card.";
        document.getElementById('step3-desc').textContent = "Research your constituency candidates. Use the KYC (Know Your Candidate) app by the ECI.";
        document.getElementById('step4-desc').textContent = "Find your polling booth via the ECI portal. Bring your Voter ID (EPIC) or Aadhar to cast your vote on the EVM.";
    }
    
    addMessage(`Switched region to ${currentCountry === 'USA' ? 'United States 🇺🇸' : 'India 🇮🇳'}. What do you want to know about the process?`, 'bot');
    chatWidget.classList.add('open');
}

// Progress Bar Logic (HCI Improvement)
function updateProgress() {
    const checkboxes = document.querySelectorAll('.tracker');
    let checkedCount = 0;
    
    checkboxes.forEach(cb => {
        if (cb.checked) checkedCount++;
    });
    
    const percentage = (checkedCount / checkboxes.length) * 100;
    document.getElementById('progressBar').style.width = Math.round(percentage) + '%';
    document.getElementById('progressText').textContent = Math.round(percentage) + '%';
    
    if (percentage === 100) {
        document.getElementById('progressBar').style.background = '#22c55e'; // Green when complete
        document.getElementById('progressText').style.color = '#22c55e';
    } else {
        document.getElementById('progressBar').style.background = 'var(--primary)';
        document.getElementById('progressText').style.color = 'var(--primary)';
    }
}

// Update Context from Step Cards
function updateContext(step) {
    currentContext = step;
    chatWidget.classList.add('open');
    
    addMessage(`I see you're interested in ${step} for the ${currentCountry} elections. How can I help?`, 'bot');
}

// Polling Station Redirect
function findPollingStation() {
    if (currentCountry === 'USA') {
        window.open('https://www.vote.org/polling-place-locator/', '_blank');
    } else {
        window.open('https://electoralsearch.eci.gov.in/', '_blank');
    }
}

// Add Message to UI
function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender}`;
    msgDiv.textContent = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle Form Submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';

    // Show typing state
    const typingMsg = document.createElement('div');
    typingMsg.className = 'chat-msg bot typing';
    typingMsg.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(typingMsg);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, context: currentContext, country: currentCountry })
        });
        
        if (!response.ok) throw new Error("Server error");
        
        // Remove typing indicator before starting the stream
        if (chatMessages.contains(typingMsg)) chatMessages.removeChild(typingMsg);
        
        // Create an empty bot message to fill
        const botMsgDiv = document.createElement('div');
        botMsgDiv.className = 'chat-msg bot';
        botMsgDiv.style.minHeight = '42px'; // Prevent layout jump
        chatMessages.appendChild(botMsgDiv);
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        
        while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            const chunk = decoder.decode(value, { stream: true });
            
            if (chunk.includes("Error:")) {
                botMsgDiv.textContent = chunk;
                break;
            }
            
            botMsgDiv.textContent += chunk;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        botMsgDiv.style.minHeight = ''; // Remove constraint after streaming is done

    } catch (error) {
        if (chatMessages.contains(typingMsg)) chatMessages.removeChild(typingMsg);
        addMessage("⚠️ Connection failed. Please check your internet and API key.", 'bot');
    }
});

