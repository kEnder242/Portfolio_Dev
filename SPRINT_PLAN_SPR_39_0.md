# Sprint 39 – Federated Routing & "MoE+" Research

This sprint focuses on designing and benchmarking a federated inference architecture (**MoE+ / External Mixture of Experts**) that utilizes lightweight routing, model specialization, and latency-hiding workflows to optimize "useful work per second."

---

## Active Stories & Task Ledger

### Story 1: Latency Hiding & Pre-Gated Routing Pipeline [Sisyphus / planning]
*   **Why**: Prove that routing and intent classification can run in the background (latency hiding) while heavyweight coding/reasoning models are warming up, transforming model startup latency into useful preparation work (RAG, workspace gathering, prompt compilation).
*   **Design**:
    *   Design a pipeline sequence: Intent Classification -> Begin RAG -> Warm Model -> Collect Workspace Context -> Compile Prompt -> Execute.
    *   Implement a latency-hiding simulator script `HomeLabAI/src/debug/simulate_moe_pipeline.py` that executes these tasks concurrently (using `asyncio`) to measure overlap benefits.
*   **Tasks**:
    *   [ ] Draft the pipeline sequence mapping out the intent classification, RAG retrieval, context collection, and model selection.
    *   [ ] Write the latency-hiding simulator script `simulate_moe_pipeline.py` in `HomeLabAI/src/debug/` to measure overlapping task execution.
*   **Verification Gate**:
    *   [ ] Run the simulator and assert that context collection and RAG query finish execution *before* the simulated heavy model starts generating, hiding at least 1-2 seconds of cold model startup time.

### Story 2: MoE+ Federated Router Harness (bench_moe_plus.py) [Sisyphus-Junior / quick]
*   **Why**: Benchmark the full federated routing latency (Llama 3B Router -> Pinky -> Brain -> Deep Thought) under different start conditions (cold vs. warm starts) to evaluate routing decisions and escalation accuracy.
*   **Design**:
    *   Develop a representative evaluation dataset of 20 queries spanning conversation, coding, and deep reasoning.
    *   Write `HomeLabAI/src/debug/bench_moe_plus.py` to timing-audit the Llama-3.2-3B router's classification latency and accuracy.
    *   Simulate cold starts programmatically in the script by requesting `"keep_alive": 0` (or `"0s"`) during queries to force Ollama to unload models.
*   **Tasks**:
    *   [ ] Create a small evaluation dataset of 20 representative queries mapping to MoE+ experts.
    *   [ ] Write the benchmarking script `bench_moe_plus.py` in `HomeLabAI/src/debug/` incorporating cold/warm start testing.
*   **Verification Gate**:
    *   [ ] Run `bench_moe_plus.py` and print a table showing the routing accuracy, TTFT, and full-route decision latency.

### Story 3: MoE+ Benchmarking Framework (KPIs) [atlas / unspecified-high]
*   **Why**: Create a diagnostic framework that evaluates the *architecture* (useful work per second) rather than just raw tokens/sec, measuring TTFT, Time to Useful Answer, Cold model load time, and RAG retrieval latency.
*   **Design**:
    *   Implement metric trackers in the benchmark script to record RAG retrieval time, routing decision time, model warm-up time, and prompt ingestion time.
    *   Format these metrics into a structured JSON report.
*   **Tasks**:
    *   [ ] Extend the performance benchmarking page `benchmarks.html` to display pipeline-stage latency metrics (RAG, routing, warming, execution).
    *   [ ] Update the site builder `build_site.py` to parse these multi-stage JSON metrics.
*   **Verification Gate**:
    *   [ ] Execute a simulated run and verify that the metrics compile and display cleanly on the local `benchmarks.html` page.
