# 📜 SPRINT PLAN: Sprint 57.0 — VRAM Topology Rebalance & EarNode Evolution

> **Status:** DRAFT / EXPLORATION BACKLOG
> **Focus:** Architectural evaluation for saving 2080 Ti VRAM via ChromaDB, MiniLM, and EarNode restructuring.

---

## 🏛️ **1. Three Topologies for ChromaDB, MiniLM & VRAM Coexistence**

### **Option A: The PyTorch Workhorse (2080 Ti Sensory Ecosystem)**
* **The Concept**: Stop fighting PyTorch's VRAM caching allocator. Lean entirely into it and dedicate the local RTX 2080 Ti (11GB) as the specialized **Sensory & Embedding Engine** (`NeMo` ASR + `ChromaDB` + `MiniLM` PyTorch embeddings).
* **The Shuffling**:
  * Offload heavy LLM text generation (**Pinky / Brain / Deep Thought**) off the 2080 Ti entirely.
  * **Deep Thought** moves to **M5 Air** (or remote Windows 4090 via Ollama).
  * **Pinky / Brain** run on M5 Air or Kender.
* **The Big Win**: Eliminates the 11GB VRAM ceiling pressure on `z87-Linux`. vLLM doesn't have to squeeze into a 5.7GB box with LoRAs, and EarNode/SentenceTransformer never hit CUDA OOM.

---

### **Option B: Method 1 — In-Process CPU Embeddings (`fastembed` / ONNX Runtime)**
* **The Concept**: Keep vLLM on the 2080 Ti, but strip PyTorch embeddings out of the Foyer process by switching MiniLM to a standalone C++ ONNX runtime (`fastembed`) running strictly on **CPU**.
* **The Topology**:
  * Foyer generates 384-dimensional vectors in ~3–5ms using CPU RAM (~50MB).
  * Foyer sends pre-computed vectors to ChromaDB over HTTP.
* **The Big Win**: **0 MB GPU VRAM** consumed by embeddings. Leaves the full VRAM budget for vLLM and EarNode.

---

### **Option C: Method 2 — Client-Server Offload (ChromaDB HTTP / Docker Embedding Service)**
* **The Concept**: The pure "Class 1" decoupling. Foyer becomes a thin async router with **zero ML libraries** (no PyTorch, no ONNX).
* **The Topology**:
  * Foyer sends raw query strings over HTTP to ChromaDB (Port 8001 / Docker).
  * ChromaDB's backend computes the embedding and performs the vector retrieval internally.
* **The Big Win**: Completely decouples Foyer from vector math. Zero ML dependencies in the Foyer process, zero VRAM used by Foyer.

---

## 👂 **2. EarNode (Speech Recognition) Spectrum & Options**

| Option | Architecture & Footprint | Trade-offs & Strategic Value |
| :--- | :--- | :--- |
| **1. Drop EarNode (Text-Only)** | • **0 MB VRAM** / 0 CPU | Pure keyboard Web Intercom. Maximum simplicity, zero audio failure modes, 100% of 2080 Ti VRAM for LLM inference. |
| **2. Keep NeMo Streaming** | • ~1.2–1.5 GB VRAM (FP16)<br>• Requires PyTorch | Streaming frame-by-frame low-latency transcription (`nemotron-speech-0.6b`). Known quantity, already integrated in `sensory_manager.py`. |
| **3. `whisper.cpp` / `faster-whisper`** | • ~150–350 MB VRAM (or pure CPU)<br>• C++ / CTranslate2 | Zero PyTorch CUDA allocator bloat. Highly efficient, battle-tested across home labs, can run fast on CPU or small CUDA footprint. |
| **4. NVIDIA Nemotron VoiceChat 11B** | • 11B multimodal audio-to-text LLM<br>• ~8–12 GB VRAM (Quantized) | Next-gen unified voice-native model (direct speech-to-speech / speech-to-intent). Requires dedicated heavy GPU (fits Kender 4090 or M5 Air, too heavy for 2080 Ti alongside other models). Ref: https://huggingface.co/nvidia/NVIDIA-NemotronLabs-VoiceChat-11B |

---

## 📌 **3. Architectural Decision: Why We Chose Option B (`fastembed` / ONNX)**

* **Selected Approach**: **Option B (In-Process CPU Embeddings via `fastembed`)**
* **Core Rationale**:
  1. **Direct Control**: Foyer directly manages the `all-MiniLM-L6-v2` ONNX model in-process, ensuring 100% consistent 384-dimensional vector embeddings without relying on external container embedding configurations.
  2. **Superior CPU Speed**: Runs via optimized C++ ONNX runtime with AVX2/AVX-512 CPU SIMD instructions (~3ms per embedding, using ~50MB RAM).
  3. **Zero GPU VRAM Impact**: **0 MB VRAM consumed** by embeddings in Foyer. Reclaims ~4 GB of GPU memory for vLLM on the 2080 Ti.
  4. **Zero Quality Loss**: The vector math is mathematically identical to PyTorch FP32/FP16 down to the decimal.

---

## 🛠️ **4. Target Files & Speculative Refactoring Map**

When executing Sprint 57, the following files will be refactored:

1. **[`HomeLabAI/src/nodes/archive_node.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/archive_node.py)**:
   * **Change**: Remove `from sentence_transformers import SentenceTransformer` and PyTorch CUDA context.
   * **Replace with**: `from fastembed import TextEmbedding` (model: `sentence-transformers/all-MiniLM-L6-v2`).
   * **Action**: Generate query embeddings on CPU and pass the raw float array to `chroma_client.query(query_embeddings=[vec])`.

2. **[`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)**:
   * **Change**: Ensure HyDE vector similarity searches and domain routing use the CPU `fastembed` instance rather than triggering CUDA PyTorch allocations.

3. **[`HomeLabAI/src/equipment/sensory_manager.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/equipment/sensory_manager.py)** & **[`ear_node.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/equipment/ear_node.py)**:
   * **Change**: Disable NeMo PyTorch CUDA initialization by default (`EAR_NODE_STUB_MODEL=1`).
   * **Action**: Transition speech transcription to `faster-whisper` on CPU or a dedicated lightweight C++ daemon.

4. **[`HomeLabAI/src/start_vllm.sh`](file:///home/jallred/Dev_Lab/HomeLabAI/src/start_vllm.sh)**:
   * **Change**: With Foyer consuming 0 MB of GPU VRAM, safely increase `--gpu-memory-utilization` from `0.55` up to `0.70`–`0.75` for massive KV-cache buffers and zero out-of-memory risk.

---

## 🧭 **5. The NeMo Reality Check (Why NeMo Must Be Addressed)**
* **The Dependency Trap**: NeMo (`nvidia/nemotron-speech-0.6b`) is fundamentally a PyTorch library. 
* If we migrate MiniLM to CPU/ONNX but still load NeMo into GPU CUDA in Foyer, **the entire VRAM win is moot**: PyTorch's Caching Allocator will still claim ~3–4 GB of VRAM.
* **Conclusion**: Removing PyTorch from the GPU requires *both* moving MiniLM to CPU (`fastembed`) AND disabling/replacing NeMo (`faster-whisper` or text-only).
