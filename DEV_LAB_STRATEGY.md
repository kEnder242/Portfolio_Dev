# Dev_Lab Federated Strategy
**The Architectural Contract for the Acme Lab Ecosystem**

This document defines the high-level rules for how independent projects within `Dev_Lab` coexist and interact.

## 1. The Federated Model
We follow a **"Shared Nothing, Talk via HTTP"** architecture.

*   **HomeLabAI:** The "Brain." Heavy compute, ML models, specialized hardware access.
*   **Portfolio_Dev:** The "Face." Lightweight, static, high-availability dashboard.
*   **Acme_Lab:** The "Product." The shipping code that combines these.

## 2. Environment Strategy (The "Clean Room" Rule)
To prevent "Dependency Hell," we enforce strict isolation.

### 🚫 The Anti-Pattern (What we avoid)
*   **System Python for Libraries:** Never install `pip` packages (especially `torch`, `numpy`) into `/usr/bin/python3`. This risks breaking OS utilities (`apt`, `dnf`) and creates unfixable conflict states.
*   **The "Mega-Venv":** Do not share a single `.venv` across HomeLabAI and Portfolio. Updating the Brain's PyTorch should never crash the Portfolio's website builder.
*   **System Fallback:** We do NOT use `--system-site-packages`. Each project must explicitly declare exactly what it needs.

### ✅ The Protocol
| Project | Env Location | Requirements | Profile |
| :--- | :--- | :--- | :--- |
| **HomeLabAI** | `./HomeLabAI/.venv` | `requirements.txt` (Heavy) | PyTorch, CUDA, Transformers, Audio |
| **Portfolio_Dev** | `./Portfolio_Dev/.venv` | `requirements.txt` (Light) | Requests, Prometheus_Client |

## 3. The Bridge (Inter-Process Communication)
Since the environments are separate, they cannot import each other's code directly.
*   **Logic:** `import acme.brain` ❌ **FORBIDDEN**
*   **Logic:** `requests.post('localhost:8765/ask')` ✅ **APPROVED**

This decoupling ensures that even if the AI Brain crashes or is rebuilding, the Portfolio dashboard remains live and functional.

## 4. Component Hierarchy (The "Resilience" Law)
We prioritize system availability by distinguishing between "Invariant" and "Transient" components.

*   **The Invariant Sensory Core (EarNode):** Powered by NeMo. This is the "Heart." It MUST remain resident and functional regardless of the reasoning engine state. Sensing must never fail.
*   **The Transient Reasoning Engine (Brain/Pinky):** Powered by vLLM/Ollama. This is the "Mind." It can be downshifted, swapped, or suspended based on hardware pressure.

## 5. Hardware Alignment (The "Silicon" Mandate)
To survive on an 11GB VRAM budget (RTX 2080 Ti), all AI projects MUST adhere to these resource constraints:
*   **Model Tiering**: Standardize on **Gemma 2 2B (MEDIUM)** for local reasoning. 
*   **VRAM Parity**: Avoid models > 7B on the orchestration node to prevent clashing with the EarNode (~1GB) and system overhead.
*   **Native Pre-emption**: AI processes must be ready to yield to non-AI tasks (Games/Transcodes) via the Resilience Ladder.
