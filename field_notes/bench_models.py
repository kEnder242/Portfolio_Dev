#!/usr/bin/env python3
# [FEAT-495] Dynamic Auto-Discovery Federated Silicon Benchmark Engine
import json
import os
import sys
import time

import requests

try:
    from prometheus_client import Gauge, start_http_server

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

    class DummyGauge:
        def labels(self, **kwargs):
            return self

        def set(self, val):
            pass

    def Gauge(*args, **kwargs):
        return DummyGauge()

    def start_http_server(port):
        pass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "benchmarks_cache.json")
PROMPT = "Explain the difference between PCIe GPU memory and Apple Unified Memory in two concise sentences."

# Prometheus Metrics
moe_model_ttft_seconds = Gauge(
    "moe_model_ttft_seconds",
    "Model Time to First Token in seconds",
    ["model", "seat", "engine"],
)
moe_model_throughput_tokens_per_second = Gauge(
    "moe_model_throughput_tokens_per_second",
    "Model throughput in tokens per second",
    ["model", "seat", "engine"],
)
moe_model_itl_seconds = Gauge(
    "moe_model_itl_seconds",
    "Model inter-token latency in seconds",
    ["model", "seat", "engine"],
)

# Known Seats & Endpoints
SEATS_CONFIG = {
    "m5_air": {
        "display_name": "Apple M5 Air (oMLX Port 8000)",
        "engine": "oMLX (Metal)",
        "host": "192.168.1.46",
        "port": 8000,
        "type": "openai",
        "power_watts": 18.0,
        "vram_gb": 5.5,
        "architecture": "24GB Unified Memory (5.5GB Resident)",
        "role": "Fast Scaffolding & Surgical Patcher",
        "context_window": "65k (65,536)",
        "cost_per_1m": 0.008,
        "reasoning_ratio": 0.85,
    },
    "kender_4090": {
        "display_name": "Windows 4090RTX (Port 11434)",
        "engine": "Ollama",
        "host": "192.168.1.26",
        "port": 11434,
        "type": "ollama",
        "power_watts": 290.0,
        "vram_gb": 14.5,
        "architecture": "24GB GDDR6X PCIe (1,008 GB/s)",
        "role": "High-Throughput Autonomous Coding (Qwen 3.8 27B)",
        "context_window": "32k (32,768)",
        "cost_per_1m": 0.095,
        "reasoning_ratio": 0.25,
    },
    "z87_2080ti": {
        "display_name": "Linux 2080ti (Port 8088)",
        "engine": "vLLM",
        "host": "127.0.0.1",
        "port": 8088,
        "type": "openai",
        "power_watts": 85.0,
        "vram_gb": 2.5,
        "architecture": "11GB GDDR6 Multi-LoRA (616 GB/s)",
        "role": "Sensory Foyer & Multi-LoRA Engine",
        "context_window": "8k (8,192)",
        "cost_per_1m": 0.035,
        "reasoning_ratio": 0.10,
    },
    "cloud_swarm": {
        "display_name": "Cloud Dynamic Free Swarm",
        "engine": "OpenRouter",
        "host": "127.0.0.1",
        "port": 4097,
        "type": "cloud",
        "power_watts": None,
        "vram_gb": 0.0,
        "architecture": "Distributed Cloud Clusters",
        "role": "Swarm Fallback & Cross-Review",
        "context_window": "128k (128,000)",
        "cost_per_1m": 0.00,
        "reasoning_ratio": 0.40,
    },
}

def build_offline_metrics(cfg):
    return {
        "model": None,
        "cold_ttft_ms": None,
        "warm_ttft_ms": None,
        "throughput": 0,
        "itl_ms": 0,
        "status": "offline",
        "context_window": cfg.get("context_window", "--"),
    }



