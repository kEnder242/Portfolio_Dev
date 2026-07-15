#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
import subprocess
import threading
from prometheus_client import Gauge, start_http_server

# Prometheus metrics
moe_stage_duration_seconds = Gauge(
    "moe_stage_duration_seconds",
    "Duration of MoE+ pipeline stages in seconds",
    ["stage"]
)
moe_model_ttft_seconds = Gauge(
    "moe_model_ttft_seconds",
    "Model Time to First Token in seconds",
    ["model", "engine"]
)
moe_model_throughput_tokens_per_second = Gauge(
    "moe_model_throughput_tokens_per_second",
    "Model throughput in tokens per second",
    ["model", "engine"]
)
moe_model_itl_seconds = Gauge(
    "moe_model_itl_seconds",
    "Model inter-token latency in seconds",
    ["model", "engine"]
)
moe_model_vram_bytes = Gauge(
    "moe_model_vram_bytes",
    "Model peak VRAM footprint in bytes",
    ["model", "engine"]
)

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "benchmarks_cache.json")
PROMPT = "Explain silicon routing in two sentences."

# Endpoints
VLLM_PORT = 8088
OLLAMA_PORT = 11434

# Pre-characterized metrics fallbacks
FALLBACKS = {
    "Llama-3.2-3B-AWQ": {
        "model": "Llama-3.2-3B-AWQ",
        "engine": "vLLM",
        "display_name": "Llama 3.2 3B AWQ (vLLM)",
        "ttft_ms": 250.0,
        "throughput": 45.0,
        "itl_ms": 22.22, # 1000 / 45
        "vram_gb": 2.5,
        "status": "offline_fallback"
    },
    "Gemma-2-2B": {
        "model": "Gemma-2-2B",
        "engine": "Ollama",
        "display_name": "Gemma 2 2B (Ollama)",
        "ttft_ms": 350.0,
        "throughput": 35.0,
        "itl_ms": 28.57, # 1000 / 35
        "vram_gb": 2.2,
        "status": "offline_fallback"
    },
    "Qwen-2.5-Coder": {
        "model": "Qwen-2.5-Coder",
        "engine": "Ollama",
        "display_name": "Qwen-27B (Remote)",
        "ttft_ms": 900.0,
        "throughput": 25.0,
        "itl_ms": 40.00, # 1000 / 25
        "vram_gb": 0.0,
        "status": "offline_fallback"
    }
}

def get_gpu_memory_used():
    """Retrieves current GPU memory usage in GB using NVML or nvidia-smi."""
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        pynvml.nvmlShutdown()
        return info.used / 1024.0 / 1024.0 / 1024.0
    except Exception:
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return float(res.stdout.strip()) / 1024.0
        except Exception:
            return 0.0

