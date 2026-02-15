// 🐹 Acme Lab: Workbench Console Logic v3.4.11
console.log("Workbench Console v3.4.11 loading...");

const CONFIG = {
    LOCAL_URL: "ws://localhost:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "3.4.0"
};

let ws = null;
let activeFile = null;
let editor = null;
let isLoading = false;
let audioContext = null;
let processor = null;
let micStream = null;
let isMicActive = false;

// UI Elements
const chatConsole = document.getElementById('chat-console');
const insightConsole = document.getElementById('insight-console');
const activeFilename = document.getElementById('active-filename');
const fileTree = document.getElementById('file-tree');
const inputEl = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusDot = document.getElementById('connection-dot');
const systemStatusEl = document.getElementById('system-status');

function pollSystemStatus() {
    const el = document.getElementById('system-status');
    if (!el) return;
    fetch('data/status.json?t=' + Date.now())
        .then(r => r.json())
        .then(data => {
            let statusText = data.vitals?.mode || data.status || 'OFFLINE';
            if (data.vitals?.model) statusText += ` (${data.vitals.model})`;
            el.textContent = `[SYSTEM] ${statusText}`;
            
            // Color coding
            if (data.vitals?.mode === 'SWAPPING' || data.vitals?.mode === 'DOWNSHIFTING') {
                el.style.color = '#ffc107'; 
            } else if (data.status === 'ONLINE' || data.status === 'IDLE') {
                el.style.color = '#28a745'; 
            } else {
                el.style.color = '#666';
            }
        })
        .catch(err => console.error("System status poll failed", err));
}

let typingTimer;
const AUTO_SAVE_DELAY = 5000; // 5 seconds

function initEditor() {
    if (!document.getElementById('workspace-content')) return;
    editor = new EasyMDE({
        element: document.getElementById('workspace-content'),
        forceSync: true,
        spellChecker: false,
        autosave: { enabled: false },
        status: ["lines", "words"],
        toolbar: ["bold", "italic", "heading", "|", "quote", "unordered-list", "ordered-list", "|", "link", "image", "|", "preview", "side-by-side", "fullscreen", "|", "undo", "redo"]
    });

    editor.codemirror.on("change", () => {
        if (isLoading) return;
        
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "user_typing", timestamp: Date.now() }));
            
            // Auto-save logic
            clearTimeout(typingTimer);
            typingTimer = setTimeout(window.saveWorkspace, AUTO_SAVE_DELAY);
        }
    });
}

function appendMsg(text, type = 'system-msg', source = 'System', channel = 'chat') {
    const target = channel === 'insight' ? insightConsole : chatConsole;
    
    if (channel === 'whiteboard' || channel === 'workspace') {
        if (editor) editor.value(text);
        return;
    }

    const msg = document.createElement('div');
    // If source is System, we force system-msg type to get gray style
    const msgType = (source && source.toLowerCase() === "system") ? "system-msg" : type;
    msg.className = `message ${msgType}`;
    const prefix = source ? `[${source.toUpperCase()}]: ` : "";
    msg.textContent = `${prefix}${text}`;
    
    // Primary Console Routing: Mute Brain output in main chat
    const isBrain = channel === 'insight' || source.toLowerCase().includes('brain');
    if (!isBrain) {
        chatConsole.appendChild(msg);
        chatConsole.scrollTop = chatConsole.scrollHeight;
    }

    // Insight Panel Routing: Brain messages only
    if (isBrain) {
        const iMsg = msg.cloneNode(true);
        insightConsole.appendChild(iMsg);
        insightConsole.scrollTop = insightConsole.scrollHeight;
    }
}

function updateFileTree(files) {
    if (!fileTree) return;
    let html = '<ul style="list-style: none; padding-left: 5px;">';
    html += '<li class="tree-item" style="font-weight:bold; color:#aaa;">📂 Workspace</li>';
    const workspaceFiles = [...(files.drafts || []), ...(files.workspace || [])];
    if (workspaceFiles.length > 0) {
        [...new Set(workspaceFiles)].forEach(f => {
            const isActive = activeFile === f;
            html += `<li class="tree-item file" onclick="selectFile('${f}')" style="${isActive ? 'color:var(--accent-color); font-weight:bold;' : ''}">
                📄 ${f} ${isActive ? '<span class="active-file-tag">OPEN</span>' : ''}
            </li>`;
        });
    } else {
        html += '<li style="padding-left:10px; color:#444; font-size:0.7rem;">(no files found)</li>';
    }
    html += '<li class="tree-item" style="font-weight:bold; color:#aaa; margin-top:10px;">📂 Archives</li>';
    if (files.archive) {
        Object.keys(files.archive).sort().reverse().slice(0, 5).forEach(year => {
            html += `<li style="padding-left:10px; color:#666;">📅 ${year}</li>`;
        });
    }
    html += '</ul>';
    fileTree.innerHTML = html;
}

