const CONFIG = {
    // [SECURITY] Enforce loopback binding for local development
    LOCAL_URL: "ws://127.0.0.1:8765",
    REMOTE_URL: "wss://acme.jason-lab.dev",
    VERSION: "5.0.0-foyer",
    // [FEAT-426] Static fallback key. Overridden at runtime by the Foyer's
    // /status session_token (browsers cannot set custom WS headers, so the key
    // rides the handshake frame as `lab_key`). Empty fallback fails closed.
    LAB_KEY: "",
    SECURITY: {
        REQUIRE_XLAB_KEY: true,
        VALIDATE_ORIGIN: true,
        ALLOWED_ORIGINS: ["http://localhost:8080", "https://notes.jason-lab.dev"]
    }
};

// [PCM CAP] Hard ceiling on a single Int16 PCM chunk: 32768 samples @ 16kHz
// = exactly 1 second of mono PCM. Clamps the mic downsampling allocation so
// a single audio rotate can never daisy-chain Int16 buffer expansion and
// grow the browser heap without a bound.
const PCM_CHUNK_CAP = 32768;

let ws = null;
let isMicActive = false;
let audioContext = null;
let micStream = null;
let processor = null;
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

let lastSystemState = "";
let lastMsgSource = "";
let currentSocketId = "Unknown"; // [FEAT-344] Persistence Tracker
let currentLabKey = ""; // [FEAT-426] X-Lab-Key for WS handshake + heartbeat fetch

// [FEAT-339] Message De-duplication
const seenMsgIds = new Set();
const MAX_SEEN_IDS = 50;

// --- INITIALIZATION ---
let isRestoringHistory = false;

document.addEventListener('DOMContentLoaded', () => {
    initResizer();
    loadHistory();
    connect();
    pollSystemStatus();
    applyCrosstalkBarStyles(document.getElementById('crosstalk-bar'));
    
    // UI Events
    sendBtn.addEventListener('click', sendText);
    textInput.addEventListener('keydown', (e) => { 
        triggerSpeculativePreWarm();
        if (e.key === 'Enter') sendText(); 
    });
    textInput.addEventListener('focus', triggerSpeculativePreWarm);
    micBtn.addEventListener('mouseenter', triggerSpeculativePreWarm);
    micBtn.addEventListener('click', toggleMic);
    document.getElementById('menu-toggle').addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('collapsed');
    });
});

// [FEAT-T22.1 / Story 54.8] Speculative Pre-Warm Trigger
let lastPreWarmTime = 0;
function triggerSpeculativePreWarm() {
    const now = Date.now();
    if (now - lastPreWarmTime < 60000) return; // 60s debounce
    lastPreWarmTime = now;
    try {
        fetch(`${window.location.origin}/attendant/wake`, { method: 'POST' }).catch(() => {});
    } catch (e) {}
}

function loadHistory() {
    try {
        isRestoringHistory = true;
        const history = JSON.parse(sessionStorage.getItem('acme_chat_history') || '[]');
        history.forEach(item => {
            appendMsg(item.text, item.type, item.source, item.channel, false, item.metadata);
        });
        
        const savedFile = sessionStorage.getItem('acme_active_file');
        if (savedFile) {
            activeFilename.textContent = savedFile;
        }
    } catch (e) {
        console.error("Failed to load history", e);
    } finally {
        isRestoringHistory = false;
    }
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
            }
        });
        document.addEventListener('mouseup', () => { isResizing = false; });
    }
}

// --- MESSAGING ---
let lastAppendedText = ""; // [FEAT-344] Brute Force Dedup

