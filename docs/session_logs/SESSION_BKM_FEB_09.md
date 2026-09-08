# Session BKM: Feb 09, 2026
**Topic:** v3.1.9 Implementation, Architecture Hardening, and Technical Architect Toolkit.

## 🛠️ Cold-Start Protocol & Debug Toolkit
If the system is reset or restarted, follow these anchors:

### 1. Environment Requirements
All background tasks and scanner scripts require an explicit `PYTHONPATH` to resolve hardened absolute utility paths:
`export PYTHONPATH=$PYTHONPATH:$(pwd)/Portfolio_Dev/field_notes`

### 2. Debug Tools
*   `dump_stream.py`: View the "short-term memory" (interaction logs) currently waiting for synthesis.
*   `clean_duplicates.py`: Manual archive maintenance to remove redundant entries.
*   `refine_gem.py`: Manual fidelity upgrade. Use to test Brain (4090) vs. Pinky (Llama-3.2-3B) fallback logic.
*   `scan_expertise.py`: Re-index the hierarchical Best Known Method (BKM) directory.

### 3. Critical Fixes (v3.1.9)
*   **Path Traps**: `utils.py` uses `BASE_DIR = os.path.dirname(os.path.abspath(__file__))`. Never use raw relative strings for data paths.
*   **Indentation Scars**: `acme_lab.py` was recovered from a critical indentation error in the tool-routing loop.
*   **Echo Bug**: Removed redundant server-side text echo to fix UI message duplication.

## 📋 The Horizon Backlog
Items identified during the v3.1.9 roll-out:
- [x] **Modular Sidebar**: Switched to Web Components (mission-control.js) for single-point navigation updates.
- [x] **Lab Status Center**: Unified Grafana telemetry and alert logs into `status.html`.
- [x] **Notification Gatekeeper**: Implemented `notify_gatekeeper.py` to triage alerts (Silent info/warn, Live critical).
- [x] **Dead-Man's Switch**: Automated CRITICAL alert if Intercom port 8765 is down for >5 minutes.
- [x] **vLLM V1 Pilot**: Migrated RTX 2080 Ti to vLLM AWQ stack for high-throughput serving.
- [x] **Semantic De-duper**: Implemented 85% fuzzy threshold in `nibble_v2.py`.
- [ ] **Fallback Dreaming**: Port Pinky fallback to memory consolidation.

## 💎 High-Fidelity Highlights
*   **Signature Synthesis**: 3x3 CVT Resume Builder is active.
*   **Diamond Highlighting**: Rank 4 entries are now highlighted in Gold with a 💎 icon in the Timeline.
*   **Expertise tab**: Hierarchical BKM storage is now visible in the Artifact Map.
