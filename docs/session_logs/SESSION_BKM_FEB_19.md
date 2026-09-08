# Post-Silicon Recovery BKM: Driver 550 Resurgence

### 1. Silicon Verification (Mandatory)
Run `nvidia-smi`. It must report **550.120** and **CUDA 12.4** (or 12.8 depending on the installer). If it fails, do not proceed.

### 2. Infrastructure Resurrection
The following services were "Hammered" to secure the void and may need manual starting if they don't auto-start:
- `sudo systemctl start docker containerd` (Restores container engine).
- `sudo systemctl start sysstat` (Restores system telemetry).
- `sudo systemctl start gdm3` (Restores GUI/Display).
- `sudo systemctl start sunshine` (Restores Moonlight streaming).

### 3. Lab Watchdog Restoration
The **Lab Attendant** is the heart of the co-pilot. Start it to autonomously bring up the AI nodes:
- `nohup ./HomeLabAI/.venv/bin/python3 HomeLabAI/src/lab_attendant.py > attendant.log 2>&1 &`

### 4. Housekeeping
Remove the "Blinding" config used to trick the kernel:
- `sudo rm /etc/modprobe.d/temp_blind.conf`
- `sudo update-initramfs -u -k all`
- `rm ~/nvidia_550.run` (Once verified stable).

---
**BKM Note:** Future kernel updates may re-introduce the "Bully" kernels. Always check `uname -r` after a system update.