function appendMsg(text, type = 'system-msg', source = 'System', channel = 'chat', clear = false, metadata = {}) {
    // [FEAT-453] Diagnostic rows never land here: [SYSTEM]/[HEARTBEAT]/[REMOTE]
    // prefixed text is routed to the scrollable #crosstalk-bar by
    // routeDiagnosticToCrosstalk() before appendMsg() is ever reached.
    // [FEAT-344] Brute Force Dedup: Ignore if exact same text as last message
    if (text === lastAppendedText && source !== 'ME') {
        return;
    }
    lastAppendedText = text;

    const target = channel === 'insight' ? insightConsole : chatConsole;
    
    if (clear) {
        target.innerHTML = `<div class="panel-header">${channel === 'insight' ? "Brain's Insight" : "Pinky's Console"}</div>`;
        if (!isRestoringHistory) {
            sessionStorage.removeItem('acme_chat_history');
        }
    }

    if (!isRestoringHistory && !clear && type !== 'hearing' && !text.includes('Connecting to') && !text.includes('Microphone Active') && !text.includes('Microphone Muted') && !text.includes('Larynx is warming')) {
        try {
            const history = JSON.parse(sessionStorage.getItem('acme_chat_history') || '[]');
            history.push({ text, type, source, channel, metadata });
            if (history.length > 60) history.shift();
            sessionStorage.setItem('acme_chat_history', JSON.stringify(history));
        } catch (e) {}
    }

    const msg = document.createElement('div');
    const msgType = (source && source.toLowerCase() === "system") ? "system-msg" : type;
    
    // [VISUAL THINK] Detect Internal Crosstalk
    const sl_low = source ? source.toLowerCase() : "system";
    const isInternal = sl_low.includes('interjection') || 
                       sl_low.includes('reflex') || 
                       sl_low.includes('intuition') || 
                       sl_low.includes('forensic') || 
                       sl_low.includes('fidelity') || 
                       sl_low.includes('shadow') ||
                       sl_low.includes('lag shield') ||
                       metadata.is_internal;

    msg.className = `message ${msgType} ${isInternal ? 'internal' : ''}`;
    
    const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const sl = source ? source.toLowerCase() : "system";
    let displaySource = source.toUpperCase();

    // [VISUAL THINK] Detect Building Upon state
    let isBuildingUpon = false;
    if (sl.includes('brain') && lastMsgSource.includes('pinky')) isBuildingUpon = true;
    if (sl.includes('pinky') && lastMsgSource.includes('brain')) isBuildingUpon = true;
    
    // [Task 2.5] Visible Consensus: Detect Sovereign Refinement
    const isRefinement = (sl.includes('deep thought') || sl.includes('the brain (failover)')) && (lastMsgSource.includes('brain') || lastMsgSource.includes('pinky'));
    
    lastMsgSource = sl;

    // [FEAT-118] Resonant Oracle Badge (Text-Only)
    if (metadata.oracle_category) {
        displaySource += ` (STATE: ${metadata.oracle_category})`;
    }
    
    // Update class with refinement
    if (isRefinement) msg.classList.add('refinement-msg');
    
    // [FEAT-344] Visible Physical Truth: Prepend SID and PID to source
    if (currentSocketId && source.toLowerCase() !== "system") {
        let signature = `[SID: ${currentSocketId}]`;
        if (metadata.hub_pid) signature += ` [PID: ${metadata.hub_pid}]`;
        displaySource += ` ${signature}`;
    }

    // [FEAT-120] Context Transparency: Prepend clickable refs
    if (metadata.sources && metadata.sources.length > 0) {
        const sourceLinks = metadata.sources.map(s => 
            `<a href="#" onclick="openFile('${s}'); return false;" style="color:var(--accent-color); text-decoration:none; margin-right:5px;">[Ref: ${s}]</a>`
        ).join('');
        text = `${sourceLinks} ${text}`;
    }

    // [FEAT-232] Relay Metadata & Feedback
    let metaHtml = '';
    if (metadata.topic || metadata.fuel !== undefined) {
        const topic = metadata.topic || 'Casual';
        const fuel = metadata.fuel || 0.0;
        const fuelPct = Math.min(100, fuel * 100);
        
        metaHtml = `
            <div class="relay-meta">
                <span>TOPIC: ${topic}</span>
                <span>FUEL: <div class="fuel-gauge"><div class="fuel-fill" style="width: ${fuelPct}%"></div></div></span>
                <div class="feedback-btns">
                    <button class="feedback-btn up" title="Promote Logic" onclick="sendFeedback(this, 'UP', '${topic}', ${fuel}, '${source}')">⬆️</button>
                    <button class="feedback-btn down" title="Demote Logic" onclick="sendFeedback(this, 'DOWN', '${topic}', ${fuel}, '${source}')">⬇️</button>
                </div>
            </div>
        `;
    }
    
    const isSystem = sl_low === 'system';
    const text_low = text.toLowerCase();
    const isSystemStrategic = (isSystem) && (text_low.includes('strategic') || text_low.includes('engaging'));

    // [Task 16.2] Markdown Pop via Marked.js
    let formattedText = text;
    
    // Check if the response is a JSON block to pretty-print
    let isJSON = false;
    let jsonFormatted = '';
    const trimmed = text.trim();
    if (trimmed.startsWith('{') && trimmed.endsWith('}')) {
        try {
            const obj = JSON.parse(trimmed);
            jsonFormatted = JSON.stringify(obj, null, 2);
            isJSON = true;
        } catch (e) {}
    }

    if (isJSON) {
        const esc = (unsafe) => unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        formattedText = `<pre class="json-pretty-print" style="white-space: pre-wrap; font-family: monospace; background: var(--bg-card); padding: 8px; border-radius: 4px; border: 1px solid var(--border-color); font-size: 0.85em; margin: 5px 0;">${esc(jsonFormatted)}</pre>`;
    } else if (!isSystem && window.marked) {
        formattedText = marked.parse(text);
    }
    
    if (isSystem && !isSystemStrategic) {
        msg.innerHTML = `
            <div class="msg-body system-inline">
                <span class="msg-time">${time}</span>
                <span class="msg-source ${sl}">[${displaySource}]</span>
                ${formattedText}
            </div>
        `;
    } else {
        msg.innerHTML = `
            <div class="msg-header">
                <span class="msg-time">${time}</span>
                <span class="msg-source ${sl}">[${isBuildingUpon ? '↳ ' : ''}${displaySource}]</span>
            </div>
            <div class="msg-body">${formattedText}</div>
            ${metaHtml}
        `;
    }
    
    // Fix: Routing Logic - [FEAT-222] Source-First Authority
    
    // [FEAT-224] Brain (Signal or Result) and Shadow (Intuition) always go to the Right
    const isBrain = sl_low.includes('brain') || sl_low.includes('shadow') || sl_low.includes('deep thought');
    // Pinky (Triage or Reflex) always goes to the Left
    const isPinky = sl_low.includes('pinky');
    // System strategic messages go to the Right
    
    if (isBrain || isSystemStrategic || channel === 'insight') {
        insightConsole.appendChild(msg);
        insightConsole.scrollTop = insightConsole.scrollHeight;
    } else {
        chatConsole.appendChild(msg);
        chatConsole.scrollTop = chatConsole.scrollHeight;
    }
}

