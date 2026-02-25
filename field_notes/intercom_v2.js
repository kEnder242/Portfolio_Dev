const CONFIG = {
    LOCAL_URL: "ws://localhost:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "3.8.0"
};

let ws = null;
let isMicActive = false;
let audioContext = null;
let micStream = null;
let processor = null;
let editor = null;

// DOM Elements
const chatConsole = document.getElementById('chat-console');
const insightConsole = document.getElementById('insight-console');
const textInput = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusDot = document.getElementById('connection-dot');
const activeFilename = document.getElementById('active-filename');
const resizer = document.getElementById('resizer');
const consoleRow = document.getElementById('console-row');
const workspaceContainer = document.getElementById('workspace-container');

let lastSystemState = "";

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    initEditor();
    initResizer();
    connect();
    pollSystemStatus();
    
    // UI Events
    sendBtn.addEventListener('click', sendText);
    textInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendText(); });
    micBtn.addEventListener('click', toggleMic);
    document.getElementById('menu-toggle').addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('collapsed');
    });
});

function initEditor() {
    editor = new EasyMDE({
        element: document.getElementById('workspace-content'),
        spellChecker: false,
        autosave: { enabled: false },
        status: ["lines", "words"],
        toolbar: ["bold", "italic", "heading", "|", "quote", "code", "table", "|", "preview", "side-by-side", "fullscreen"],
        minHeight: "100px"
    });
}

function initResizer() {
    if (resizer) {
        let isResizing = false;
        resizer.addEventListener('mousedown', () => { isResizing = true; });
        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const main = document.querySelector('main');
            const mainRect = main.getBoundingClientRect();
            const relativeY = e.clientY - mainRect.top;
            const containerHeight = main.offsetHeight;
            const newConsoleHeight = (relativeY / containerHeight) * 100;

            if (newConsoleHeight > 10 && newConsoleHeight < 80) {
                consoleRow.style.height = `${newConsoleHeight}%`;
                workspaceContainer.style.flex = "1";
                workspaceContainer.style.height = "auto";
                if (editor && editor.codemirror) {
                    editor.codemirror.refresh();
                }
            }
        });
        document.addEventListener('mouseup', () => { isResizing = false; });
    }
}

// --- MESSAGING ---
function appendMsg(text, type = 'system-msg', source = 'System', channel = 'chat', clear = false, metadata = {}) {
    const target = channel === 'insight' ? insightConsole : chatConsole;
    
    if (clear) {
        target.innerHTML = `<div class="panel-header">${channel === 'insight' ? "Brain's Insight" : "Pinky's Console"}</div>`;
    }

    if (channel === 'whiteboard' || channel === 'workspace') {
        if (editor) editor.value(text);
        return;
    }

    const msg = document.createElement('div');
    const msgType = (source && source.toLowerCase() === "system") ? "system-msg" : type;
    msg.className = `message ${msgType}`;
    
    const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const sl = source ? source.toLowerCase() : "system";
    let displaySource = source.toUpperCase();

    // [FEAT-118] Resonant Oracle Badge (Text-Only)
    if (metadata.oracle_category) {
        displaySource += ` (STATE: ${metadata.oracle_category})`;
    }

    // [FEAT-120] Context Transparency: Prepend clickable refs
    if (metadata.sources && metadata.sources.length > 0) {
        const sourceLinks = metadata.sources.map(s => 
            `<a href="#" onclick="openFile('${s}'); return false;" style="color:var(--accent-color); text-decoration:none; margin-right:5px;">[Ref: ${s}]</a>`
        ).join('');
        text = `${sourceLinks} ${text}`;
    }
    
    msg.innerHTML = `
        <div class="msg-header">
            <span class="msg-time">${time}</span>
            <span class="msg-source ${sl}">[${displaySource}]</span>
        </div>
        <div class="msg-body">${text}</div>
    `;
    
    // Fix: Routing Logic - TRUE Brain or Brain (Shadow) or explicit insight channel goes to the right.
    const sl_low = sl.toLowerCase().trim();
    const text_low = text.toLowerCase();
    
    // [FEAT-058] Strategic Shunt: If System mentions Sovereign/Engaging, route to Insight
    const isSystemStrategic = (sl_low === 'system') && (text_low.includes('sovereign') || text_low.includes('engaging'));
    
    const isTrueBrain = sl_low.includes('brain') || (channel === 'insight') || isSystemStrategic;
    
    if (!isTrueBrain) {
        chatConsole.appendChild(msg);
        chatConsole.scrollTop = chatConsole.scrollHeight;
    } else {
        insightConsole.appendChild(msg);
        insightConsole.scrollTop = insightConsole.scrollHeight;
    }
}

