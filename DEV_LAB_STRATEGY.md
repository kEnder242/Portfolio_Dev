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