class VRAMTracker:
    """Helper to poll and track peak VRAM footprint in a background thread."""
    def __init__(self, interval=0.05):
        self.interval = interval
        self.peak_vram = 0.0
        self.running = False
        self.thread = None

    def _track(self):
        while self.running:
            vram = get_gpu_memory_used()
            if vram > self.peak_vram:
                self.peak_vram = vram
            time.sleep(self.interval)

    def start(self):
        self.peak_vram = get_gpu_memory_used()
        self.running = True
        self.thread = threading.Thread(target=self._track, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        return self.peak_vram


def safe_read_json(file_path: str, default=None):
    """Safely read and parse a JSON file. Returns `default` if file is missing, empty, or invalid."""
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if not content:
                print(f"⚠️  Warning: File {file_path} is empty. Using default value.")
                return default
            return json.loads(content)
    except FileNotFoundError:
        print(f"⚠️  Warning: File {file_path} not found. Using default value.")
        return default
    except json.JSONDecodeError as e:
        print(f"❌ Error: File {file_path} contains invalid JSON: {e}. Using default value.")
        return default
    except Exception as e:
        print(f"❌ Error: Failed to read {file_path}: {e}. Using default value.")
        return default

def test_vllm_model(model_name):
    """Benchmarks vLLM model by streaming a completion."""
    url = f"http://localhost:{VLLM_PORT}/v1/completions"
    payload = {
        "model": model_name,
        "prompt": PROMPT,
        "max_tokens": 50,
        "temperature": 0.0,
        "stream": True
    }
    
    tracker = VRAMTracker()
    tracker.start()
    
    start_time = time.time()
    ttft = None
    token_times = []
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=5)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                chunk_time = time.time()
                line_str = line.decode('utf-8').strip()
                if line_str.startswith("data:"):
                    data_str = line_str[5:].strip()
                    if data_str == "[DONE]":
                        break
                    chunk = json.loads(data_str)
                    choices = chunk.get("choices", [])
                    if choices:
                        text = choices[0].get("text", "")
                        if text:
                            token_times.append(chunk_time)
                            if ttft is None:
                                ttft = chunk_time - start_time
    except Exception as e:
        tracker.stop()
        raise e
        
    peak_vram = tracker.stop()
    
    if not token_times:
        raise Exception("No tokens generated from vLLM")
        
    total_time = token_times[-1] - start_time
    total_tokens = len(token_times)
    
    if len(token_times) > 1:
        intervals = [token_times[i] - token_times[i-1] for i in range(1, len(token_times))]
        itl = sum(intervals) / len(intervals)
    else:
        itl = 0.0
        
    throughput = total_tokens / total_time if total_time > 0 else 0.0
    
    return {
        "model": model_name,
        "engine": "vLLM",
        "display_name": f"{model_name} (vLLM)",
        "ttft_ms": ttft * 1000.0 if ttft else 0.0,
        "throughput": throughput,
        "itl_ms": itl * 1000.0,
        "vram_gb": peak_vram,
        "status": "online"
    }

def test_ollama_model(model_name):
    """Benchmarks Ollama model by streaming a generation request."""
    # First probe if the model is locally loaded
    probe_url = f"http://localhost:{OLLAMA_PORT}/api/tags"
    resp = requests.get(probe_url, timeout=3)
    resp.raise_for_status()
    available_models = [m.get("name") for m in resp.json().get("models", [])]
    
    # Try exact match or base name match
    matched_model = None
    for name in available_models:
        if model_name.lower() in name.lower() or name.lower() in model_name.lower():
            matched_model = name
            break
            
    if not matched_model:
        raise Exception(f"Model {model_name} not available in Ollama tags")

    url = f"http://localhost:{OLLAMA_PORT}/api/generate"
    payload = {
        "model": matched_model,
        "prompt": PROMPT,
        "stream": True,
        "options": {"temperature": 0.0}
    }
    
    tracker = VRAMTracker()
    tracker.start()
    
    start_time = time.time()
    ttft = None
    token_times = []
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=5)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                chunk_time = time.time()
                chunk = json.loads(line.decode('utf-8'))
                if chunk.get("response"):
                    token_times.append(chunk_time)
                    if ttft is None:
                        ttft = chunk_time - start_time
                if chunk.get("done", False):
                    break
    except Exception as e:
        tracker.stop()
        raise e
        
    peak_vram = tracker.stop()
    
    if not token_times:
        raise Exception("No tokens generated from Ollama")
        
    total_time = token_times[-1] - start_time
    total_tokens = len(token_times)
    
    if len(token_times) > 1:
        intervals = [token_times[i] - token_times[i-1] for i in range(1, len(token_times))]
        itl = sum(intervals) / len(intervals)
    else:
        itl = 0.0
        
    throughput = total_tokens / total_time if total_time > 0 else 0.0
    
    return {
        "model": model_name,
        "engine": "Ollama",
        "display_name": f"{model_name} (Ollama)",
        "ttft_ms": ttft * 1000.0 if ttft else 0.0,
        "throughput": throughput,
        "itl_ms": itl * 1000.0,
        "vram_gb": peak_vram,
        "status": "online"
    }

