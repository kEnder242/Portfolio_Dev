# Tech Stack: HomeLabAI Ecosystem

## Core Infrastructure
- **Operating Systems**: Ubuntu Linux (Primary Host), Windows 11 (Heavy Inference).
- **GPU Acceleration**: NVIDIA CUDA (RTX 2080 Ti & RTX 4090).
- **Inference Engines**: 
  - **vLLM**: Primary inference for multi-adapter hot-swapping.
  - **Ollama**: Fallback and base model hosting.
- **Service Management**: Systemd (lab-attendant.service).

## Development & AI Tools
- **Language**: Python 3.12+
- **Agent Framework**: DeepAgent (Local/Remote hybrid).
- **Linter/Formatter**: Ruff (Mandatory check-gate).
- **Testing**: Pytest (Integrated with patching tools).
- **ML Libraries**: Unsloth (for Expert Forge), Liger-Kernel (Performance).

## Connectivity & Security
- **Networking**: Tailscale (MagicDNS), Cloudflare Tunnels (Zero Trust Access).
- **Security**: Split-policy model (Admin Vault vs. Guest Lobby).
- **Observability**: Prometheus, Grafana, DCGM, NodeExporter.
