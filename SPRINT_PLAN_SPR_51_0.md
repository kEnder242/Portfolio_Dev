# 📜 SPRINT PLAN: SPR-51.0 (Conversational Polish, Deep Thought Refinement, Mobile Crosstalk UI & Thermal Stability)

> **Sprint Goal**: Restore natural conversational flow to Acme Lab by eliminating persona leakage (removing Pinky tics like "Narf!" from Deep Thought via Brain persona grounding), bypassing heavy HyDE/RAG pre-reflections on casual greetings ("hello") using prompt judge classification without hardcoded keywords (BKM-015), un-blocking Deep Thought preamble latency (`[FEAT-455]`), routing `[SYSTEM]` log floods into a compact scrolling Crosstalk Bar for mobile viewports, and implementing thermal/CPU scheduling guardrails (`nice -n 19`, thread caps, thermal throttling watchdog) to prevent host reboots.

---

## 🏛️ Executive Summary & Architectural Focus

| Story | Feature ID | Target / Module | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Story 1** | `FEAT-451` | `src/logic/cognitive_hub.py` | Persona Boundary Hardening: Ground Deep Thought in Brain persona docs; remove Pinky tics ("Narf!", "Poit!") from preambles without ad-hoc regex censorship | **PLANNED** |
| **Story 2** | `FEAT-452` | `src/logic/cognitive_hub.py` | Casual Greeting Fast-Path: Respect prompt judge classification (`t_parsed.get("casual")`) to set `hyde_vector_text = ""` and skip RAG on greetings without hardcoded string arrays (BKM-015) | **PLANNED** |
| **Story 3** | `FEAT-455` | `src/v5/foyer/router.py` & `cognitive_hub.py` | Zero-Latency Un-blocked Async Preamble: Decouple Deep Thought preamble streaming from `request_lock` and resident wake checks to restore instant space-filling pre-reflection | **PLANNED** |
| **Story 4** | `FEAT-453` | `field_notes/intercom_v2.js` / HTML | Mobile Crosstalk Bar System Routing: Route `[SYSTEM]`, `[HEARTBEAT]`, and `[REMOTE]` diagnostic floods into a dedicated scrollable Crosstalk Bar component | **PLANNED** |
| **Story 5** | `LAB-099` | `src/infra/thermal_guard.py` & `delegate.py` | Thermal & Process Scheduling Guardrails: Implement `nice -n 19`, worker thread caps (`OMP_NUM_THREADS=2`), and thermal zone monitoring in `scheduled_tasks_loop()` | **PLANNED** |
| **Story 6** | `FEAT-454` | Integration Gauntlet | End-to-End Sprint 51 Verification Suite & `/grill-me` Interactive Alignment Certification | **PLANNED** |

---

## 🔍 Root Cause Analysis & Empirical Retrospective (The "WHY")

### 1. Empirical Host Reboot & Thermal Investigation (Aug 08, 2026)
* **Observed Failure**: Host `z87-Linux` suffered an unexpected reboot at 11:15 AM PDT during background task execution (`task-2613`).
* **Log Telemetry (`journalctl -b -1`)**:
  ```text
  Aug 08 11:12:17 z87-Linux pcp-pmie[5588]: Severe demand for real memory 69pgsout/s@z87-Linux
  Aug 08 11:12:17 z87-Linux pcp-pmie[5588]: CPU is experiencing thermal throttling 10853%time[cpu0]@z87-Linux ... 10859%time[cpu6]@z87-Linux 10851%time[cpu7]@z87-Linux
  ```
* **Root Cause Breakdown**:
  * **Thermal Throttling**: Background OpenAgent sub-task spawns ran multi-threaded C-extensions across all 8 CPU cores at 100% duty cycle, driving CPU temperatures into severe thermal throttling.
  * **Memory Page Swapping**: High memory pressure triggered disk page swapping (`69 pgsout/s`), which amplified CPU I/O wait and combined with thermal stress to trigger a hardware/kernel reset.
