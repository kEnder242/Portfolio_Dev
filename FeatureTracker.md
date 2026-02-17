# Feature Tracker (FeatureTracker.md)
**Status:** ACTIVE | **Version:** 1.0 (Initial Identity)
**Design Reference:** [FeatureTrackerDesign.md](./FeatureTrackerDesign.md)

## 🎯 Goal Section
Use this file as a guiding tool when refactoring code to minimize feature drift and prevent the accidental loss of critical logic. This is the **Map Room**—it tracks the "Why" and identifies how we want the system to be based on explicit architectural buy-in.

## 🛡️ Guardrail Section
*   **Architectural Buy-in:** Features must not be removed without explicit buy-in from the Human Architect.
*   **Change Control:** Any change to feature identity, code location, or core implementation strategy requires architectural review.
*   **Semantic Anchors:** Features use `[FEAT-XXX]` tags. Use `grep "[FEAT-XXX]"` to find implementation details in the silicon.

---

## 🏛️ Group I: Silicon & Orchestration (HomeLabAI Core)

| ID | Feature | How -> Why | Where (Code) | Research / BKM | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[FEAT-001]` | **Unity Pattern** | Llama-3.2-3B + vLLM -> Ensures 3.6GB VRAM headroom for resident EarNode on 11GB silicon. | `start_vllm.sh`, `lab_attendant.py` | BKM: Weights & Measures | `smoke_gate.py` |
| `[FEAT-002]` | **Montana Protocol** | Sequential Init + Logger Control -> Recovered from Feb 11 "Total Driver Loss." Prevents logger hijacking by NeMo/Chroma. | `acme_lab.py`, `loader.py` | Retrospective: Bladerunner Forensic | `stability_marathon_v2.py` |
| `[FEAT-003]` | **Lab Attendant** | Non-blocking Background Boot -> Decouples orchestrator from inference engine to prevent Signal 9 timeout crashes. | `lab_attendant.py` | BKM: Boot Protocol v4 | `/heartbeat` |
| `[FEAT-016]` | **Autonomous Watchdog**| Active Port Verification (8765) -> Automatically restarts Lab Server if port bind is lost, preventing zombie states. | `lab_attendant.py` | BKM: Resilience Ladder | `vram_watchdog_loop` |
| `[FEAT-017]` | **Stable Bootstrapper** | `start_lab.sh` + `/wait_ready` -> Provides a bulletproof one-liner for cold-starting the full stack with verified readiness. | `start_lab.sh` | BKM: Unity Stabilization | `./start_lab.sh` |
| `[FEAT-004]` | **Shadow Dispatch** | Predictive Intent Detection -> Anticipates strategic queries during transcription to "warm up" the Brain. | `acme_lab.py` | Paper: TTCS (Self-Correction) | `test_pi_flow.py` |

---

## 🧠 Group II: Bicameral Cognition (The Mind)

| ID | Feature | How -> Why | Where (Code) | Research / BKM | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[FEAT-005]` | **Semantic Map Consumer** | Pinky reads `semantic_map.json` -> Grounds intuitive triage in 18 years of historical focal points. | `pinky_node.py` | BKM: Strategic Vibe Check | `test_resurrection_tools.py` |
| `[FEAT-006]` | **Bicameral Triage** | Pinky (Gateway) vs Brain (Reasoning) -> Minimizes latency by using the lightweight model for triage and the heavy for logic. | `acme_lab.py`, `nodes/` | Paper: Bicameral Mind (Julian Jaynes) | `test_dispatch_logic.py` |
| `[FEAT-007]` | **RLM Research Pattern** | Recursive LM Breadcrumbs -> Allows Pinky to follow technical threads through the search index. | `archive_node.py` | Paper: Recursive LMs | `test_tool_registry.py` |

---

## 📜 Group III: Static Synthesis (Portfolio Pipeline)

| ID | Feature | How -> Why | Where (Code) | Research / BKM | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[FEAT-008]` | **Librarian/Nibbler Loop** | Two-stage Scan -> Classifies files first to respect Prometheus load, then nibbles granular JSONs. | `scan_librarian.py`, `nibble.py` | BKM: Smoke & Mirrors Architecture | `scan_state.json` |
| `[FEAT-009]` | **Cynical Ranking (0-4)** | Showcase Value Scale -> Ensures only Rank 4 "Star Power" artifacts dominate the public map. | `nibble.py` | BKM: Cynical Curator | `files.html` |
| `[FEAT-010]` | **Nuclear Search Isolation** | DOM Containerization -> Prevents search filtering from clobbering the Mission Control persistent navigation. | `mission-control.js` | BKM: Class 1 Modularity | UI Verification |

---

## 📊 Group IV: Observability & Resilience

| ID | Feature | How -> Why | Where (Code) | Research / BKM | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[FEAT-011]` | **DCGM/RAPL-Sim Telemetry** | Native NVML -> Captures sub-millisecond GPU power/thermal spikes. | `docker-compose.yml`, `pinky_node.py` | NVIDIA DCGM Reference | `monitor.jason-lab.dev` |
| `[FEAT-012]` | **Neural Pager** | Typewriter Alert Log -> Provides a cinematic, severity-aware visualization of system events. | `pager.html`, `notify_pd.py` | BKM: Neural Pager | `/pager.html` |
| `[FEAT-013]` | **Self-Healing Fallback** | Auto-Downshift -> (Backlog) Automated transition from vLLM to Ollama on health-check failure. | `lab_attendant.py` | BKM: Resilience Ladder | `test_vllm_alpha.py` |

---

## 🌍 Group V: The Hybrid Cloud (Airlock)

| ID | Feature | How -> Why | Where (Code) | Research / BKM | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[FEAT-014]` | **Access Request Layer** | The "Knock" Button -> Implements split-policy Cloudflare Zero Trust for guests vs. admin. | `FIELD_NOTES_ARCHITECTURE.md` | BKM: Access Request Pattern | Cloudflare Dashboard |
| `[FEAT-015]` | **Cinematic Trailers** | JPEG Build Pipeline -> Uses `shot-scraper` to provide public snapshots without exposing the internal lab. | `build_site.py`, `www_deploy/` | BKM: WWW Strategy | `www.jason-lab.dev` |

---

## 🏺 Lost Gems (The Resurrection Ledger)
*   `[GIFT-001]` **Mistral-7B Base**: Sidelined Feb 15. Kill Reason: Compute 7.5 VRAM/Graph conflicts. Resurrection Trigger: RTX 5090 or vLLM CUDA Graph optimization for Turing.
*   `[GIFT-002]` **InfluxDB Integration**: Sidelined Jan 2026. Kill Reason: Redundancy with Prometheus/Grafana stack. Resurrection Trigger: Multi-year retention requirements.

## 🚀 Future Requirements
*   **Agentic-R implementation:** Integrating reasoning-as-a-tool for multi-step validation paths.
*   **TTT-Discover:** Autonomous path discovery for silicon validation regressions.
*   **Voice Intercom v2:** Transition from Int16 PCM to WebRTC streaming.