// [FEAT-453] Crosstalk Diagnostic Routing
const DIAGNOSTIC_PREFIX_RE = /^\[(SYSTEM|HEARTBEAT|REMOTE|FOYER|INIT|LOCK|GOVERNOR|LAB|STAGE|PAGER)\]/i;

function getCrosstalkStatusLine() {
    const bar = document.getElementById('crosstalk-bar');
    if (!bar) return null;
    let statusLine = bar.querySelector('.crosstalk-status-line');
    if (!statusLine) {
        statusLine = document.createElement('div');
        statusLine.className = 'crosstalk-status-line';
        statusLine.innerText = bar.innerText; // Preserve markup default ("Nominal...")
        bar.textContent = ''; // Move the default text into the status line
        bar.appendChild(statusLine);
    }
    return statusLine;
}

// [FEAT-453] Enforce the scrollable multi-line crosstalk container spec:
// max-height: 25vh, overflow-y: auto, white-space: normal, font-size: 0.7rem.
// Applied idempotently at load time AND before every diagnostic append, so the
// inline styles always beat the static stylesheet's nowrap/hidden defaults.
function applyCrosstalkBarStyles(bar) {
    if (!bar) return;
    bar.style.maxHeight = '4.5rem';
    bar.style.overflowY = 'auto';
    bar.style.overflowX = 'hidden';
    bar.style.whiteSpace = 'normal';
    bar.style.fontSize = '0.7rem';
    bar.style.height = 'auto';
    bar.style.minHeight = '2.4rem';
}

