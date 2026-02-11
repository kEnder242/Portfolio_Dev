// 🐹 Acme Lab: Workbench Console Logic v3.4.0
console.log("Workbench Console v3.4.0 loading...");

const CONFIG = {
    LOCAL_URL: "ws://localhost:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "3.4.0"
};

let ws = null;
let activeFile = null;

// UI Elements
const chatConsole = document.getElementById('chat-console');
const insightConsole = document.getElementById('insight-console');
const whiteboard = document.getElementById('whiteboard-content');
const activeFilename = document.getElementById('active-filename');
const fileTree = document.getElementById('file-tree');
const inputEl = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusDot = document.getElementById('connection-dot');

function appendMsg(text, type = 'system-msg', source = 'System', channel = 'chat') {
    const target = channel === 'insight' ? insightConsole : chatConsole;
    
    // Auto-route Whiteboard updates
    if (channel === 'whiteboard') {
        whiteboard.value = text;
        return;
    }

    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    const prefix = source ? `[${source.toUpperCase()}]: ` : "";
    msg.textContent = `${prefix}${text}`;
    
    target.appendChild(msg);
    target.scrollTop = target.scrollHeight;
}

function updateFileTree(files) {
    if (!fileTree) return;
    let html = '<ul style="list-style: none; padding-left: 5px;">';
    
    // Archive Section
    html += '<li class="tree-item" style="font-weight:bold; color:#aaa;">📂 Archives</li>';
    if (files.archive) {
        Object.keys(files.archive).sort().reverse().slice(0, 5).forEach(year => {
            html += `<li style="padding-left:10px; color:#666;">📅 ${year}</li>`;
        });
    }

    // Workspace Section
    html += '<li class="tree-item" style="font-weight:bold; color:#aaa; margin-top:10px;">📂 Workspace</li>';
    if (files.drafts) {
        files.drafts.forEach(f => {
            const isActive = activeFile === f;
            html += `<li class="tree-item file" onclick="selectFile('${f}')" style="${isActive ? 'color:var(--accent-color); font-weight:bold;' : ''}">
                📄 ${f} ${isActive ? '<span class="active-file-tag">OPEN</span>' : ''}
            </li>`;
        });
    }
    
    html += '</ul>';
    fileTree.innerHTML = html;
}

window.selectFile = (filename) => {
    activeFile = filename;
    activeFilename.textContent = filename;
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "select_file", filename: filename }));
    }
    appendMsg(`Opened ${filename} for editing.`, 'system-msg');
    // Reload tree to show 'OPEN' tag
    // (This will happen automatically on next server sync)
};

function connect() {
    const targetUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? CONFIG.LOCAL_URL : CONFIG.REMOTE_URL;

    try {
        ws = new WebSocket(targetUrl);
        ws.onopen = () => {
            statusDot.className = 'status-dot online';
            ws.send(JSON.stringify({ type: "handshake", version: CONFIG.VERSION }));
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'cabinet') {
                updateFileTree(data.files);
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

// Global Listeners
if (sendBtn) sendBtn.addEventListener('click', sendMessage);
if (inputEl) inputEl.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

window.addEventListener('DOMContentLoaded', connect);