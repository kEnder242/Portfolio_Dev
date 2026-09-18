/**
 * DNA Card Core Component [FEAT-588 / FEAT-582]
 * Unified, polymorphic rendering for Federated Lab DNA cards across
 * DNA Forge, Writer Studio, and Intercom WYWO.
 * 
 * Includes Tron Neon styling (Default Tron Blue, Glowing Tron Red for Flagged/AR).
 */

(function(window) {
    const DnaCardCore = {
        DOMAINS: ['PHL', 'BKM', 'FEAT', 'WIS', 'GEM', 'VIBE', 'DISC', 'SPRINT', 'RDNA', 'ART'],

        isFlagged(card) {
            if (!card) return false;
            if (card.is_flagged || card.flagged) return true;
            if (card.status === 'flagged' || card.status === 'needs_review') return true;
            if (card.id && card.id.startsWith('AR-')) return true;
            const tags = Array.isArray(card.tags) ? card.tags : (card.tags ? String(card.tags).split(',') : []);
            return tags.some(t => {
                const clean = String(t).trim().toLowerCase().replace(/^#/, '');
                return clean === 'flagged' || clean === 'ar' || clean === 'needs_review' || clean === 'action_required';
            });
        },

        getDomainColor(domain) {
            const map = {
                'PHL': 'var(--chip-phl, #a371f7)',
                'BKM': 'var(--chip-bkm, #3fb950)',
                'FEAT': 'var(--chip-feat, #58a6ff)',
                'WIS': 'var(--chip-wis, #e3b341)',
                'DISC': 'var(--chip-disc, #f0883e)',
                'GEM': '#79c0ff',
                'VIBE': '#ff7b72',
                'SPRINT': '#d2a8ff',
                'RDNA': '#56d364',
                'ART': '#ff9bce'
            };
            return map[domain] || '#58a6ff';
        },

        renderCard(card, options = {}) {
            const isFlagged = this.isFlagged(card);
            const domain = card.domain || (card.id ? card.id.split('-')[0] : 'DNA');
            const cardId = card.id || 'DNA-UNSET';
            const title = card.title || card.topic || card.name || 'Untitled Entry';
            const summary = card.summary || card.core_mandate || card.thesis || card.content || '';
            const tags = Array.isArray(card.tags) ? card.tags : (card.tags ? String(card.tags).split(',').map(t => t.trim()) : []);
            const explicitLinks = Array.isArray(card.explicit_links) ? card.explicit_links : (card.links || []);
            const isDocked = options.isDocked || false;
            const canEdit = options.canEdit !== false;

            const tronClass = isFlagged ? 'tron-card tron-red' : 'tron-card tron-blue';
            const flagBadge = isFlagged ? '<span class="tron-badge-flag">🚨 FLAGGED / AR</span>' : '';

            // Lateral Migration / Re-bucketing options
            const domainOptions = this.DOMAINS.map(d => 
                `<option value="${d}" ${d === domain ? 'selected' : ''}>${d}</option>`
            ).join('');

            return `
                <div class="dna-card-core ${tronClass}" data-card-id="${cardId}" data-domain="${domain}">
                    <div class="dna-card-glow"></div>
                    <div class="dna-card-header">
                        <div class="dna-card-id-row">
                            <span class="dna-card-id" title="DNA Identifier">${cardId}</span>
                            <span class="dna-card-domain-badge" style="border-color: ${this.getDomainColor(domain)}; color: ${this.getDomainColor(domain)}">${domain}</span>
                            ${flagBadge}
                        </div>
                        <div class="dna-card-actions">
                            ${options.showRackAction ? `
                                <button class="dna-btn-action btn-rack ${isDocked ? 'docked' : ''}" data-action="toggle-rack" title="${isDocked ? 'Remove from Bone Rack' : 'Snap to Bone Rack'}">
                                    ${isDocked ? '🦴 In Rack' : '+ Rack'}
                                </button>
                            ` : ''}
                            ${canEdit ? `
                                <button class="dna-btn-action btn-edit" data-action="edit" title="Edit Card">✏️</button>
                            ` : ''}
                        </div>
                    </div>

                    <div class="dna-card-title">${title}</div>

                    <div class="dna-card-body">
                        ${summary ? `<div class="dna-card-summary">${summary}</div>` : ''}
                        ${card.origin_quote ? `<blockquote class="dna-card-quote">"${card.origin_quote}"</blockquote>` : ''}
                        ${card.rationale ? `<div class="dna-card-rationale"><strong>Rationale:</strong> ${card.rationale}</div>` : ''}
                    </div>

                    ${explicitLinks.length > 0 ? `
                        <div class="dna-card-links">
                            <span class="dna-links-label">🔗 Links:</span>
                            ${explicitLinks.map(l => `<span class="dna-link-pill">${l}</span>`).join(' ')}
                        </div>
                    ` : ''}

                    <div class="dna-card-footer">
                        <div class="dna-card-tags">
                            ${tags.map(t => `<span class="dna-tag-pill ${String(t).toLowerCase().includes('ar') || String(t).toLowerCase().includes('flag') ? 'tag-flag' : ''}">#${String(t).replace(/^#/, '')}</span>`).join(' ')}
                        </div>
                        ${canEdit ? `
                            <div class="dna-rebucket-wrap" title="Lateral Re-bucketing">
                                <label class="rebucket-label">Bucket:</label>
                                <select class="dna-rebucket-select" data-action="rebucket">
                                    ${domainOptions}
                                </select>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        },

        injectStyles() {
            if (document.getElementById('dna-card-core-styles')) return;
            const style = document.createElement('style');
            style.id = 'dna-card-core-styles';
            style.textContent = `
                /* Unified Tron Neon Styling for DNA Cards [FEAT-588] */
                .dna-card-core {
                    background: var(--card-bg, #161b22);
                    border-radius: 6px;
                    padding: 14px 16px;
                    position: relative;
                    font-family: var(--font-stack, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace);
                    font-size: 0.85rem;
                    line-height: 1.5;
                    transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    border: 1px solid var(--border-color, #30363d);
                }

                /* Standard Tron Blue Glow */
                .dna-card-core.tron-blue {
                    border-left: 3px solid #58a6ff;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                }
                .dna-card-core.tron-blue:hover {
                    border-color: #58a6ff;
                    box-shadow: 0 0 12px rgba(88, 166, 255, 0.35);
                    transform: translateY(-2px);
                }

                /* Flagged / Action Required: Vibrant Neon Tron Red Glow */
                .dna-card-core.tron-red {
                    border: 1px solid #ff3366 !important;
                    border-left: 4px solid #ff0055 !important;
                    background: linear-gradient(180deg, rgba(255, 0, 85, 0.08) 0%, var(--card-bg, #161b22) 100%) !important;
                    box-shadow: 0 0 14px rgba(255, 0, 85, 0.35), inset 0 0 6px rgba(255, 0, 85, 0.15) !important;
                    animation: tronPulse 3s infinite alternate ease-in-out;
                }
                .dna-card-core.tron-red:hover {
                    box-shadow: 0 0 20px rgba(255, 0, 85, 0.6), inset 0 0 10px rgba(255, 0, 85, 0.25) !important;
                    transform: translateY(-2px);
                }

                @keyframes tronPulse {
                    0% { box-shadow: 0 0 10px rgba(255, 0, 85, 0.25); }
                    100% { box-shadow: 0 0 18px rgba(255, 0, 85, 0.5); }
                }

                .dna-card-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 8px;
                }
                .dna-card-id-row {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    flex-wrap: wrap;
                }
                .dna-card-id {
                    font-family: monospace;
                    font-weight: 700;
                    color: var(--text-color, #c9d1d9);
                    font-size: 0.8rem;
                }
                .dna-card-domain-badge {
                    font-size: 0.65rem;
                    padding: 1px 5px;
                    border-radius: 3px;
                    border: 1px solid;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                }
                .tron-badge-flag {
                    font-size: 0.65rem;
                    background: #ff0055;
                    color: #fff;
                    padding: 1px 6px;
                    border-radius: 3px;
                    font-weight: 800;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                }

                .dna-card-actions {
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }
                .dna-btn-action {
                    background: var(--code-bg, #0d1117);
                    border: 1px solid var(--border-color, #30363d);
                    color: var(--text-color, #c9d1d9);
                    border-radius: 4px;
                    padding: 2px 7px;
                    font-size: 0.72rem;
                    cursor: pointer;
                    transition: all 0.15s ease;
                }
                .dna-btn-action:hover {
                    border-color: #58a6ff;
                    color: #58a6ff;
                }
                .dna-btn-action.btn-rack.docked {
                    background: rgba(86, 211, 100, 0.2);
                    border-color: #56d364;
                    color: #56d364;
                    font-weight: bold;
                }

                .dna-card-title {
                    font-size: 0.95rem;
                    font-weight: 600;
                    color: var(--text-color, #f0f6fc);
                    line-height: 1.35;
                }
                .dna-card-summary {
                    color: #c9d1d9;
                    font-size: 0.82rem;
                    line-height: 1.45;
                }
                .dna-card-quote {
                    margin: 6px 0;
                    padding: 4px 10px;
                    background: rgba(255, 255, 255, 0.03);
                    border-left: 2px solid #8b949e;
                    color: #8b949e;
                    font-style: italic;
                    font-size: 0.78rem;
                }
                .dna-card-rationale {
                    font-size: 0.78rem;
                    color: #8b949e;
                    margin-top: 4px;
                }

                .dna-card-links {
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    flex-wrap: wrap;
                    font-size: 0.72rem;
                    color: var(--sub-color, #8b949e);
                }
                .dna-link-pill {
                    background: rgba(56, 139, 253, 0.15);
                    border: 1px solid rgba(56, 139, 253, 0.3);
                    color: #58a6ff;
                    padding: 1px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                }

                .dna-card-footer {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 8px;
                    margin-top: auto;
                    padding-top: 8px;
                    border-top: 1px solid rgba(255, 255, 255, 0.06);
                    font-size: 0.72rem;
                }
                .dna-card-tags {
                    display: flex;
                    gap: 4px;
                    flex-wrap: wrap;
                }
                .dna-tag-pill {
                    color: #8b949e;
                }
                .dna-tag-pill.tag-flag {
                    color: #ff3366;
                    font-weight: 700;
                }

                .dna-rebucket-wrap {
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }
                .rebucket-label {
                    color: #8b949e;
                    font-size: 0.68rem;
                }
                .dna-rebucket-select {
                    background: var(--code-bg, #0d1117);
                    border: 1px solid var(--border-color, #30363d);
                    color: var(--text-color, #c9d1d9);
                    padding: 1px 4px;
                    border-radius: 3px;
                    font-size: 0.7rem;
                    cursor: pointer;
                }
            `;
            document.head.appendChild(style);
        }
    };

    window.DnaCardCore = DnaCardCore;
})(window);
