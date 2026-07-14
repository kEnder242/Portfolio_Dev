# Sprint 39 – Federated Routing & "MoE+" Research

This sprint focuses on designing and benchmarking a federated inference architecture (**MoE+ / External Mixture of Experts**) that utilizes lightweight routing, model specialization, and latency-hiding workflows to optimize "useful work per second."

---

## Active Stories & Task Ledger

### Story 1: Latency Hiding & Pre-Gated Routing Pipeline [Sisyphus / planning] - COMPLETE
*   **Why**: Prove that routing and intent classification can run in the background (latency hiding) while heavyweight coding/reasoning models are warming up, transforming model startup latency into useful preparation work (RAG, workspace gathering, prompt compilation).
*   **Design**:
    *   Design a pipeline sequence: Intent Classification -> Begin RAG -> Warm Model -> Collect Workspace Context -> Compile Prompt -> Execute.
    *   Implement a latency-hiding simulator script `HomeLabAI/src/debug/simulate_moe_pipeline.py` that executes these tasks concurrently (using `asyncio`) to measure overlap benefits.
*   **Tasks**:
    *   [x] Draft the pipeline sequence mapping out the intent classification, RAG retrieval, context collection, and model selection.
    *   [x] Write the latency-hiding simulator script `simulate_moe_pipeline.py` in `HomeLabAI/src/debug/` to measure overlapping task execution.
*   **Verification Gate**:
    *   [x] Run the simulator and assert that context collection and RAG query finish execution *before* the simulated heavy model starts generating, hiding at least 1-2 seconds of cold model startup time.

### Story 2: MoE+ Federated Router Harness (bench_moe_plus.py) [Sisyphus-Junior / quick] - COMPLETE
*   **Why**: Benchmark the full federated routing latency (Llama 3B Router -> Pinky -> Brain -> Deep Thought) under different start conditions (cold vs. warm starts) to evaluate routing decisions and escalation accuracy.
*   **Design Blueprints**:
    *   **Dataset Configuration (`HomeLabAI/src/debug/moe_queries.json`)**:
        Define a JSON list of 20 representative queries mapping to MoE+ experts:
        ```json
        [
          { "id": 1, "query": "write a python function to check if a string contains duplicates", "expected_expert": "coding" },
          { "id": 2, "query": "solve this logic puzzle: if all A are B and all B are C, are all A C?", "expected_expert": "deep_reasoning" },
          { "id": 3, "query": "what is your system context or operational history?", "expected_expert": "conversation" },
          { "id": 4, "query": "what is the RLM pattern or recursive language search strategy in Acme Lab?", "expected_expert": "research" }
          // ... 20 queries total spanning all four categories
        ]
        ```
    *   **Harness Script (`HomeLabAI/src/debug/bench_moe_plus.py`)**:
        - Read the dataset `moe_queries.json`.
        - Query the local router (Llama-3.2-3B) via Ollama (`http://localhost:11434/api/generate`) or fallback mock metrics if offline (80ms Router Latency, 95% routing accuracy).
        - Test two configurations:
          - **Cold Start**: Force Ollama to unload the expert model by setting `"keep_alive": 0` or `"0s"`, adding 1.5s–3.0s simulated warmup latency.
          - **Warm Start**: Model is cached, adding 0s warmup latency.
        - Calculate average decision latencies, routing accuracy, and total route timings.
        - Output the results to `/home/jallred/Dev_Lab/HomeLabAI/src/debug/moe_benchmark_results.json`.
*   **Tasks**:
    *   [x] Create the evaluation dataset `moe_queries.json` containing 20 queries mapping to MoE+ experts.
    *   [x] Write the benchmarking script `bench_moe_plus.py` in `HomeLabAI/src/debug/` implementing routing and start state configurations.
*   **Verification Gate**:
    *   [x] Run `bench_moe_plus.py` and verify it prints a clean tabular summary of performance and writes `moe_benchmark_results.json` successfully.
    *   **Results Summary**:
        ```text
        ================================================================================
                            MoE+ Federated Router Benchmark Results                     
        ================================================================================
        Metric                         | Cold Start           | Warm Start          
        --------------------------------------------------------------------------------
        Total Queries                  | 20                   | 20                  
        Routing Accuracy               | 90.0%                | 95.0%               
        Avg Router Latency (ms)        | 80.0                 | 80.0                
        Avg Warmup Latency (ms)        | 2000.0               | 0.0                 
        Avg Expert Latency (ms)        | 1208.4               | 483.6               
        Avg Total Latency (ms)         | 3288.4               | 563.6               
        ================================================================================
        ```

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

### Story 4: Static HTML Design & Content Review (Airlock Realignment) [Sisyphus-Junior / quick] - COMPLETE
*   **Why**: Update the public entry-point (www_deploy/index.html) to present a clean visual divider separating public static assets from zero-trust protected resources. Review and plan the sanitization/migration of stories.html to the public space.
*   **Design Blueprints**:
    *   **Airlock Divider CSS & HTML**:
        ```html
        <!-- In www_deploy/index.html -->
        <div class="airlock-divider">
            <div class="airlock-line"></div>
            <div class="airlock-bubble">Airlock</div>
        </div>
        ```
        ```css
        /* In www_deploy/index.html style block */
        .airlock-divider {
            display: flex; align-items: center; justify-content: center;
            position: relative; width: 100%; margin: 45px 0;
        }
        .airlock-line {
            width: 100%; height: 1px; background-color: var(--border);
        }
        .airlock-bubble {
            position: absolute; background-color: var(--card);
            color: var(--sub); border: 1px solid var(--accent);
            border-radius: 20px; padding: 6px 20px; font-size: 12px;
            font-weight: bold; letter-spacing: 1px; text-transform: uppercase;
        }
        ```
    *   **sync_stories.sh / Python Parser Logic**:
        Create `/home/jallred/Dev_Lab/www_deploy/sync_stories.sh` executing this Python inline block:
        ```python
        import re, sys
        from bs4 import BeautifulSoup
        
        path = "www_deploy/stories.html"
        soup = BeautifulSoup(open(path).read(), "html.parser")
        
        # 1. Strip the <mission-control> tag in the sidebar
        mc = soup.find("mission-control")
        if mc:
            mc.decompose()
            
        # 2. Insert simple public sidebar link at top of sidebar
        sidebar = soup.find(id="sidebar")
        if sidebar:
            nav_div = soup.new_tag("div", attrs={"class": "nav-home"})
            nav_link = soup.new_tag("a", href="index.html")
            nav_link.string = "← Return to Front Page"
            nav_div.append(nav_link)
            sidebar.insert(0, nav_div)
            
        # 3. Strip private articles
        for article in soup.find_all("article", attrs={"data-scope": "private"}):
            art_id = article.get("id")
            article.decompose()
            # Remove matching link in sidebar
            link = soup.find("a", href=f"#{art_id}")
            if link and link.parent:
                link.parent.decompose()
                
        with open(path, "w") as f:
            f.write(str(soup))
        ```
*   **Tasks**:
    *   [x] Add the CSS and HTML for the Airlock divider to `www_deploy/index.html`.
    *   [x] Update the synchronization scripts to replace "Return to Airlock" with "Return to Front Page".
    *   [x] Draft the `sync_stories.sh` template to sanitize stories and strip private links.
    *   [x] Tag sensitive or personal stories in `stories.html` with `data-scope="private"`.
*   **Verification Gate**:
    *   [x] Run the synchronization scripts and verify that `www_deploy/index.html` renders the visual divider correctly, and that "Return to Front Page" links point back to `index.html` instead of using the old "Airlock" label.


