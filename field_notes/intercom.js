// 🐹 Acme Lab: Web Intercom Logic
// Pure Vanilla JS - No Frameworks (Class 1 Design)

const CONFIG = {
    LOCAL_URL: "ws://localhost:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "2.2.1"
};

let ws = null;
let audioContext = null;
let processor = null;
let micStream = null;
let isMicActive = false;

const consoleEl = document.getElementById('chat-console');
const inputEl = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusDot = document.getElementById('connection-dot');
const statusText = document.getElementById('connection-text');
const versionEl = document.getElementById('lab-version');
const audioMeter = document.getElementById('audio-level');
const meterContainer = document.getElementById('audio-meter-container');

function appendMsg(text, type = 'system-msg', source = 'System') {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    
    const prefix = source ? `[${source.toUpperCase()}]: ` : "";
    msg.textContent = `${prefix}${text}`;
    
    consoleEl.appendChild(msg);
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

// --- AUDIO LOGIC ---

async function toggleMic() {
    if (isMicActive) {
        stopMic();
    } else {
        await startMic();
    }
}

async function startMic() {
    try {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        }

        micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = audioContext.createMediaStreamSource(micStream);
        
        // We use a ScriptProcessorNode for simplicity in this "Class 1" design.
        // In a production app, an AudioWorklet would be better for performance.
        processor = audioContext.createScriptProcessor(4096, 1, 1);

        processor.onaudioprocess = (e) => {
            if (!isMicActive || !ws || ws.readyState !== WebSocket.OPEN) return;

            const inputData = e.inputBuffer.getChannelData(0);
            
            // 1. Calculate RMS for the meter
            let sum = 0;
            for (let i = 0; i < inputData.length; i++) {
                sum += inputData[i] * inputData[i];
            }
            const rms = Math.sqrt(sum / inputData.length);
            audioMeter.style.width = `${Math.min(100, rms * 500)}%`;

            // 2. Convert Float32 to Int16 (Signed PCM)
            const pcmData = new Int16Array(inputData.length);
            for (let i = 0; i < inputData.length; i++) {
                // Clamp and scale
                const s = Math.max(-1, Math.min(1, inputData[i]));
                pcmData[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
            }

            // 3. Send binary chunk
            ws.send(pcmData.buffer);
        };

        source.connect(processor);
        processor.connect(audioContext.destination);

        isMicActive = true;
        micBtn.classList.add('active');
        meterContainer.style.display = 'block';
        appendMsg("Microphone Active. Speak now...", "system-msg");

    } catch (err) {
        console.error("Mic Error:", err);
        appendMsg(`Failed to access microphone: ${err.message}`, "system-msg");
    }
}

function stopMic() {
    isMicActive = false;
    micBtn.classList.remove('active');
    meterContainer.style.display = 'none';
    
    if (micStream) {
        micStream.getTracks().forEach(track => track.stop());
    }
    appendMsg("Microphone Muted.", "system-msg");
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
            console.error("WS Error Details:", err);
            appendMsg(`Uplink Error. Protocol: ${ws.protocol}, ReadyState: ${ws.readyState}`, "system-msg");
            appendMsg("Check if 'acme.jason-lab.dev' requires Cloudflare Access login.", "system-msg");
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
micBtn.addEventListener('click', toggleMic);
inputEl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// --- UNIT TESTING / VERIFICATION ---

// Hidden test function: run in browser console to verify binary streaming
window.verifyAudioPipeline = (durationSec = 5) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        console.error("WebSocket not connected.");
        return;
    }
    
    appendMsg(`Starting Virtual Mic Test (${durationSec}s)...`, "system-msg");
    const sampleRate = 16000;
    const chunkSize = 4096;
    let elapsed = 0;

    const interval = setInterval(() => {
        // Generate a 440Hz sine wave as dummy audio
        const pcmData = new Int16Array(chunkSize);
        for (let i = 0; i < chunkSize; i++) {
            const time = (elapsed * chunkSize + i) / sampleRate;
            pcmData[i] = Math.sin(2 * Math.PI * 440 * time) * 10000;
        }
        
        ws.send(pcmData.buffer);
        elapsed++;

        if (elapsed * chunkSize / sampleRate >= durationSec) {
            clearInterval(interval);
            appendMsg("Virtual Mic Test Finished.", "system-msg");
        }
    }, (chunkSize / sampleRate) * 1000);
};

// Sidebar Toggle (Parity with index.html)
document.getElementById('menu-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('active');
});

// Start
connect();