* **Sprint 50 SystemD Fixes Verification Status**:
  * `opencode-core.service`: **LIVE & ACTIVE** (`MemoryHigh=3.0G`, `MemoryMax=3.5G`, `swap max=0B`, 2.7GB free headroom).
  * `earlyoom.service`: **LIVE & ACTIVE** (Custom SIGTERM/SIGKILL thresholds active).
  * **Remaining Action**: Add CPU process priority (`nice -n 19`), limit C-extension worker threads (`OMP_NUM_THREADS=2`), and add a thermal watchdog loop in `scheduled_tasks_loop()`.

---

### 2. Conversational Naturalness & Deep Thought Refinement

#### **A. Persona Bleed & Character Contamination (`FEAT-451`)**
* **The Problem**: Deep Thought pre-reflection outputs occasionally included Pinky catchphrases like `"Narf!"` or `"Zort!"`. Deep Thought is intended to be a calm, strategic, non-interactive analytical stream. Emitting cartoon tics creates an uncanny persona mismatch.
* **BKM Compliance (Zero Regex Censorship)**: Ad-hoc regex string-matching (`re.sub("narf", ...)`) is forbidden as a symptom patch.
* **The Solution**: Ground Deep Thought pre-reflections directly in the **Brain Persona Documentation** within `src/logic/cognitive_hub.py`. The system prompt explicitly enforces that Deep Thought represents the Brain's pre-conscious analytical stream, strictly forbidding Pinky catchphrases.

#### **B. HyDE vs. Casual Greetings — The HyDE Domain Map Contract (`FEAT-452`)**
* **The Problem**: Previously, the preamble prompt used a vague directive (*"For technical, historical, or validation queries, synthesize HyDE..."*), causing Deep Thought to attempt HyDE vector generation on casual turns, status queries, or general chit-chat.
* **The Solution (The HyDE Domain Map)**: Give the pre-reflection model an explicit **Lab Domain Map**. HyDE synthesis is strictly gated: **If the prompt does NOT map to one of these 4 domains, HyDE is BYPASSED (`hyde_vector_text = ""`) and RAG is SKIPPED entirely.**
* **The 4-Domain HyDE Map**:
  1. **`exp_tlm` (Silicon Telemetry)**: PCIe error bursts, RAPL power/thermal caps, NVIDIA GPU metrics, MSR registers, Redfish sensors.
  2. **`exp_bkm` (Validation & SRE BKMs)**: Point-of-failure playbooks, diagnostic shell BKMs, test runner steps, systemd service topologies.
  3. **`exp_for` (Forensic Debugging)**: Kernel panic tracebacks, OOM crash logs, backpressure ledgers, memory pressure root cause analysis.
  4. **`lab_history` (18-Year Acme Lab Archive)**: Historical project notes (2005–2025), career milestones, past sprint retrospectives.
* **Rule**: Greetings (*"hello"*), status checks, general conversation, or meta-questions NOT on the map set `hyde_vector_text = ""` and `vibe = "CASUAL"`. No hardcoded string arrays (BKM-015 compliant).

#### **C. Deep Thought Un-blocking & Latency Retrospective (`FEAT-455`)**
* **Retrospective**: Deep Thought preamble was architected as a zero-latency space-filler while heavy models (vLLM / Round Table) initialize. During recent memory refactorings, pre-reflection was placed *inside* `async with self.request_lock:` and made sequential to resident wake checks (`_wrap_residents_for_sandbox()`).
* **Why It Was Lost**: We **did not tag the un-blocking contract with a dedicated `FEAT` ID**, so the sequence lock swallowed pre-reflection execution.
* **The Solution**: Tagged with `[FEAT-455]`. Preamble streaming will be spawned as an un-gated `asyncio.create_task()` immediately upon WebSocket frame receipt, decoupled from resident wake locks. Broadcast message updated to generic `"Deep Thought pre-reflecting..."` instead of assuming HyDE.

#### **D. Mobile Crosstalk Bar UI (`FEAT-453`)**
* **The Problem**: `[SYSTEM]` heartbeats, `[REMOTE]` wake signals, and judge evaluation telemetry stream directly into the main chat log, swallowing actual dialogue on mobile viewports.
* **The Solution**: Update `field_notes/intercom_v2.js` to route all `[SYSTEM]`, `[HEARTBEAT]`, and `[REMOTE]` messages into a compact, scrollable Crosstalk Bar component, keeping the primary chat window clean for out-loud dialogue.