window.selectFile = (filename) => {
    activeFile = filename;
    activeFilename.textContent = filename;
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "read_file", filename: filename }));
        ws.send(JSON.stringify({ type: "select_file", filename: filename }));
    }
    appendMsg(`Opening ${filename}...`, 'system-msg');
};

async function toggleMic() {
    if (isMicActive) stopMic();
    else await startMic();
}

async function startMic() {
    try {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
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
        appendMsg("Microphone Active. Speak now...", "system-msg");
    } catch (err) {
        appendMsg(`Mic Error: ${err.message}`, "system-msg");
    }
}

function stopMic() {
    isMicActive = false;
    micBtn.classList.remove('active');
    if (micStream) micStream.getTracks().forEach(track => track.stop());
    appendMsg("Microphone Muted.", "system-msg");
}

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
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'status') {
                const label = data.state === 'waiting' ? 'LOBBY' : data.state.toUpperCase();
                appendMsg(`${data.message} [${label}] (v${data.version})`, 'system-msg', 'System');
            } else if (data.type === 'control') {
                if (data.command === 'stop_audio') stopMic();
            } else if (data.type === 'cabinet') {
                updateFileTree(data.files);
            } else if (data.type === 'file_content') {
                if (editor) {
                    isLoading = true;
                    editor.value(data.content);
                    isLoading = false;
                }
                appendMsg(`${data.filename} loaded.`, 'system-msg');
            } else if (data.brain) {
                appendMsg(data.brain, "brain-msg", data.brain_source, data.channel || 'chat');
            } else if (data.text) {
                appendMsg(data.text, "user-msg", "Hearing...");
            }
        };
        ws.onclose = () => {
            statusDot.className = 'status-dot offline';
            setTimeout(connect, 5000);
        };
    } catch (e) { console.error(e); }
}

function sendMessage() {
    const text = inputEl.value.trim();
    if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;
    appendMsg(text, "user-msg", "Me");
    ws.send(JSON.stringify({ type: "text_input", content: text }));
    inputEl.value = "";
}

window.saveWorkspace = () => {
    if (!editor || !ws || ws.readyState !== WebSocket.OPEN) return;
    const content = editor.value();
    if (!activeFile) {
        appendMsg("No file open to save.", "system-msg");
        return;
    }
    ws.send(JSON.stringify({ 
        type: "workspace_save", 
        filename: activeFile, 
        content: content 
    }));
    appendMsg(`Saved ${activeFile}. Agents notified.`, "system-msg");
};

// Global Listeners
if (sendBtn) sendBtn.addEventListener('click', sendMessage);
if (micBtn) micBtn.addEventListener('click', toggleMic);
if (inputEl) {
    inputEl.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
    inputEl.addEventListener('input', () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "user_typing", timestamp: Date.now() }));
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    console.log("[INIT] DOM Loaded. Initializing Workbench...");

    // --- Resizer Logic ---
    const resizer = document.getElementById('resizer');
    const consoleRow = document.getElementById('console-row');
    const workspaceContainer = document.getElementById('workspace-container');

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
                // Ensure workspace fills the remaining space minus some padding for input
                workspaceContainer.style.flex = "1";
                workspaceContainer.style.height = "auto"; 
                
                // Explicitly tell EasyMDE to refresh its internal heights
                if (editor && editor.codemirror) {
                    editor.codemirror.refresh();
                }
            }
        });
        document.addEventListener('mouseup', () => { isResizing = false; });
    }

    try {
        initEditor();
    } catch (e) {
        console.error("[INIT] Editor failed:", e);
    }
    
    try {
        connect();
        pollSystemStatus();
        setInterval(pollSystemStatus, 5000);
    } catch (e) {
        console.error("[INIT] Connection failed:", e);
    }
});