function routeDiagnosticToCrosstalk(text) {
    const bar = document.getElementById('crosstalk-bar');
    if (!bar) return;

    // [FEAT-453] Convert the bar into a scrollable log container (idempotent).
    applyCrosstalkBarStyles(bar);

    getCrosstalkStatusLine();

    const entry = document.createElement('div');
    entry.className = 'crosstalk-log-entry';
    entry.style.color = '#d29922';
    entry.style.borderTop = '1px solid #1b1b1b';
    entry.style.padding = '2px 0';
    entry.style.wordBreak = 'break-word';
    const stamp = new Date().toISOString().substr(11, 8); // HH:MM:SS UTC
    entry.textContent = `[${stamp} UTC] ${text}`;
    bar.appendChild(entry);

    // Cap at 10 log entries (drop the oldest, keep the status line).
    while (bar.querySelectorAll('.crosstalk-log-entry').length > 10) {
        const oldest = bar.querySelector('.crosstalk-log-entry');
        if (oldest) oldest.remove();
    }

    bar.scrollTop = bar.scrollHeight;
}

function sendText() {
    const content = textInput.value.trim();
    if (!content || !ws || ws.readyState !== WebSocket.OPEN) return;

    // [FEAT] /topic command: Refresh cognitive history buffer
    if (content.startsWith('/topic')) {
        const topicArg = content.slice(6).trim();
        sessionStorage.removeItem('acme_chat_history');
        const msg = topicArg
            ? `Cognitive history buffer refreshed. Topic context: "${topicArg}".`
            : 'Cognitive history buffer refreshed. Topic context reset.';
        appendMsg(msg, 'system-msg', 'System');
        document.dispatchEvent(new CustomEvent('topic-reset', {
            detail: { topic: topicArg || '', timestamp: new Date().toISOString() }
        }));
        textInput.value = '';
        return;
    }

    const request_id = `UI_${Math.random().toString(36).substr(2, 6)}`;
    appendMsg(content, 'user-msg', 'ME');
    lastMsgSource = 'me';
    ws.send(JSON.stringify({ 
        type: "text_input", 
        content: content,
        request_id: request_id
    }));
    textInput.value = '';
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
            // Clamp the Int16 allocation to PCM_CHUNK_CAP so no single
            // processing event can expand browser heap past the 1s PCM
            // ceiling (prevents daisy-chained int16 buffer expansion).
            const inSamples = inputData.length;
            const chunkLen = Math.min(inSamples, PCM_CHUNK_CAP);
            const pcmData = new Int16Array(chunkLen);
            for (let i = 0; i < chunkLen; i++) {
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
// [FEAT-426] X-Lab-Key source: the Foyer exposes its session token via the
// REST /status endpoint on the same host as the WS. Browsers cannot set custom
// WS headers, so the key rides the handshake frame as `lab_key` instead.
async function getLabKey(target) {
    try {
        const statusUrl = target.replace(/^ws/, 'http') + '/status';
        const resp = await fetch(statusUrl, { cache: 'no-store' });
        if (resp.ok) {
            const data = await resp.json();
            if (data.session_token) {
                return data.session_token;
            }
        }
    } catch (e) {
        // Fall through to the static fallback.
    }
    return CONFIG.LAB_KEY || '';
}

async function connect() {
    const targetUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? CONFIG.LOCAL_URL : CONFIG.REMOTE_URL;

    appendMsg(`Connecting to ${targetUrl}...`, 'system-msg');
    try {
        // [FEAT-426] Fetch the session key before opening the socket.
        currentLabKey = await getLabKey(targetUrl);
        ws = new WebSocket(targetUrl);
        window.ws = ws;
        ws.onopen = () => {
            statusDot.className = 'status-dot online';
            ws.send(JSON.stringify({ 
                type: "handshake", 
                version: CONFIG.VERSION,
                client: "intercom",
                lab_key: currentLabKey
            }));
        };
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            console.log("[WS RECV]", data);
            
            // [FEAT-433] Asynchronous Sanity Critic Badge Handler
            if (data.type === 'sanity_check') {
                appendMsg(`🛡️ Sanity Verified (Confidence: ${(data.confidence * 100).toFixed(0)}%)`, 'system-msg', 'SanityCritic', 'chat');
                return;
            }
            
            // [FEAT-339] Message De-duplication
            if (data.msg_id) {
                if (seenMsgIds.has(data.msg_id)) {
                    console.log("[WS DROP] Duplicate message:", data.msg_id);
                    return;
                }
                seenMsgIds.add(data.msg_id);
                if (seenMsgIds.size > MAX_SEEN_IDS) {
                    const firstId = seenMsgIds.values().next().value;
                    seenMsgIds.delete(firstId);
                }
            }

            // [FEAT-221] Crosstalk Migration
            if (data.type === 'crosstalk' || data.type === 'status') {
                const bar = document.getElementById('crosstalk-bar');
                if (bar) {
                    // [FEAT-453] Status text targets the dedicated status line so log entries survive
                    const statusLine = getCrosstalkStatusLine();
                    if (data.type === 'status') {
                        if (data.state === "hibernating") {
                            statusLine.innerText = "🌙 HIBERNATING";
                            bar.classList.add('status-hibernating');
                        } else if (data.state === "waking") {
                            statusLine.innerText = "⚡ [IGNITION IN PROGRESS]";
                            bar.classList.remove('status-hibernating');
                        } else if (data.state === "quiesced") {
                            statusLine.innerText = "⚙️ MAINTENANCE (QUIESCED)";
                            bar.classList.remove('status-hibernating');
                        } else if (data.state === "offline") {
                            statusLine.innerText = "💀 OFFLINE";
                            bar.classList.remove('status-hibernating');
                        } else if (data.state === "init") {
                            // [FEAT-265.6] Functional Gate: Distinguish between Up and Vocal
                            if (data.full_lab_ready || data.operational) {
                                statusLine.innerText = "⚡ Mind is OPERATIONAL.";
                            } else {
                                statusLine.innerText = "⏳ SYNCHRONIZING NODES...";
                            }
                            bar.classList.remove('status-hibernating');
                        } else if (data.state === "ready") {
                            // Legacy support for older Hub signals
                            statusLine.innerText = "⚡ Mind is READY.";
                            bar.classList.remove('status-hibernating');
                        } else if (data.state === "working") {
                            statusLine.innerText = `🧠 ${data.message || "THINKING..."}`;
                            bar.classList.remove('status-hibernating');
                        } else if (data.state === "error") {
                            statusLine.innerText = `⚠️ ${data.message || "SYSTEM ERROR"}`;
                            bar.classList.remove('status-hibernating');
                        }
                    } else if (data.type === 'crosstalk') {
                        // [FEAT-453] Diagnostic-prefixed crosstalk never touches the chat panes
                        if (data.brain && DIAGNOSTIC_PREFIX_RE.test(data.brain)) {
                            routeDiagnosticToCrosstalk(data.brain);
                            return;
                        }
                        // Store the current non-crosstalk text if we don't have a better state tracker
                        if (!window.lastStatusMessage) {
                            window.lastStatusMessage = statusLine.innerText;
                        }
                        
                        statusLine.innerText = `⚡ ${data.brain}`;
                        bar.classList.remove('status-hibernating');
                        // Clear after 15s if no new updates
                        if (window.crosstalkTimeout) clearTimeout(window.crosstalkTimeout);
                        window.crosstalkTimeout = setTimeout(() => {
                            // Revert to the last known stable status
                            if (window.lastStatusMessage && !bar.classList.contains('status-hibernating')) {
                                statusLine.innerText = window.lastStatusMessage;
                            }
                        }, 15000);
                    }
                }
                
                if (data.type === 'crosstalk') {
                    // [Task 18.2] Silence verbose triage attempts in main console
                    if (data.brain && data.brain.includes("Triage Attempt")) {
                        return; // Already updated the crosstalk bar above
                    }
                    
                    const sl_low = (data.brain_source || 'System').toLowerCase();

                    // [Story 6] Pretty-print triage JSON instead of dumping raw
                    if (sl_low.includes('triage')) {
                        try {
                            const triage = JSON.parse(data.brain);
                            const formatted = 'Routed to ' + triage.addressed_to + ' | Vibe: ' + triage.vibe + ' | Domain: ' + (triage.domain || 'standard');
                            appendMsg(formatted, 'system-msg', 'Triage', data.channel || 'chat', false, { msg_id: data.msg_id });
                            return;
                        } catch(e) { /* not JSON, fall through */ }
                    }

                    // [Story 6] Pretty-print coherence critic JSON
                    if (sl_low.includes('coherence') || sl_low.includes('critic')) {
                        try {
                            const critic = JSON.parse(data.brain);
                            if (critic.retort) {
                                const scoreStars = '★'.repeat(Math.min(critic.score || 0, 5)) + '☆'.repeat(5 - Math.min(critic.score || 0, 5));
                                const formatted = scoreStars + ' ' + critic.retort;
                                appendMsg(formatted, 'system-msg', 'Coherence Critic', data.channel || 'chat', false, { msg_id: data.msg_id });
                                return;
                            }
                        } catch(e) { /* not JSON, fall through */ }
                    }

                    // [FEAT-453] Log Integration: Persona lines go to chat log; system/stage diagnostic lines go to Crosstalk Bar
                    const isPersona = sl_low.includes('pinky') || sl_low.includes('brain') || sl_low.includes('shadow');
                    if (!isPersona || (data.channel === 'stage') || (data.brain && data.brain.includes('STAGE'))) {
                        routeDiagnosticToCrosstalk(`[${data.brain_source || 'STAGE'}] ${data.brain}`);
                        return;
                    }
                    appendMsg(data.brain, 'brain-msg', data.brain_source || 'System', data.channel || 'chat', false, { msg_id: data.msg_id });
                }
            }

            if (data.type === 'status') {
                if (data.socket_id) {
                    currentSocketId = data.socket_id;
                }
                if (data.message) {
                    let msg = data.message;
                    if (data.socket_id) msg += ` [SID: ${data.socket_id}]`;
                    if (data.version && data.version !== CONFIG.VERSION) {
                        alert(`CACHE_LOCK_VIOLATION: Browser is running Intercom ${CONFIG.VERSION} but the Lab is at ${data.version}. \n\nThis mismatch will break the X-Lab-Key dependency and cause Remote Control errors. \n\nPlease perform a hard-refresh (Ctrl+F5) immediately.`);
                    }
                    // [FEAT-453] All system/diagnostic status lines route to the Crosstalk Bar, not Pinky's main console
                    routeDiagnosticToCrosstalk(msg);
                    return;
                }
            } else if (data.type === 'file_content_request') {
                ws.send(JSON.stringify({ type: "read_file", filename: data.filename }));
            } else if (data.type === 'tool_log') {
                // [SPR_41] Tool Log: Render collapsible card in sidebar
                if (window.renderToolLogEntry) {
                    window.renderToolLogEntry({
                        time: data.time || new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                        node: data.node || 'System',
                        tool: data.tool || 'unknown',
                        params: data.params || null,
                        output_path: data.output_path || null,
                        error: data.error || null,
                        detail: data.detail || null
                    });
                }
            } else if (data.type === 'rag_eval') {
                // [FEAT-454] Render interactive collapsible RAG Eval card with + click expansion
                if (window.renderRagEvalCard) {
                    window.renderRagEvalCard(data);
                } else {
                    const esc = (unsafe) => String(unsafe).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
                    const cardHtml = `
                        <details class="rag-eval-card" style="margin: 6px 0; border: 1px solid #2a2a3a; background: #0b0c10; border-left: 3px solid #7ec8e3; border-radius: 4px; padding: 4px 8px;">
                            <summary style="cursor: pointer; color: #7ec8e3; font-size: 0.78rem; font-weight: bold; user-select: none;">
                                🔍 [RAG EVAL] HyDE: ${esc(data.hyde || 'Direct')} (${data.n_results || 3} docs) <span style="color: #666; font-size: 0.7rem;">[Tier: ${esc(data.tier || '2')}]</span>
                            </summary>
                            <div class="rag-eval-body" style="padding: 8px 4px 4px 4px; font-size: 0.75rem; color: #aaa; border-top: 1px solid #1a1a2e; margin-top: 4px;">
                                <div style="margin-bottom: 4px;"><strong>Query:</strong> ${esc(data.query || '')}</div>
                                <div style="margin-bottom: 4px;"><strong>Doc ID:</strong> <a href="#" onclick="openFile('${esc(data.doc_id || '')}'); return false;" style="color: var(--accent-color); text-decoration: none;">[Ref: ${esc(data.doc_id || '')}]</a></div>
                                <div style="margin-bottom: 4px;"><strong>Raw Context (Click to expand):</strong></div>
                                <pre style="white-space: pre-wrap; font-family: monospace; background: #050508; padding: 6px; border-radius: 3px; border: 1px solid #1a1a2e; max-height: 200px; overflow-y: auto; color: #88c0d0; font-size: 0.72rem;">${esc(data.full_context || data.snippet || '')}</pre>
                            </div>
                        </details>
                    `;
                    appendMsg(cardHtml, 'system-msg', 'System');
                }
            } else if (data.type === 'file_content') {
                activeFilename.textContent = data.filename;
                try {
                    sessionStorage.setItem('acme_active_file', data.filename);
                } catch (e) {}
            } else if (data.brain) {
                // [FEAT-453] Safety net: diagnostic-prefixed brain lines go to the Crosstalk Bar
                if (DIAGNOSTIC_PREFIX_RE.test(data.brain)) {
                    routeDiagnosticToCrosstalk(data.brain);
                    return;
                }
                appendMsg(data.brain, 'brain-msg', data.brain_source || 'Brain', data.channel || 'chat', data.clear || false, {
                    msg_id: data.msg_id, // [FIX] Task 2.4: Bridge the ID
                    hub_pid: data.hub_pid, // [FIX] Task 2.5: Bridge the PID
                    oracle_category: data.oracle_category,
                    sources: data.sources,
                    is_internal: data.is_internal,
                    topic: data.topic,
                    fuel: data.fuel
                });
            } else if (data.type === 'hearing') {
                // [FEAT-233.2] Live Hearing Pipe: Update or create a temporary hearing bubble
                let hearingMsg = document.getElementById('live-hearing-msg');
                if (!hearingMsg) {
                    hearingMsg = document.createElement('div');
                    hearingMsg.id = 'live-hearing-msg';
                    hearingMsg.className = 'message user-msg hearing-active';
                    chatConsole.appendChild(hearingMsg);
                }
                const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
                hearingMsg.innerHTML = `
                    <div class="msg-header">
                        <span class="msg-time">${time}</span>
                        <span class="msg-source me">[HEARING...]</span>
                    </div>
                    <div class="msg-body">${data.text}</div>
                `;
                chatConsole.scrollTop = chatConsole.scrollHeight;
            } else if (data.type === 'final') {
                // [FEAT-233.2] Replace hearing bubble with permanent final transcript
                const hearingMsg = document.getElementById('live-hearing-msg');
                if (hearingMsg) hearingMsg.remove();
                
                // acme_lab.py sends tagged_query: f"[ME] {query}"
                const cleanText = data.text.replace("[ME] ", "");
                appendMsg(cleanText, 'user-msg', 'Me (Voice)');
                lastMsgSource = 'me';
            }
        };
        ws.onclose = async () => {
            statusDot.className = 'status-dot offline';

            // [FEAT-314] State-Aware Reconnect: Poll Attendant before retrying
            const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
            const hbUrl = isLocal ? 'http://localhost:9999/heartbeat' : 'https://pager.jason-lab.dev/heartbeat';

            try {
                const response = await fetch(hbUrl, { headers: { 'X-Lab-Key': currentLabKey || 'unknown' } });
                const hb = await response.json();
                const reason = hb.vitals?.reason || '';

                if (["SAFE_PILOT", "RECOVERY", "REST_API_START", "VLLM_CRASH_RECOVERY"].includes(reason)) {
                    appendMsg("⚡ [SILICON_RESET] Lab is warming its anchors. Standing by...", "system-msg", "System", "chat", true);
                    setTimeout(connect, 10000); // 10s wait during ignition
                    return;
                }
            } catch (e) {
                // If Attendant is down too, use standard 5s backoff
            }

            appendMsg("Disconnected. Reconnecting in 5s...", "system-msg");
            setTimeout(connect, 5000);
        };

    } catch (err) {
        appendMsg(`Connection Error: ${err.message}`, 'system-msg');
    }
}

function openFile(fn) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "read_file", filename: fn }));
    }
}


