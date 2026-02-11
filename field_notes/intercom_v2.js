// 🐹 Acme Lab: Workbench Console Logic v3.4.3
console.log("Workbench Console v3.4.3 loading...");

const CONFIG = {
    LOCAL_URL: "ws://localhost:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "3.4.0"
};

let ws = null;
let activeFile = null;
let editor = null;

// UI Elements
const chatConsole = document.getElementById('chat-console');
const insightConsole = document.getElementById('insight-console');
const activeFilename = document.getElementById('active-filename');
const fileTree = document.getElementById('file-tree');
const inputEl = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusDot = document.getElementById('connection-dot');

function initEditor() {
    editor = new EasyMDE({
        element: document.getElementById('workspace-content'),
        forceSync: true,
        spellChecker: false,
        autosave: { enabled: false },
        status: ["lines", "words"],
        toolbar: ["bold", "italic", "heading", "|", "quote", "unordered-list", "ordered-list", "|", "link", "image", "|", "preview", "side-by-side", "fullscreen", "|", "undo", "redo"]
    });
}

function appendMsg(text, type = 'system-msg', source = 'System', channel = 'chat') {
    // 1. Unified Console: Show everything in Pinky's window by default
    // We append to chatConsole regardless of channel for now, as requested.
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    const prefix = source ? `[${source.toUpperCase()}]: ` : "";
    msg.textContent = `${prefix}${text}`;
    chatConsole.appendChild(msg);
    chatConsole.scrollTop = chatConsole.scrollHeight;

    // 2. Insight Console: Duplicate Brain messages here for high-fidelity view
    if (channel === 'insight' || source.toLowerCase() === 'brain') {
        const iMsg = msg.cloneNode(true);
        insightConsole.appendChild(iMsg);
        insightConsole.scrollTop = insightConsole.scrollHeight;
    }
    
    // 3. Auto-route Workspace updates (The Live Thinking path)
    if (channel === 'whiteboard' || channel === 'workspace') {
        if (editor) editor.value(text);
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
        // Request the file content
        ws.send(JSON.stringify({ type: "read_file", filename: filename }));
        // Inform the server of the selection context
        ws.send(JSON.stringify({ type: "select_file", filename: filename }));
    }
    appendMsg(`Opening ${filename}...`, 'system-msg');
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
            } else if (data.type === 'file_content') {
                if (editor) editor.value(data.content);
                appendMsg(`${data.filename} loaded into workspace.`, 'system-msg');
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

window.addEventListener('DOMContentLoaded', () => {
    initEditor();
    connect();
});