def is_socket_up(host, port, timeout=0.8):
    import socket

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((host, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def discover_and_benchmark_openai_node(seat_id, cfg):
    host, port = cfg["host"], cfg["port"]
    if not is_socket_up(host, port):
        raise ConnectionError(f"Node {host}:{port} is unreachable/offline")

    # 1. Discover resident model
    models_url = f"http://{host}:{port}/v1/models"
    resp = requests.get(models_url, timeout=3)
    resp.raise_for_status()
    models_data = resp.json().get("data", [])
    if not models_data:
        raise ValueError("No models registered in /v1/models")
    model_name = models_data[0].get("id")

    # 2. Benchmark streaming completion
    chat_url = f"http://{host}:{port}/v1/chat/completions"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": 60,
        "temperature": 0.1,
        "stream": True,
    }

    t0 = time.perf_counter()
    ttft = None
    tokens = 0
    with requests.post(chat_url, json=payload, stream=True, timeout=(3, 30)) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8").strip()
            if "error" in line_str.lower() and not line_str.startswith("data: "):
                try:
                    err_data = json.loads(line_str)
                    if "error" in err_data:
                        raise RuntimeError(
                            f"Engine Error: {err_data.get('error', {}).get('message', line_str)}"
                        )
                except Exception as ex:
                    if isinstance(ex, RuntimeError):
                        raise ex
            if line_str == "data: [DONE]":
                break
            if line_str.startswith("data: "):
                try:
                    chunk = json.loads(line_str[6:])
                    if "error" in chunk:
                        raise RuntimeError(f"Stream Error: {chunk.get('error')}")
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    text = delta.get("content") or delta.get("reasoning_content") or ""
                    if text:
                        if ttft is None:
                            ttft = time.perf_counter() - t0
                        tokens += 1
                except Exception as ex:
                    if isinstance(ex, RuntimeError):
                        raise ex

    total_time = time.perf_counter() - t0
    gen_time = total_time - (ttft or 0)
    throughput = tokens / gen_time if gen_time > 0 else 0
    itl_ms = (gen_time / tokens * 1000.0) if tokens > 1 else 0

    # Live context window discovery via /api/show
    context_window = cfg.get("context_window", "--")
    try:
        show_url = f"http://{host}:{port}/api/show"
        show_resp = requests.get(show_url, params={"name": model_name}, timeout=3)
        show_resp.raise_for_status()
        show_data = show_resp.json()
        ctx = None
        if isinstance(show_data.get("model_info"), dict):
            params = show_data["model_info"].get("params")
            if isinstance(params, str):
                try:
                    params = json.loads(params)
                except Exception:
                    params = None
            if isinstance(params, dict):
                ctx = params.get("num_ctx") or params.get("context_length")
        if ctx is None:
            details = show_data.get("details") or {}
            ctx = details.get("context_length")
        if ctx is None:
            ctx = show_data.get("context_length")
        if ctx and ctx > 0:
            context_window = f"{int(ctx)//1000}k ({int(ctx):,})"
    except Exception:
        pass

    return {
        "model": model_name,
        "cold_ttft_ms": (ttft or 1.0) * 1000.0,
        "warm_ttft_ms": (ttft or 1.0) * 1000.0,
        "throughput": throughput,
        "itl_ms": itl_ms,
        "status": "online",
        "context_window": context_window,
    }


def discover_and_benchmark_ollama_node(seat_id, cfg):
    host, port = cfg["host"], cfg["port"]
    if not is_socket_up(host, port):
        raise ConnectionError(f"Node {host}:{port} is unreachable/offline")

    tags_url = f"http://{host}:{port}/api/tags"
    resp = requests.get(tags_url, timeout=3)
    resp.raise_for_status()
    models = resp.json().get("models", [])
    if not models:
        raise ValueError("No models found in Ollama tags")

    # Pure live discovery: prioritize the active 27B autonomous coding model
    tag_names = [m.get("name", "") for m in models]
    priority = ["qwen3.8:nothink", "atlas:27b", "Qwen3.8-27B", "qwen3.8-27b", "qwen3.8"]
    model_name = None
    for cand in priority:
        if cand in tag_names:
            model_name = cand
            break
    if model_name is None:
        matches = [t for t in tag_names if "qwen3.8" in t.lower() or "27b" in t.lower()]
        model_name = matches[0] if matches else models[0].get("name")

    gen_url = f"http://{host}:{port}/api/generate"
    payload = {
        "model": model_name,
        "prompt": PROMPT,
        "stream": True,
        "think": False,
        "options": {"temperature": 0.1, "num_predict": 60},
    }

    t0 = time.perf_counter()
    ttft = None
    tokens = 0
    with requests.post(gen_url, json=payload, stream=True, timeout=(3, 30)) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            chunk = json.loads(line.decode("utf-8"))
            if chunk.get("response"):
                if ttft is None:
                    ttft = time.perf_counter() - t0
                tokens += 1
            if chunk.get("done"):
                break

    total_time = time.perf_counter() - t0
    gen_time = total_time - (ttft or 0)
    throughput = tokens / gen_time if gen_time > 0 else 0
    itl_ms = (gen_time / tokens * 1000.0) if tokens > 1 else 0

    # Live context window discovery via /api/show
    context_window = cfg.get("context_window", "--")
    try:
        show_url = f"http://{host}:{port}/api/show"
        show_resp = requests.post(show_url, json={"name": model_name}, timeout=3)
        show_resp.raise_for_status()
        show_data = show_resp.json()
        ctx = None
        if isinstance(show_data.get("model_info"), dict):
            m_info = show_data["model_info"]
            for k, v in m_info.items():
                if "context_length" in k or k == "num_ctx":
                    ctx = v
                    break
            if ctx is None:
                params = m_info.get("params")
                if isinstance(params, str):
                    try:
                        params = json.loads(params)
                    except Exception:
                        params = None
                if isinstance(params, dict):
                    ctx = params.get("num_ctx") or params.get("context_length")
        if ctx is None:
            details = show_data.get("details") or {}
            ctx = details.get("context_length")
        if ctx is None:
            ctx = show_data.get("context_length")
        if ctx and int(ctx) > 0:
            ctx_int = int(ctx)
            context_window = f"{ctx_int // 1000}k ({ctx_int:,})"
    except Exception:
        pass

    return {
        "model": model_name,
        "cold_ttft_ms": (ttft or 0.3) * 1000.0,
        "warm_ttft_ms": (ttft or 0.3) * 1000.0,
        "throughput": throughput,
        "itl_ms": itl_ms,
        "status": "online",
        "context_window": context_window,
    }


def run_sweep():
    print("=== [FEAT-495] Running Dynamic Federated Benchmark Sweep ===")
    sweep_results = []

    for seat_id, cfg in SEATS_CONFIG.items():
        print(f"[*] Probing {cfg['display_name']}...")
        metrics = None
        try:
            if cfg["type"] == "openai":
                metrics = discover_and_benchmark_openai_node(seat_id, cfg)
            elif cfg["type"] == "ollama":
                metrics = discover_and_benchmark_ollama_node(seat_id, cfg)
            else:
                metrics = build_offline_metrics(cfg)

            if metrics and metrics.get("status") == "online":
                print(
                    f"   ✔ [ONLINE] Model: {metrics['model']} | TTFT: {metrics['warm_ttft_ms']:.1f}ms | Throughput: {metrics['throughput']:.2f} tok/s"
                )
            else:
                print(f"   ✖ [OFFLINE] Node {cfg['display_name']} is offline/unconfigured")
        except Exception as e:
            print(f"   ✖ [OFFLINE] Reason: {e}")
            metrics = build_offline_metrics(cfg)

        power_w = cfg["power_watts"]
        tp = metrics["throughput"]
        tokens_per_joule = (
            round(tp / power_w, 3)
            if (power_w is not None and power_w > 0 and tp > 0)
            else None
        )

        if tokens_per_joule and tokens_per_joule > 0:
            kwh_per_1m = (1000000.0 / tokens_per_joule) / 3600000.0
            electricity_cost_per_1m = round(kwh_per_1m * 0.15, 4)
            cloud_multiplier = (
                round(3.00 / electricity_cost_per_1m, 1)
                if electricity_cost_per_1m > 0
                else 1.0
            )
            cloud_savings_pct = round(
                100.0 - (electricity_cost_per_1m / 3.00 * 100.0), 1
            )
        else:
            electricity_cost_per_1m = None
            cloud_multiplier = None
            cloud_savings_pct = 100.0

        item = {
            "model": metrics["model"],
            "engine": cfg["engine"],
            "seat_id": seat_id,
            "display_name": cfg["display_name"],
            "architecture": cfg["architecture"],
            "role": cfg["role"],
            "context_window": metrics.get("context_window") or cfg.get("context_window", "--"),
            "cold_ttft_ms": metrics["cold_ttft_ms"],
            "warm_ttft_ms": metrics["warm_ttft_ms"],
            "ttft_ms": metrics["warm_ttft_ms"],
            "raw_throughput": metrics["throughput"],
            "effective_throughput": metrics["throughput"],
            "throughput": metrics["throughput"],
            "itl_ms": metrics["itl_ms"],
            "vram_gb": cfg["vram_gb"],
            "power_watts": power_w,
            "tokens_per_joule": tokens_per_joule,
            "electricity_cost_per_1m": electricity_cost_per_1m,
            "cloud_multiplier": cloud_multiplier,
            "cloud_savings_pct": cloud_savings_pct,
            "reasoning_token_ratio": cfg["reasoning_ratio"],
            "status": metrics["status"],
        }
        sweep_results.append(item)

        # Expose to Prometheus
        if metrics["warm_ttft_ms"] is not None:
            moe_model_ttft_seconds.labels(
                model=metrics["model"] or "offline", seat=seat_id, engine=cfg["engine"]
            ).set(metrics["warm_ttft_ms"] / 1000.0)
        if metrics["throughput"] is not None:
            moe_model_throughput_tokens_per_second.labels(
                model=metrics["model"] or "offline", seat=seat_id, engine=cfg["engine"]
            ).set(metrics["throughput"])
        if metrics["itl_ms"] is not None:
            moe_model_itl_seconds.labels(
                model=metrics["model"] or "offline", seat=seat_id, engine=cfg["engine"]
            ).set(metrics["itl_ms"] / 1000.0)

    # Save to benchmarks_cache.json atomically
    cache_payload = {
        "timestamp": time.time(),
        "date_str": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": sweep_results,
    }
    tmp_path = CACHE_FILE + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(cache_payload, f, indent=2)
    os.replace(tmp_path, CACHE_FILE)
    print(f"✅ Atomically updated {CACHE_FILE} with live sweep results!")


def main():
    if "--no-serve" not in sys.argv:
        try:
            start_http_server(8011)
            print("💡 Prometheus metrics active on http://localhost:8011")
        except Exception as e:
            print(f"⚠️ Prometheus port 8011 busy or failed: {e}")
    run_sweep()


if __name__ == "__main__":
    main()