async function pollSystemStatus() {
    try {
        const resp = await fetch('data/status.json?t=' + Date.now());
        const data = await resp.json();
        const vitals = data.vitals || {};
        const mode = vitals.mode || "OLLAMA";
        const model = vitals.model || "None";
        const newState = `${mode}: ${model}`;
        
        if (newState !== lastSystemState) {
            appendMsg(newState, 'system-msg', 'System');
            lastSystemState = newState;
        }
    } catch (err) {
        console.error("Status poll failed", err);
    }
    setTimeout(pollSystemStatus, 10000);
}

function sendFeedback(btn, vote, topic, fuel, source) {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    
    // Toggle active state
    const parent = btn.parentElement;
    parent.querySelectorAll('.feedback-btn').forEach(b => {
        b.classList.remove('active-up', 'active-down');
    });
    btn.classList.add(vote === 'UP' ? 'active-up' : 'active-down');
    
    // Send to Hub
    ws.send(JSON.stringify({
        type: "relay_feedback",
        vote: vote,
        topic: topic,
        fuel: fuel,
        source: source,
        timestamp: new Date().toISOString()
    }));
    
    console.log("[FEEDBACK] Sent:", { vote, topic, fuel, source });
}

// Tool Log: Global render helper
window.renderToolLogEntry = function(entry) {
    const container = document.getElementById('tool-log-container');
    const countBadge = document.getElementById('tool-log-count');
    if (!container) return;

    // Remove empty placeholder if present
    const empty = container.querySelector('.tool-empty');
    if (empty) empty.remove();

    // Cap at 50 entries (remove oldest)
    while (container.children.length >= 50) {
        container.removeChild(container.lastElementChild);
    }

    const card = document.createElement('details');
    card.className = 'tool-card';

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    card.innerHTML = `
        <summary>
            <span class="tool-timestamp">${entry.time || '--:--:--'}</span>
            <span class="tool-node-badge">${entry.node || '?'}</span>
            <span class="tool-name">${entry.tool || 'unknown_tool'}</span>
        </summary>
        <div class="tool-card-body">
            ${entry.params ? `<div class="param-row"><span class="param-key">params:</span><span class="param-val">${escapeHtml(JSON.stringify(entry.params))}</span></div>` : ''}
            ${entry.output_path ? `<div class="param-row"><span class="param-key">output:</span><a class="output-link" href="file://${entry.output_path}" target="_blank">${entry.output_path}</a></div>` : ''}
            ${entry.error ? `<div class="param-row" style="color:#e57373;"><span class="param-key">error:</span><span class="param-val">${escapeHtml(entry.error)}</span></div>` : ''}
            ${entry.detail ? `<div style="margin-top:4px;color:#888;">${escapeHtml(entry.detail)}</div>` : ''}
        </div>
    `;

    // Insert newest at top
    container.insertBefore(card, container.firstChild);

    // Update badge count
    if (countBadge) {
        countBadge.textContent = container.querySelectorAll('.tool-card').length;
    }
};

