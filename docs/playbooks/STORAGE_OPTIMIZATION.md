# Storage Optimization Plan (Feb 18, 2026)

## 📊 Current State (Home Directory: 522GB Used)
- **Top Consumer:** `~/.steam` (455GB) - Atomic Heart, Elden Ring, No Man's Sky.
- **Cache Bloat:** `~/.cache` (21GB) - HuggingFace models & Pip.
- **Project Space:** `~/Dev_Lab` (20GB).

## 🛠️ Recommendations

### 1. Relocate Steam Library (High Impact)
Move the bulk of `.steam` to the **1.8TB drive** (`/mnt/2TB`).
- **Path:** `/mnt/2TB/SteamLibrary`
- **Action:** Use Steam's "Move Install Folder" feature or a symlink. 
- **Gain:** ~400GB reclaimed in home.

### 2. Offload AI Models to /speedy (Performance Gain)
Utilize the **150GB SSD** (`/speedy`) for high-throughput model access.
- **Path:** `/speedy/models`
- **Action:** Set `HF_HOME=/speedy/models` in `.bashrc` and move existing caches.
- **Gain:** Reduced latency for vLLM weight loading + 8.4GB reclaimed in home.

### 3. Move Jellyfin Metadata/Temp (Optional)
If Jellyfin transcoding happens in home, point the transcode path to `/speedy/transcode`.

## 🚀 Execution Strategy
I will wait for human architect approval before moving any non-project files (like Steam games).
