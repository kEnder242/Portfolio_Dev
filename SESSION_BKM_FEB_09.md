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
*   `refine_gem.py`: Manual fidelity upgrade. Use to test Brain (4090) vs. Pinky (Mistral) fallback logic.
*   `scan_expertise.py`: Re-index the hierarchical Best Known Method (BKM) directory.

### 3. Critical Fixes (v3.1.9)
*   **Path Traps**: `utils.py` uses `BASE_DIR = os.path.dirname(os.path.abspath(__file__))`. Never use raw relative strings for data paths.
*   **Indentation Scars**: `acme_lab.py` was recovered from a critical indentation error in the tool-routing loop.
*   **Echo Bug**: Removed redundant server-side text echo to fix UI message duplication.

## 📋 The Horizon Backlog
Items identified during the v3.1.9 roll-out:
- [ ] **Round Table Lock**: Pause `mass_scan.py` when Web Intercom detects user activity.
- [ ] **Fallback Dreaming**: Implement 2080 Ti fallback in `dream_cycle.py` if Windows 4090 is offline/busy.
- [ ] **vLLM Benchmarking**: Test migration from Ollama to vLLM for peak serving throughput.
- [ ] **Semantic De-duping**: Implement 95%+ similarity filtering during the `Nibbler` (scan) phase.
- [ ] **TTT-Discover**: RL-based autonomous failure path discovery.

## 💎 High-Fidelity Highlights
*   **Signature Synthesis**: 3x3 CVT Resume Builder is active.
*   **Diamond Highlighting**: Rank 4 entries are now highlighted in Gold with a 💎 icon in the Timeline.
*   **Expertise tab**: Hierarchical BKM storage is now visible in the Artifact Map.
