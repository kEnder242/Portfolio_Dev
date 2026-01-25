import time
import os
from prometheus_client import start_http_server, Gauge

# --- Configuration ---
PL1_LIMIT_WATTS = 65.0
BASE_POWER_WATTS = 25.0
MAX_TURBO_WATTS = 95.0

# --- Metrics Definition ---
# Real Telemetry
M_TEMP_PKG = Gauge('hw_temp_package_celsius', 'Real Package Temperature from Thermal Zone')
M_CPU_LOAD = Gauge('hw_cpu_load_percent', 'Real System CPU Load %')

# Validation Logic (The "Sim")
M_PKG_POWER = Gauge('val_package_power_watts', 'Simulated Package Power based on Load/Temp')
M_PL1_LIMIT = Gauge('val_pl1_limit_watts', 'Active Power Limit (PL1)')
M_THROTTLE  = Gauge('val_throttling_active', '1 if Simulated Power exceeds Limit', ['reason'])

def get_cpu_load():
    """ Reads /proc/stat to calculate CPU load % since last read. """
    # Simplified for demo: return a basic load factor (0.0 to 1.0)
    # In a real exporter, we'd calc diff between two timestamps.
    # For now, we use Load Avg (1min) normalized by core count (8 threads)
    try:
        load1, _, _ = os.getloadavg()
        return min(load1 / 8.0, 1.0) * 100.0
    except:
        return 10.0 # Fallback

def get_real_temp():
    """ Reads thermal_zone0 from the mounted host directory. """
    try:
        # Docker mount: /host/sys/class/thermal/thermal_zone0/temp
        with open('/host/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            # Value is in millidegrees (27800 = 27.8C)
            return int(f.read().strip()) / 1000.0
    except Exception as e:
        print(f"Error reading temp: {e}")
        return 35.0 # Fallback

def calculate_power(load_pct, temp_c):
    """ The Physics Model: Power = Base + Dynamic(Load) + Leakage(Temp) """
    dynamic_power = (load_pct / 100.0) * (MAX_TURBO_WATTS - BASE_POWER_WATTS)
    leakage_power = (temp_c - 25.0) * 0.1 # 0.1W per degree above ambient
    
    total = BASE_POWER_WATTS + dynamic_power + max(leakage_power, 0)
    return round(total, 2)

if __name__ == '__main__':
    # Start Prometheus Server on Port 8000
    start_http_server(8000)
    print("RAPL Sim Exporter running on :8000")
    print(f"Monitoring: /host/sys/class/thermal/thermal_zone0/temp")

    while True:
        # 1. Acquire Real Data
        real_load = get_cpu_load()
        real_temp = get_real_temp()

        # 2. Update Real Metrics
        M_CPU_LOAD.set(real_load)
        M_TEMP_PKG.set(real_temp)

        # 3. Validation Logic (The Sim)
        sim_power = calculate_power(real_load, real_temp)
        
        # Check Throttling
        if sim_power > PL1_LIMIT_WATTS:
            # Clamp the power to the limit (Simulating FW clamping)
            M_PKG_POWER.set(PL1_LIMIT_WATTS)
            M_THROTTLE.labels(reason='PL1').set(1)
        else:
            M_PKG_POWER.set(sim_power)
            M_THROTTLE.labels(reason='PL1').set(0)

        M_PL1_LIMIT.set(PL1_LIMIT_WATTS)

        time.sleep(1)
