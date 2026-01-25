# Phase 3 Learning Primer: The Metrics Lab
**Status:** Live Document
**Goal:** Master Observability (Prometheus/Grafana/Docker) using "Field Notes" logic.

## 🧠 Core Concepts (The "Why")
- **Exporters:** Agents that translate system data (CPU, Logs) into metrics.
- **Scraping:** Prometheus "pulls" data from exporters every 15s (Pull Model).
- **Time-Series:** Data is stored as `(timestamp, value)` pairs, not relational rows.
- **Visualization:** Grafana queries Prometheus to draw pretty lines.

## 🛠️ The Stack (Dockerized)
We chose Docker to keep the host clean ("Class 1" philosophy).
- `docker-compose.yml`: The blueprint defining all services.
- **Network:** Docker creates an internal bridge; containers talk via names (e.g., `prometheus:9090`).

## 🎮 The "RAPL-Sim" Logic
We map REAL telemetry to SIMULATED validation scenarios.
- **Real:** CPU Usage, Temperature (via `lm-sensors` if available), Frequency.
- **Simulated:** "Package Power Limits" (PL1/PL2) based on load.

## 📜 Cheat Sheet (Commands)
- `docker-compose up -d`: Start everything in background.
- `docker-compose logs -f`: Tail logs for all containers.
- `docker-compose ps`: See what's running.
- `docker-compose down`: Stop and clean up.

## 🛡️ Security Note
- **Grafana:** Default user `admin/admin` (Must change on first login).
- **Sharing:** We will configure a "Viewer" role for secure sharing.

---
*Updated automatically as we build.*
