/**
 * [FEAT-059 / FEAT-673 / Story 109.12] Always-Live Multi-Node Projection Studio
 * 
 * Multi-node real-time comparative matrix view connecting to live heterogeneous silicon:
 *   - z87-Linux (vLLM 3B AWQ / Pinky Reflex on :8088)
 *   - Node Brain (macOS M5 Air MLX / Bonsai 27B on :8002)
 *   - Node KENDER (RTX 4090 Ollama 32B / Deep Thought on :11434)
 *
 * All mock/stub modes are permanently purged per the Always-Live Mandate.
 */

(function () {
    'use strict';

    const FOYER_BASE_URL = window.location.origin.includes('8765')
        ? window.location.origin
        : 'http://127.0.0.1:8765';

    const DISPATCH_ENDPOINT = `${FOYER_BASE_URL}/api/projection/dispatch`;

    const STATE = {
        activeLens: 'technical',
        isDispatching: false,
        lastResults: null
    };

    /**
     * Dispatch prompt across physical silicon inference fleet.
     */
    async function dispatchMultiNode(promptText, lens = 'technical') {
        if (!promptText || !promptText.trim()) {
            console.warn('[PROJECTION_STUDIO] Empty prompt text.');
            return null;
        }

        STATE.isDispatching = true;
        updateDispatchIndicator(true);

        const payload = {
            prompt: promptText.trim(),
            lens: lens,
            max_tokens: 150
        };

        try {
            const resp = await fetch(DISPATCH_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) {
                throw new Error(`Dispatch failed with HTTP status ${resp.status}`);
            }

            const data = await resp.json();
            STATE.lastResults = data;
            renderFleetCards(data.fleet || []);
            return data;
        } catch (err) {
            console.error('[PROJECTION_STUDIO] Dispatch error:', err);
            renderErrorCards(err.message);
            return null;
        } finally {
            STATE.isDispatching = false;
            updateDispatchIndicator(false);
        }
    }

    /**
     * Render multi-node comparative cards in DOM.
     */
    function renderFleetCards(fleet) {
        const container = document.getElementById('fleet-matrix-container') || document.querySelector('.matrix-view');
        if (!container) return;

        container.innerHTML = '';

        fleet.forEach(nodeData => {
            const card = document.createElement('div');
            card.className = `node-projection-card ${nodeData.status.toLowerCase()}`;
            card.style.cssText = `
                flex: 1;
                min-width: 280px;
                background: #161b22;
                border: 1px solid ${nodeData.status === 'ONLINE' ? '#30363d' : '#8b0000'};
                border-radius: 6px;
                padding: 16px;
                margin: 8px;
                display: flex;
                flex-direction: column;
            `;

            const header = document.createElement('div');
            header.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #21262d; padding-bottom: 8px;';
            header.innerHTML = `
                <strong style="color: #58a6ff;">${nodeData.node}</strong>
                <span style="font-size: 0.8em; padding: 2px 6px; border-radius: 4px; background: ${nodeData.status === 'ONLINE' ? '#238636' : '#da3633'}; color: #fff;">
                    ${nodeData.status}
                </span>
            `;
            card.appendChild(header);

            const body = document.createElement('div');
            body.style.cssText = 'flex: 1; font-family: monospace; font-size: 0.9em; line-height: 1.5; color: #c9d1d9; white-space: pre-wrap;';
            if (nodeData.status === 'ONLINE') {
                body.textContent = nodeData.completion || '(Empty completion received)';
            } else {
                body.innerHTML = `<span style="color: #f85149;">Node Offline: ${nodeData.error || 'Connection timed out'}</span>`;
            }
            card.appendChild(body);

            const footer = document.createElement('div');
            footer.style.cssText = 'margin-top: 12px; padding-top: 8px; border-top: 1px solid #21262d; font-size: 0.75em; color: #8b949e; display: flex; justify-content: space-between;';
            if (nodeData.status === 'ONLINE') {
                footer.innerHTML = `
                    <span>Latency: <strong>${nodeData.latency_ms} ms</strong></span>
                    <span>Tokens: <strong>${nodeData.tokens || 0}</strong></span>
                `;
            } else {
                footer.innerHTML = `<span>Latency: <strong>TIMEOUT</strong></span>`;
            }
            card.appendChild(footer);

            container.appendChild(card);
        });
    }

    function renderErrorCards(errorMsg) {
        const container = document.getElementById('fleet-matrix-container') || document.querySelector('.matrix-view');
        if (!container) return;
        container.innerHTML = `
            <div style="background: #211516; border: 1px solid #da3633; color: #f85149; padding: 16px; border-radius: 6px; margin: 8px;">
                <strong>Fleet Dispatch Error:</strong> ${errorMsg}
            </div>
        `;
    }

    function updateDispatchIndicator(busy) {
        const btn = document.getElementById('dispatch-fleet-btn');
        if (btn) {
            btn.disabled = busy;
            btn.textContent = busy ? 'Dispatching Fleet...' : 'Dispatch Multi-Node Matrix';
        }
    }

    // Export module to global window
    window.ProjectionStudio = {
        dispatch: dispatchMultiNode,
        state: STATE
    };

    document.addEventListener('DOMContentLoaded', () => {
        const btn = document.getElementById('dispatch-fleet-btn');
        if (btn) {
            btn.addEventListener('click', () => {
                const promptInput = document.getElementById('projection-prompt-input');
                const promptText = promptInput ? promptInput.value : 'Verify system matrix bring-up.';
                dispatchMultiNode(promptText, STATE.activeLens);
            });
        }
    });
})();
