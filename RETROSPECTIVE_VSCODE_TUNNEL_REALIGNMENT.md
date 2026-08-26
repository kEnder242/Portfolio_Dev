# Retrospective: VS Code Tunnel Realignment & Assumption Audit
**Date:** August 26, 2026  
**Status:** Canonical Reference  
**Subject:** Resolving the False "Phantom Service" Assumption, Dual-Server Divergence, and Unified Remote Strategy

---

## 1. Executive Summary & Root Cause Realignment

For several sprints, documentation in `LAB_INFRASTRUCTURE.md` asserted that `code-tunnel.service` was a "phantom unit with no unit file" and concluded that `~/.vscode-server/` (spawned ad-hoc via Remote-SSH) was the sole operational interface. 

A forensic audit of the Linux host revealed that **this assumption was entirely false**:
1. `code-tunnel.service` has been an active, operational **systemd user unit** since **March 2, 2026** (`~/.config/systemd/user/code-tunnel.service` pointing to `/home/jallred/.vscode/cli/code-tunnel.service`).
2. It manages a persistent, official Microsoft Dev Tunnel named **`z87-linux`** (ID: `new-ant-jp88mhk`, Cluster: `usw2`), consuming a constant ~9.8 MB of RAM.
3. The previous audit misidentified it as "phantom" because it only checked system-level paths (`/etc/systemd/system/`) with `systemctl list-unit-files`, completely overlooking user-level systemd units (`systemctl --user`).

---

## 2. The Dual-Server Divergence (Why VS Code Got Slow & Flaky)

The confusion caused the environment to diverge into two competing, desynchronized connection mechanisms:

| Dimension | Native Dev Tunnel (`code-tunnel.service`) | Remote-SSH (`~/.vscode-server/`) |
|:---|:---|:---|
| **Scope** | Persistent systemd user service (`~/.config/systemd/user/`) | Ephemeral per-session child process spawned over SSH |
| **Binary** | `/usr/share/code/bin/code-tunnel` (Official Debian `code` package) | Auto-downloaded node binaries in `~/.vscode-server/cli/servers/<hash>/` |
| **Communication** | Outbound WebSocket to Microsoft Dev Tunnels Relay (`wss://...rel.tunnels.api.visualstudio.com`) | Inbound SSH (`port 22`) attaching to Unix domain sockets in `/tmp/code-*` |
| **State Storage** | `~/.vscode/cli/` | `~/.vscode-server/` |
| **Failure Mode** | Survives crashes & reboots automatically via systemd user manager | Abrupt reboot leaves stale `pid.txt` and `.token` on disk, causing `AsyncPipeFailed (Os 2 NotFound)` |

### The Settings Regression
When `AsyncPipeFailed` occurred on the Remote-SSH path, applying settings workarounds on Windows (`"remote.SSH.useLocalServer": false`, `"remote.SSH.useExecServer": false`) forced the SSH client into a sluggish, unoptimized Node-spawn fallback loop. This introduced heavy latency into file tree navigation and terminal rendering.

---

## 3. Audit of Misleading "Missing" Claims Across Ledgers

An audit of `FeatureTracker.md` and `LAB_INFRASTRUCTURE.md` revealed a recurring pattern:
* **The Repo Boundary Blindspot:** Automated repo auditors previously scanned only `HomeLabAI/src/` and `Portfolio_Dev/` for Python/JS code.
* **The False "Missing" Label:** OS-level configurations (such as `/etc/systemd/system/`, `/etc/sysctl.d/`, `/etc/modprobe.d/`, `/etc/default/earlyoom`, and `~/.config/systemd/user/`) were routinely marked as `Code: *none found (documented only)*` or "phantom" simply because they lived outside the git repository roots.
* **Remediation Rule:** Any future architecture audit must inspect the live system state (`systemctl --user`, `/etc/`, `/proc/`) before asserting that a component or service is missing.

---

## 4. Single-Server Unification & Upgrade Plan

To eliminate server divergence and ensure rock-solid stability, the lab is standardizing on **`code-tunnel.service`** as the primary connection layer:

### Phase 1: Upgrade `code` Package (Debian / Microsoft Repository)
1. The currently installed Debian package `/usr/share/code/bin/code-tunnel` is `1.127.0`.
2. The candidate in Microsoft's repository is `1.134.0+`.
3. Upgrading via `sudo apt update && sudo apt install --only-upgrade code` immediately upgrades the tunnel binary without modifying configuration or tunnel registration.

### Phase 2: Client Standardization
1. **Remove Windows Emulation Flags:** Revert `"remote.SSH.useLocalServer"` and `"remote.SSH.useExecServer"` back to default in Windows VS Code settings.
2. **Connect via Dev Tunnel:** In Windows VS Code, connect directly via `Remote Tunnels: Connect to Tunnel...` $\rightarrow$ `z87-linux`.
3. **SSH Lifeline as Fallback:** Remote-SSH remains protected by `~/.ssh/rc` pre-flight PID validation and `OOMScoreAdjust=-1000` solely as an out-of-band terminal lifeline.
