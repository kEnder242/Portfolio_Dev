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

### Story 4: Static HTML Design & Content Review (Airlock Realignment) [Sisyphus-Junior / quick]
*   **Why**: Update the public entry-point (www_deploy/index.html) to present a clean visual divider separating public static assets from zero-trust protected resources. Review and plan the sanitization/migration of stories.html to the public space.
*   **Design**:
    *   Add an `.airlock-divider` visual line with a blue bubble labeled "Airlock" in `www_deploy/index.html` below the public links and above the private ones.
    *   Refactor `sync_protocols.sh` and `sync_research.sh` to update "Return to Airlock" to "Return to Front Page".
    *   Design the `sync_stories.sh` deployment script to filter out `<article>` elements tagged with `data-scope="private"` and refactor the sidebar (stripping out `<mission-control>`).
*   **Tasks**:
    *   [ ] Add the CSS and HTML for the Airlock divider to `www_deploy/index.html`.
    *   [ ] Update the synchronization scripts to replace "Return to Airlock" with "Return to Front Page".
    *   [ ] Draft the `sync_stories.sh` template to sanitize stories and strip private links.
    *   [ ] Tag sensitive or personal stories in `stories.html` with `data-scope="private"`.
*   **Verification Gate**:
    *   [ ] Run the synchronization scripts and verify that `www_deploy/index.html` renders the visual divider correctly, and that "Return to Front Page" links point back to `index.html` instead of using the old "Airlock" label.

