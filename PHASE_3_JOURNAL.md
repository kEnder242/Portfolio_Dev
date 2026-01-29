# Phase 3 Journal: Building the Neural Uplink
**Date:** January 29, 2026
**Topic:** Observability Stack (Prometheus, Grafana, & Custom Telemetry)

---

## 1. The Mission
We have a "Brain" (Pinky/Mistral-7B) running on local hardware. We need to see how much energy it consumes and how hot it runs *without* manually checking logs.
**Goal:** Build a "Mission Control" dashboard that visualizes System Load, Temperature, and Power Consumption in real-time.

## 2. The Stack (Infrastructure as Code)
Instead of installing binaries manually, we used **Docker Compose** to define the entire stack as a reproducible unit.

### The Components
1.  **Prometheus (`:9090`):** The time-series database. It "scrapes" metrics from endpoints every 15 seconds.
2.  **Grafana (`:3000`):** The visualization layer. It queries Prometheus and draws pretty graphs.
3.  **Node Exporter (`:9100`):** A standard tool that exposes Linux kernel metrics (CPU, RAM, Disk).
4.  **RAPL Sim (`:8000`):** Our *custom* Python script. This is the "Special Sauce" that translates raw thermal data into "Power Watts" metrics.

### Key Configuration (`docker-compose.yml`)
We mapped specific volumes to give the containers "X-Ray Vision" into the host:
```yaml
    volumes:
      - /proc:/host/proc:ro   # Let Node Exporter read processes
      - /sys:/host/sys:ro     # Let it read hardware sensors
```
*Insight:* Without these read-only (`:ro`) mounts, the container is blind to the actual host hardware.

## 3. The Custom Exporter (RAPL Sim)
Standard tools weren't enough. We needed to validate power throttling logic. We wrote a simple Python web server (`monitor/rapl_sim/app.py`) using the `prometheus_client` library.

**The Code Pattern:**
```python
# Define a Gauge (a metric that goes up and down)
M_PKG_POWER = Gauge('val_package_power_watts', 'Simulated Package Power')

# In the main loop:
while True:
    # 1. Read Real Data (from /sys/class/thermal...)
    temp = read_thermal_zone()
    
    # 2. Apply Logic (The "Sim")
    power = calculate_watts(temp, load)
    
    # 3. Publish to Prometheus
    M_PKG_POWER.set(power)
```
*Insight:* Writing a custom exporter is surprisingly easy. It's just a while-loop that updates global variables exposed on an HTTP port.

## 4. The "Provisioning" Setback
**The Problem:** We didn't want to manually create the dashboard in the UI every time we restarted Docker. If we destroyed the container, our beautiful graphs would vanish.

**The Solution:** Grafana **Provisioning**.
We told Grafana to look for config files on startup by mounting a local directory:
```yaml
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
```

**The File Structure:**
1.  `datasources/prometheus.yml`: Tells Grafana "Prometheus is at `http://prometheus:9090`."
2.  `dashboards/dashboard.yml`: Tells Grafana "Look for JSON files in this folder."
3.  `dashboards/pinky_dashboard.json`: The actual layout of the panels.

*Lesson:* "ClickOps" (doing things in the GUI) is technical debt. Always define your dashboards as code (JSON) so they are version-controlled.

## 5. Designing the Dashboard
We chose three specific visualizations to tell a story:

1.  **Neural Uplink Load (Gauge):**
    *   *Metric:* `hw_cpu_load_percent`
    *   *Why:* Immediate "Is it thinking?" feedback. Green (<60%) means capacity available.

2.  **Core Temperature (Gauge):**
    *   *Metric:* `hw_temp_package_celsius`
    *   *Why:* Safety. If this hits Red (>75C), the cooling solution is failing.

3.  **Power Profile (Time Series):**
    *   *Metric A:* `val_package_power_watts` (Yellow Line)
    *   *Metric B:* `val_pl1_limit_watts` (Green Threshold)
    *   *Insight:* This graph visualizes our *Validation Logic*. If the Yellow line crosses the Green line, we know our throttling code failed.

## 6. Execution Commands
Here is the cheat sheet for managing this stack:

```bash
# Start the stack
docker-compose -f monitor/docker-compose.yml up -d

# Check if metrics are flowing (Raw Data)
curl localhost:8000/metrics | grep val_package_power

# Reload Grafana configs without restarting
docker restart field_grafana
```

## 7. Final Insight
Observability is not just about "checking if it's up." It is about **visualizing the constraints**. By graphing the *Limit* alongside the *Actual*, we turned a monitoring tool into a Validation Tool.