def main():
    # Start Prometheus metrics server if not disabled
    if "--no-serve" not in sys.argv:
        try:
            start_http_server(8011)
            print("💡 Prometheus metrics endpoint active on http://localhost:8011")
        except Exception as e:
            print(f"⚠️  Failed to start Prometheus server on port 8011: {e}")

    print("--- Silicon Performance Benchmarking Start ---")
    results = []
    
    # 1. Benchmark Llama-3.2-3B-AWQ (vLLM)
    print("Benchmarking Llama-3.2-3B-AWQ (vLLM port 8088)...")
    try:
        metrics = test_vllm_model("Llama-3.2-3B-AWQ")
        results.append(metrics)
        print(f"✅ Online success: {metrics}")
    except Exception as e:
        print(f"⚠️  vLLM offline/failed ({e}). Loading pre-characterized fallback...")
        results.append(FALLBACKS["Llama-3.2-3B-AWQ"])
        
    # 2. Benchmark Gemma-2-2B (Ollama)
    print("Benchmarking Gemma-2-2B (Ollama port 11434)...")
    try:
        metrics = test_ollama_model("Gemma-2-2B")
        results.append(metrics)
        print(f"✅ Online success: {metrics}")
    except Exception as e:
        print(f"⚠️  Ollama Gemma-2-2B offline/failed ({e}). Loading pre-characterized fallback...")
        results.append(FALLBACKS["Gemma-2-2B"])

    # 3. Benchmark Qwen-2.5-Coder (Ollama)
    print("Benchmarking Qwen-2.5-Coder (Ollama port 11434)...")
    try:
        metrics = test_ollama_model("Qwen-2.5-Coder")
        results.append(metrics)
        print(f"✅ Online success: {metrics}")
    except Exception as e:
        print(f"⚠️  Ollama Qwen-2.5-Coder offline/failed ({e}). Loading pre-characterized fallback...")
        results.append(FALLBACKS["Qwen-2.5-Coder"])

    moe_pipeline = safe_read_json("/home/jallred/Dev_Lab/HomeLabAI/src/debug/moe_pipeline_metrics.json")
    moe_benchmark = safe_read_json("/home/jallred/Dev_Lab/HomeLabAI/src/debug/moe_benchmark_results.json")

    # Expose pipeline stage durations as Prometheus metrics
    if moe_pipeline:
        stages = [
            "intent_classification",
            "rag_retrieval",
            "workspace_context",
            "model_warming",
            "prompt_compilation",
            "total_pipeline"
        ]
        for stage in stages:
            start_val = moe_pipeline.get(f"{stage}_start")
            end_val = moe_pipeline.get(f"{stage}_end")
            if start_val is not None and end_val is not None:
                duration = end_val - start_val
                moe_stage_duration_seconds.labels(stage=stage).set(duration)

    # Expose model metrics to Prometheus
    for res in results:
        moe_model_ttft_seconds.labels(model=res["model"], engine=res["engine"]).set(res["ttft_ms"] / 1000.0)
        moe_model_throughput_tokens_per_second.labels(model=res["model"], engine=res["engine"]).set(res["throughput"])
        moe_model_itl_seconds.labels(model=res["model"], engine=res["engine"]).set(res["itl_ms"] / 1000.0)
        moe_model_vram_bytes.labels(model=res["model"], engine=res["engine"]).set(res["vram_gb"] * 1024.0 * 1024.0 * 1024.0)


    output_data = {
        "timestamp": time.time(),
        "date_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "results": results,
        "moe_pipeline": moe_pipeline,
        "moe_benchmark": moe_benchmark
    }

    # Atomic write pattern: write to tmp file then rename
    tmp_file = CACHE_FILE + ".tmp"
    try:
        with open(tmp_file, "w") as f:
            json.dump(output_data, f, indent=2)
        os.replace(tmp_file, CACHE_FILE)
        print(f"✅ Successfully wrote atomic cache to: {CACHE_FILE}")
    except Exception as e:
        print(f"❌ Failed writing cache: {e}")
        if os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except OSError:
                pass
        sys.exit(1)

    # Keep-alive loop so Prometheus can scrape metrics if serving
    if "--no-serve" not in sys.argv:
        print("Metrics endpoint active. Sleeping to allow scraping (Ctrl+C to exit)...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping metrics server.")

if __name__ == "__main__":
    main()
