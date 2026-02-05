// 🐹 Acme Lab: Web Intercom Logic
// Pure Vanilla JS - No Frameworks (Class 1 Design)

const CONFIG = {
    LOCAL_URL: "ws://localhost:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "2.1.0"
};

let ws = null;
const consoleEl = document.getElementById('chat-console');
const inputEl = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const statusDot = document.getElementById('connection-dot');
const statusText = document.getElementById('connection-text');
const versionEl = document.getElementById('lab-version');

function appendMsg(text, type = 'system-msg', source = 'System') {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    
    const prefix = source ? `[${source.toUpperCase()}]: ` : "";
    msg.textContent = `${prefix}${text}`;
    
    consoleEl.appendChild(msg);
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

function connect() {
    // Determine target URL based on current hostname
    const targetUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? CONFIG.LOCAL_URL 
        : CONFIG.REMOTE_URL;

    appendMsg(`Connecting to ${targetUrl}...`, 'system-msg');
    
    try {
        ws = new WebSocket(targetUrl);

        ws.onopen = () => {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'CONNECTED';
            appendMsg("Uplink Established. Handshaking...", "system-msg");
            
            // Handshake (As per acme_lab.py requirements)
            ws.send(jsonStr({ type: "handshake", version: CONFIG.VERSION }));
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleServerMessage(data);
        };

        ws.onclose = () => {
            statusDot.className = 'status-dot offline';
            statusText.textContent = 'DISCONNECTED';
            appendMsg("Connection Lost. Reconnecting in 5s...", "system-msg");
            setTimeout(connect, 5000);
        };

        ws.onerror = (err) => {
            console.error("WS Error:", err);
            appendMsg("Uplink Error. Check if Acme Lab server is running.", "system-msg");
        };

    } catch (e) {
        appendMsg(`Failed to initiate connection: ${e.message}`, "system-msg");
    }
}

function handleServerMessage(data) {
    if (data.type === 'status') {
        if (data.state === 'ready') {
            appendMsg("Lab is Open. Pinky is listening.", "system-msg");
            versionEl.textContent = `v${data.version || '???'}`;
        }
    } else if (data.brain) {
        appendMsg(data.brain, "brain-msg", data.brain_source || "Brain");
    } else if (data.type === 'debug') {
        appendMsg(`${data.event}: ${JSON.stringify(data.data)}`, "debug-msg", "Debug");
    }
}

function sendMessage() {
    const text = inputEl.value.trim();
    if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;

    appendMsg(text, "user-msg", "You");
    ws.send(jsonStr({ type: "text_input", content: text }));
    inputEl.value = "";
}

function jsonStr(obj) { return JSON.stringify(obj); }

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Sidebar Toggle (Parity with index.html)
document.getElementById('menu-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('active');
});

// Start
connect();