function sendText() {
    const content = textInput.value.trim();
    if (!content || !ws || ws.readyState !== WebSocket.OPEN) return;
    
    appendMsg(content, 'user-msg', 'ME');
    ws.send(JSON.stringify({ type: "text_input", content: content }));
    textInput.value = '';
}

async function saveWorkspace() {
    const content = editor.value();
    const filename = activeFilename.textContent === 'no file open' ? 'scratchpad.md' : activeFilename.textContent;
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "workspace_save", filename: filename, content: content }));
        appendMsg(`Saving ${filename}...`, 'system-msg', 'System');
    }
}

// --- MICROPHONE ---
async function toggleMic() {
    if (isMicActive) stopMic();
    else await startMic();
}

async function startMic() {
    try {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        }
        if (audioContext.state === 'suspended') {
            await audioContext.resume();
        }
        micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = audioContext.createMediaStreamSource(micStream);
        processor = audioContext.createScriptProcessor(4096, 1, 1);
        processor.onaudioprocess = (e) => {
            if (!isMicActive || !ws || ws.readyState !== WebSocket.OPEN) return;
            const inputData = e.inputBuffer.getChannelData(0);
            const pcmData = new Int16Array(inputData.length);
            for (let i = 0; i < inputData.length; i++) {
                const s = Math.max(-1, Math.min(1, inputData[i]));
                pcmData[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
            }
            ws.send(pcmData.buffer);
        };
        source.connect(processor);
        processor.connect(audioContext.destination);
        isMicActive = true;
        micBtn.classList.add('active');
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "mic_state", active: true }));
        }
        appendMsg("Microphone Active. Speak now...", "system-msg");
    } catch (err) {
        appendMsg(`Mic Error: ${err.message}`, "system-msg");
    }
}

function stopMic() {
    isMicActive = false;
    micBtn.classList.remove('active');
    if (micStream) micStream.getTracks().forEach(track => track.stop());
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "mic_state", active: false }));
    }
    appendMsg("Microphone Muted.", "system-msg");
}

// --- CONNECTION ---
function connect() {
    const targetUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? CONFIG.LOCAL_URL : CONFIG.REMOTE_URL;

    appendMsg(`Connecting to ${targetUrl}...`, 'system-msg');
    try {
        ws = new WebSocket(targetUrl);
        ws.onopen = () => {
            statusDot.className = 'status-dot online';
            ws.send(JSON.stringify({ type: "handshake", version: CONFIG.VERSION }));
        };
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.type === 'status') {
                if (data.message) {
                    appendMsg(data.message, 'system-msg', 'System');
                }
            } else if (data.type === 'file_content_request') {
                // [FEAT-074] Workbench: Mice requested a file for the user
                ws.send(JSON.stringify({ type: "read_file", filename: data.filename }));
            } else if (data.type === 'cabinet') {
                updateFileTree(data.files);
            } else if (data.type === 'file_content') {
                activeFilename.textContent = data.filename;
                editor.value(data.content);
            } else if (data.brain) {
                appendMsg(data.brain, 'brain-msg', data.brain_source || 'Brain', data.channel || 'chat', data.clear || false, {
                    oracle_category: data.oracle_category,
                    sources: data.sources
                });
            } else if (data.type === 'transcription') {
                appendMsg(data.text, 'user-msg', 'Me (Voice)');
            }
        };
        ws.onclose = () => {
            statusDot.className = 'status-dot offline';
            appendMsg("Disconnected. Reconnecting in 5s...", 'system-msg');
            setTimeout(connect, 5000);
        };
    } catch (err) {
        appendMsg(`Connection Error: ${err.message}`, 'system-msg');
    }
}

function openFile(fn) {
    console.log("Opening file via ref:", fn);
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "read_file", filename: fn }));
    }
}

function updateFileTree(files) {
    const tree = document.getElementById('file-tree');
    tree.innerHTML = '';
    files.forEach(f => {
        const item = document.createElement('div');
        item.className = 'tree-item';
        // Remove prefixes for display but keep them for the click event
        item.textContent = f;
        item.onclick = () => {
            console.log("Opening file:", f);
            ws.send(JSON.stringify({ type: "read_file", filename: f }));
        };
        tree.appendChild(item);
    });
}

async function pollSystemStatus() {
    try {
        const resp = await fetch('data/status.json?t=' + Date.now());
        const data = await resp.json();
        const vitals = data.vitals || {};
        const mode = vitals.mode || "OLLAMA";
        const model = vitals.model || "None";
        const newState = `[SYSTEM] ${mode}: ${model}`;
        
        if (newState !== lastSystemState) {
            appendMsg(newState, 'system-msg', 'System');
            lastSystemState = newState;
        }
    } catch (err) {
        console.error("Status poll failed", err);
    }
    setTimeout(pollSystemStatus, 10000);
}
