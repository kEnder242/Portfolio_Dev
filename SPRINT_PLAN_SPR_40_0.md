# Sprint 40 – Real-Time Observability & Grafana Pipeline Synthesis

This sprint focuses on transitioning the MoE+ mixture-of-experts benchmarking framework from static JSON metrics to a real-time, Prometheus-scraped telemetry stack, visualizable via a multi-lane Grafana dashboard embedded back into our static files.

---

## Active Stories & Task Ledger

### Story 1: Prometheus Metrics Exporter for MoE+ Engine [Sisyphus / planning]
*   **Why**: Shift from post-processed offline JSON metrics to live-streaming application events, enabling correlation of query latency phases (intent triage, context aggregation, model warmup, and inference) directly with hardware metrics (VRAM, Power, and Thermals).
*   **Design**:
    *   Integrate `prometheus_client` into `HomeLabAI/src/debug/bench_moe_plus.py` and `Portfolio_Dev/field_notes/bench_models.py`.
    *   Expose a `/metrics` HTTP endpoint (on port `8000`) or configure pushing to the local Prometheus Pushgateway.
    *   Expose critical telemetry metrics:
        *   `moe_router_latency_seconds` (Gauge/Histogram)
        *   `moe_warmup_latency_seconds` (Gauge/Histogram)
        *   `moe_expert_latency_seconds` (Gauge/Histogram)
        *   `moe_total_latency_seconds` (Gauge/Histogram)
        *   `moe_routing_accuracy` (Gauge)
        *   `moe_stage_duration_seconds{stage="RAG|workspace|warming|compilation"}`
*   **Tasks**:
    *   [ ] Install `prometheus-client` in both virtual environments:
        *   `/home/jallred/Dev_Lab/Portfolio_Dev/.venv/bin/pip install prometheus_client`
        *   `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pip install prometheus_client`
    *   [ ] Refactor `/home/jallred/Dev_Lab/HomeLabAI/src/debug/bench_moe_plus.py` to start a prometheus server on port `8000` and stream metrics.
    *   [ ] Refactor `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/bench_models.py` to expose telemetry on port `8001` or push to a local scraping registry.
*   **Verification Gate**:
    *   Run curl commands on the endpoints:
        *   `curl -s http://localhost:8000/metrics`
        *   `curl -s http://localhost:8001/metrics`
        *   Verify that the custom `moe_` gauges are rendering correctly.

### Story 2: Grafana Latency Nuance Dashboard & Panel Build [Sisyphus-Junior / quick]
*   **Why**: Construct a high-fidelity visual ledger showing query-relative latency contributions, bimodal cold/warm start splits, and box-plot distributions across different experts.
*   **Design**:
    *   Configure Prometheus to scrape the new MoE+ endpoint at `http://localhost:8000/metrics`.
    *   In Grafana (`https://monitor.jason-lab.dev`), create panels:
        *   **Stacked Area Chart**: Y-axis represents latency duration (ms), X-axis represents calendar time. Stacked layers of Triage + RAG + Warmup + Execution show contribution.
        *   **Latency Heatmap**: Y-axis represents latency buckets, X-axis represents calendar time. Show the bimodal distribution of cold start vs warm start queries.
        *   **State Timeline (Gantt)**: Expose state values for query execution blocks to map overlaps.
        *   **Box Plot (Candlestick)**: Compare latency distribution and variance across Local (2080 Ti) vs KENDER (4090).
*   **Tasks**:
    *   [ ] Update Prometheus scrape targets configuration.
    *   [ ] Build the Latency Nuance Dashboard in Grafana.
    *   [ ] Export the Grafana dashboard JSON configuration and commit to the repo.
*   **Verification Gate**:
    *   Verify the charts display active query data under test cycles in the Grafana UI.

### Story 3: Hybrid Dashboard Iframe Integration [atlas / unspecified-high]
*   **Why**: Embed the real-time Grafana panels directly into the static `benchmarks.html` page, maintaining a clean console layout while utilizing Grafana's graphing engine.
*   **Design**:
    *   Add a **Platform Switcher Toggle** (Class 1 CSS style) in `benchmarks.html` to swap views between Local 2080 Ti (vLLM) and KENDER 4090 (Ollama) statistics.
    *   Embed Grafana panels using `<iframe>` elements referencing anonymous dashboard panels (`/d-solo/...`) on `https://monitor.jason-lab.dev`.
*   **Tasks**:
    *   [ ] Re-style `benchmarks.html` to integrate the tab switcher.
    *   [ ] Embed iframes for Stacked Area, Heatmap, and State Timeline.
*   **Verification Gate**:
    *   Load `benchmarks.html` in browser and confirm that all Grafana panels render, refresh, and display live telemetry values.