---

## 📜 Detailed Story Specifications

### 🎭 Story 1: Persona Boundary Hardening (`FEAT-451`) — **[STATUS: PLANNED]**
* **Task Specification**:
  1. Audit `CognitiveHub` prompt templates in `src/logic/cognitive_hub.py`.
  2. Ground Deep Thought pre-reflection in the Brain Persona Documentation: explicit directive that Deep Thought is the Brain's pre-conscious analytical pass, strictly prohibiting Pinky catchphrases (`"Narf!"`, `"Poit!"`, `"Zort!"`). No regex string stripping.
* **Target File**: [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_v5_stabilization.py`

---

### 💬 Story 2: Casual Greeting Fast-Path via Prompt Judge (`FEAT-452`) — **[STATUS: PLANNED]**
* **Task Specification**:
  1. Refactor `_fetch_rag_context()` in `src/logic/cognitive_hub.py` to evaluate the prompt judge's structured output `t_parsed.get("casual")` and `t_parsed.get("vibe")`.
  2. If `casual` is `true` or `vibe` is `"CASUAL"`, set `hyde_vector_text = ""`, bypass HyDE vector generation, and skip ChromaDB RAG retrieval entirely without hardcoded keyword lists (BKM-015).
* **Target File**: [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_qpr_hyde.py`

---

### ⚡ Story 3: Zero-Latency Un-blocked Async Preamble (`FEAT-455`) — **[STATUS: PLANNED]**
* **Task Specification**:
  1. Audit `process_query` lock acquisition in `src/v5/foyer/router.py` & `src/logic/cognitive_hub.py`.
  2. Decouple Deep Thought preamble streaming from `request_lock` and resident wake checks (`_wrap_residents_for_sandbox()`), spawning it as an un-gated `asyncio.create_task()` immediately upon WebSocket frame receipt.
* **Target Files**: [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py), [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_integration_foyer.py`

---

### 📱 Story 4: Mobile Crosstalk Bar System Message Routing (`FEAT-453`) — **[STATUS: PLANNED]**
* **Task Specification**:
  1. Update `field_notes/intercom_v2.js` and `intercom.html` layout to add a scrollable sub-component to the Crosstalk Bar.
  2. Route all `[SYSTEM]`, `[REMOTE]`, and heartbeat messages directly to the Crosstalk Bar, preventing system logs from cluttering main out-loud dialogue on mobile screens.
* **Target Files**: `Portfolio_Dev/field_notes/intercom_v2.js`, `Portfolio_Dev/field_notes/intercom.html`
* **Verification Command**: `python3 field_notes/scan_librarian.py`

---

### 🌡️ Story 5: Thermal & Process Scheduling Guardrails (`LAB-099`) — **[STATUS: PLANNED]**
* **Task Specification**:
  1. Update background workers (`delegate.py`, `nibble_v2.py`) to execute with `nice -n 19 ionice -c 3` and cap C-extension threads (`OMP_NUM_THREADS=2`, `OPENBLAS_NUM_THREADS=2`, `TORCH_NUM_THREADS=2`).
  2. Add a thermal watchdog loop to `scheduled_tasks_loop()` in `src/v5/foyer/router.py` monitoring `/sys/class/thermal/thermal_zone*/temp`. If CPU temperature exceeds 78°C, pause background tasks for 15 seconds.
* **Target Files**: [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py), [`HomeLabAI/src/tests/delegate.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/delegate.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_integration_foyer.py`

---

### 🧪 Story 6: End-to-End Integration Gauntlet Certification (`FEAT-454`) — **[STATUS: PLANNED]**
* **Task Specification**:
  1. Execute unit and integration test suites (`test_integration_foyer.py`, `test_memory_architecture.py`, `test_qpr_hyde.py`).
  2. Conduct interactive `/grill-me` alignment session with user for prompt nuances and Crosstalk UI behavior.
* **Verification Command**: `pytest HomeLabAI/src/tests/test_integration_foyer.py HomeLabAI/src/tests/test_memory_architecture.py`
