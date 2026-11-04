#!/usr/bin/env python3
"""[Story 110.6 / BKM-088] Empirical Throughput & Latency Benchmark Gauntlet.

Benchmarks pure CUDA vs heterogeneous hybrid pooled VRAM execution.
Measures TTFT (Time-to-first-token), tok/s throughput, and VRAM footprints.
"""

import datetime
import json
import os
import subprocess
import sys
import time
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "hybrid_benchmark_results.json")


def get_cuda_vram_mb() -> float:
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            check=True,
        )
        return float(res.stdout.strip().split("\n")[0])
    except Exception:
        return 0.0


def benchmark_endpoint(
    endpoint_url: str = "http://127.0.0.1:8088/v1/chat/completions",
    prompt: str = "Explain the architecture of Resizable BAR and PCIe MMIO allocation in Linux.",
    max_tokens: int = 128,
) -> dict:
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "stream": True,
    }

    req = urllib.request.Request(
        endpoint_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    ttft_ms = 0.0
    start_time = time.perf_counter()
    first_token_time = None
    token_count = 0

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line_str = line.decode("utf-8").strip()
                if not line_str.startswith("data: "):
                    continue
                data_part = line_str[6:]
                if data_part == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_part)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        token_count += 1
                        if first_token_time is None:
                            first_token_time = time.perf_counter()
                            ttft_ms = (first_token_time - start_time) * 1000.0
                except Exception:
                    pass
    except Exception as e:
        return {"error": str(e), "status": "FAILED"}

    end_time = time.perf_counter()
    total_sec = end_time - start_time
    tok_per_sec = token_count / (end_time - first_token_time) if first_token_time and end_time > first_token_time else 0.0

    return {
        "status": "PASS",
        "ttft_ms": round(ttft_ms, 2),
        "total_ms": round(total_sec * 1000.0, 2),
        "tokens_emitted": token_count,
        "tokens_per_second": round(tok_per_sec, 2),
        "cuda_vram_mb": get_cuda_vram_mb(),
    }


def main():
    print("--- [Story 110.6] Empirical LLM Benchmark Gauntlet ---")
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Test short prompt
    short_res = benchmark_endpoint(
        prompt="Reply with exactly three words.",
        max_tokens=16,
    )
    print(f"Short prompt: {short_res}")

    # Test medium prompt
    med_res = benchmark_endpoint(
        prompt="Explain the technical difference between Pipeline Parallelism and Tensor Parallelism in distributed AI inference.",
        max_tokens=256,
    )
    print(f"Standard prompt: {med_res}")

    benchmark_record = {
        "timestamp": timestamp,
        "cuda_card": "NVIDIA GeForce RTX 2080 Ti (11GB)",
        "arc_card": "Intel Arc B580 (16GB ReBAR)",
        "short_bench": short_res,
        "standard_bench": med_res,
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(benchmark_record, f, indent=2)

    print(f"✅ Benchmark results recorded to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
