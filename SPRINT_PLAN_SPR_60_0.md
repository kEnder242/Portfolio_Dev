# 🚀 Sprint Plan SPR-60.0: Systematic Modular Satellite Refactoring & Boundary Testing

**Sprint:** 60.0  
**Date:** August 25, 2026  
**Status:** PLANNING & ARCHITECTURAL STAGING  
**Theme:** *Systematic Decomposition via the Modular Satellite Pattern (Order, Simplicity & Zero-Thrash Boundaries)*

---

## 🎯 Executive Summary & Architectural Philosophy

Following the certified success of Sprint 59.0 (where 4 isolated satellite services were cleanly delegated with 149/149 passing unit tests and 0% regression), Sprint 60.0 applies this **Modular Satellite Service Pattern** to systematically decouple the largest remaining monolithic orchestrators: [`CognitiveHub`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py) (~1,900 lines) and [`router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py) (~1,600 lines).

Our guiding law is **Strict Phasing & Minimal Blast Radius**:
1. Tackle pure functional transformations first (**Phase 1**).
2. Tackle isolated OS/GC background loops second (**Phase 2**).
3. Tackle deterministic binary audio framing third (**Phase 3**).
4. **Hard-Gate & Prevent** high-coupling refactors like `triage_engine` to eliminate live streaming regressions.

---

## 🛡️ Preventative Boundary: The `triage_engine` Exclusion Law

> [!WARNING]
> **ARCHITECTURAL BOUNDARY: `triage_engine` IS EXCLUDED FROM SPRINT 60 REFACTORING.**

### **Rationale & Failure Modes Prevented:**
1. **Deep Asynchronous Coupling**: In `cognitive_hub.py:L740-960`, the triage pass is entangled with 7 concurrent orchestrator systems: `self._process_node_stream()`, live WebSocket `broadcast()` crosstalk events, `self.request_lock`, `self.role_tokens` priority routing, `self.turn_thought_trace`, and remote Deep Thought reachability health probes.
2. **Timing & Handshake Fragility**: Subagent delegation of `triage_engine` would require passing 8+ async callbacks. An off-by-one async cancellation or unhandled exception in token generation will freeze the entire live voice chat session.
3. **Critical Path Latency**: Triage is the sub-100ms conversational gateway. It is working reliably and certified; refactoring it now yields high risk for negligible structural gain.

**The Rule**: `triage_engine` remains unified inside `CognitiveHub` throughout Sprint 60.

---

## 🧪 Testability & Boundary-Level Mocking Strategy

Monolithic orchestrator testing (`test_relay_interest_buildup.py`, `test_strategic_live_fire.py`) required mocking 6+ resident nodes, sensory managers, and async queues, resulting in fragile tests that broke on harmless logging changes.

By extracting standalone satellites at pure functional boundaries, testability improves by an order of magnitude:

```
┌───────────────────────────────────────┬─────────────────────────────────────────────────────────────────┐
│ Monolithic Testing (Brittle)          │ Satellite Boundary Testing (Robust)                             │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ • Mocks CognitiveHub + 5 nodes        │ • Zero mocks for internal state: pure input -> output           │
│ • Simulates complex async event loops │ • Synthetic PCM byte fixtures test byte alignment in 0.01s     │
│ • Tests break on broadcast log format │ • Tempfile isolation tests atomic file swaps with zero side-eff │
│ • Slow (~25s test gauntlet)           │ • Blazing fast (<0.1s unit assertions per module)              │
└───────────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Granular Refactoring Stories (Phases 1–3)

### **Story 60.1: [FEAT-145/REF-01] Override Parser Satellite (`override_parser.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Source Lines**: [`cognitive_hub.py:L713-738, L1676-1740`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L713)
* **Target Files**:
  * `HomeLabAI/src/logic/override_parser.py` (New Greenfield Module)
  * `HomeLabAI/src/tests/test_override_parser.py` (New Test Suite)
* **Design & Interfaces**:
  ```python
  class OverrideParser:
      @staticmethod
      def is_override_query(turn: str) -> tuple[bool, Optional[str]]:
          """Detects GEM-xxxx / BKM override syntax (BKM-015 compliant)."""

      @staticmethod
      async def parse_override(gem_id: str, turn: str, resident_caller) -> Optional[dict]:
          """Invokes resident to parse schema updates."""

      @staticmethod
      def save_override(gem_id: str, updates: dict, overrides_path: str = None) -> bool:
          """Atomically updates overrides.json via BKM-022 .tmp + os.replace."""
  ```
* **Delegation Safety**: 🟢 **100% Safe**. Pure parsing + JSON persistence.
* **Verification**: `test_override_parser.py` verifying GEM extraction, invalid syntax rejection, and atomic JSON file updates.

---

### **Story 60.2: [LAB-095/LAB-096/LAB-099/REF-02] Maintenance Sweeper Satellite (`maintenance_sweeper.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Source Lines**: [`router.py:L1437-1530`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L1437)
* **Target Files**:
  * `HomeLabAI/src/v5/foyer/maintenance_sweeper.py` (New Greenfield Module)
  * `HomeLabAI/src/tests/test_maintenance_sweeper.py` (New Test Suite)
* **Design & Interfaces**:
  ```python
  class MaintenanceSweeper:
      @staticmethod
      def check_cpu_thermal_throttle(threshold_milli: int = 78000) -> tuple[bool, float]:
          """[LAB-099] Reads /sys/class/thermal/thermal_zone* with non-Linux mock fallback."""

      @staticmethod
      def run_heap_scavenger() -> int:
          """[LAB-096] Executes gc.collect() and returns unreachable object count."""

      @staticmethod
      def prune_ttl_buffer(buffer_dict: dict, timestamp_dict: dict, max_age_s: float = 30.0) -> list[str]:
          """[LAB-095] Prunes stale keys from in-memory stream buffers."""
  ```
* **Delegation Safety**: 🟢 **95% Safe**.
* **Delegation Guard / Ambiguity**: Subagent prompt must mandate a graceful mock fallback if `/sys/class/thermal` is missing (e.g. MacOS / CI).
* **Verification**: `test_maintenance_sweeper.py` testing thermal zone thresholding, GC metrics, and TTL buffer pruning.

---

### **Story 60.3: [FEAT-059/LAB-088/REF-03] Audio Pipeline Satellite (`audio_pipeline.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Source Lines**: [`sensory_manager.py:L102-120`](file:///home/jallred/Dev_Lab/HomeLabAI/src/equipment/sensory_manager.py#L102) & [`router.py:L1300-1420`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py)
* **Target Files**:
  * `HomeLabAI/src/equipment/audio_pipeline.py` (New Greenfield Module)
  * `HomeLabAI/src/tests/test_audio_pipeline.py` (New Test Suite)
* **Design & Interfaces**:
  ```python
  class AudioPipeline:
      @staticmethod
      def pcm_to_numpy(raw_bytes: bytes, dtype=np.int16) -> np.ndarray:
          """Converts binary Signed Int16 PCM to NumPy array."""

      @staticmethod
      def slice_sliding_window(buffer: np.ndarray, window_size: int = 24000, stride: int = 16000) -> tuple[Optional[np.ndarray], np.ndarray]:
          """Extracts fixed-window audio frame and advances buffer."""

      @staticmethod
      def compute_signal_peak(chunk: np.ndarray) -> int:
          """Calculates absolute max amplitude for VAD logging."""
  ```
* **Delegation Safety**: 🟡 **85% Safe**.
* **Delegation Guard / Ambiguity**: Must explicitly provide sample 16-bit PCM little-endian byte fixture shapes in prompt to prevent endianness bugs.
* **Verification**: `test_audio_pipeline.py` testing chunk concatenation, sliding window stride math, and peak signal detection.

---

### **Story 60.4: [OPS-01] Mandatory Lab Stack Restart & Quiescence Validation**
* **Status**: 🔲 **PLANNED**
* **Scope**:
  * Cleanly terminate previous `acme_foyer_v5` and `acme_ignition_v5` daemons.
  * Respect [FEAT-136] Quiescence 60s stability window to prevent VRAM thrashing.
  * Re-ignite `acme_lab.py --mode SERVICE_UNATTENDED` in background.
  * Verify `http://127.0.0.1:8765/version` reports `boot_commit == <HEAD>`.

---

### **Story 60.5: [TEST-01] Live-Fire Service Integration Test Suite (`test_live_sprint60_e2e.py`)**
* **Status**: 🔲 **PLANNED**
* **Scope**:
  * Connects over physical WebSockets (`ws://127.0.0.1:8765`) using dynamic `session_token` authentication.
  * Exercises refactored satellites on live daemon:
    1. Sends live `GEM-xxxx` override query $\rightarrow$ verifies `overrides.json` atomic update via live `override_parser`.
    2. Exercises live audio stream frames $\rightarrow$ verifies `audio_pipeline` sliding window slicing without memory leaks.
    3. Triggers live heartbeat and status $\rightarrow$ verifies `maintenance_sweeper` thermal probe and heap scavenger.
  * **Mandate**: No mocks for the running lab service. Tests must validate the physical live running process.

---

## 🗺️ Existing Test Earmarks & Defeaturing Map

| Existing Test Script | Subsystem Covered | Refactoring Action | Earmarked Target Story |
| :--- | :--- | :--- | :--- |
| `src/tests/test_relay_interest_buildup.py` | Overrides & Hub Triage | **PRESERVE** (Core baseline) | Story 60.1 |
| `src/debug/test_goodnight_bounce.py` | Maintenance & Restart | **SUPERSEDE** (Replace with unit sweeper) | Story 60.2 |
| `src/tests/test_memory_architecture.py` | Audio Buffer & GC | **REFACTOR** (Extract to `audio_pipeline`) | Story 60.3 |
| `src/tests/test_live_audio_memory_benchmark.py`| Real-Time PCM | **PRESERVE** (Live fire benchmark) | Story 60.3 |
| `src/test_echo.py` | Legacy PCM streaming | **DEFEATURE** (Obsolete legacy test) | Earmarked for removal |

---

## 🏷️ Feature Tracking & Link Integrity Lifecycle

When refactoring code into new satellite modules, source links in `FeatureTracker.md` must be updated to prevent broken links or dropped capabilities.

### **Open Delegation Feedback Protocol:**
During subagent execution, if a refactor encounters an existing feature hook:
* **Option A (Recover & Rewire)**: Wire the feature into the new satellite module, write a unit test, and update the GitHub line reference in `FeatureTracker.md`.
* **Option B (Table & Report)**: If a legacy feature is redundant or superseded, subagent surfaces the proposal in its Handover Reflection, allowing AGY and User to formally defeature it in `FeatureTracker.md`.

### **Tracked Features for Sprint 60:**

| Feature ID | Feature Title | Current Source Link | Refactored Source Target | Action |
| :--- | :--- | :--- | :--- | :--- |
| `[FEAT-145]` | Reasoning Waterfall Override | `cognitive_hub.py:L713` | `src/logic/override_parser.py:L20` | Rewire & Update Link |
| `[LAB-095]` | TTL Sweeper (30s) | `router.py:L1437` | `src/v5/foyer/maintenance_sweeper.py:L15` | Rewire & Update Link |
| `[LAB-096]` | Heap Scavenger (60s GC) | `router.py:L1512` | `src/v5/foyer/maintenance_sweeper.py:L35` | Rewire & Update Link |
| `[LAB-099]` | CPU Thermal Guard (78°C) | `router.py:L1490` | `src/v5/foyer/maintenance_sweeper.py:L55` | Rewire & Update Link |
| `[FEAT-059]` | Real-Time PCM Audio | `sensory_manager.py:L102`| `src/equipment/audio_pipeline.py:L20` | Rewire & Update Link |
| `[LAB-088]` | Sensory Ear Component | `sensory_manager.py:L80` | `src/equipment/sensory_manager.py:L80` | Preserve |

---

## 🧭 Execution Order

1. **Story 60.1**: Dispatch `override_parser.py` (Phase 1).
2. **Story 60.2**: Dispatch `maintenance_sweeper.py` (Phase 2).
3. **Story 60.3**: Dispatch `audio_pipeline.py` (Phase 3).
4. **Wiring & Unit Baseline**: Wire satellites into `CognitiveHub` and `router.py`, run unit suites.
5. **Story 60.4**: Lab Stack Bounce & Quiescence Validation (serve fresh commit bytecode).
6. **Story 60.5**: Live-Fire Service Integration Test (`test_live_sprint60_e2e.py`) over physical WebSockets.
7. **Feature Links & Docs**: Update `FeatureTracker.md` and rebuild Field Notes.
