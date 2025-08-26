# Battery Performance Simulator (SoC, voltage, temperature, fade)
# Run: python battery_simulator.py
import numpy as np
import matplotlib.pyplot as plt

# --- Config (feel free to tweak) ---
capacity_ah = 20.0          # battery capacity (Ah)
nominal_voltage = 72.0      # pack nominal voltage (V)
internal_resistance = 0.08  # pack internal resistance (Ohm)
ambient_temp = 25.0         # °C
thermal_resistance = 1.8    # °C/W (lumped)
thermal_capacitance = 600.0 # J/°C (lumped)
time_s = 3600               # total sim time (s)
dt = 1.0                    # step (s)

# Current profile: charge at 0.5C for 20min, rest 10min, discharge at 1C to near 20% SoC
steps = int(time_s / dt)
I = np.zeros(steps)
t = np.arange(steps) * dt
half_c = 0.5 * capacity_ah   # A
one_c  = 1.0 * capacity_ah   # A

# 0–1200s: charge (negative current into battery)
I[(t >= 0) & (t < 1200)] = -half_c
# 1200–1800s: rest
I[(t >= 1200) & (t < 1800)] = 0.0
# 1800–3600s: discharge
I[(t >= 1800) & (t < 3600)] = +one_c

# Simple OCV vs SoC (piecewise) for Li-ion (rough shape)
def ocv_from_soc(soc):
    # 0–1 scale SoC
    return (nominal_voltage/1.05) * (0.05 + 0.9*soc + 0.05*np.tanh(6*(soc-0.5)))

soc = 0.60  # initial SoC (0–1)
soc_hist, v_hist, temp_hist, fade_hist = [], [], [], []
temp = ambient_temp
fade = 0.0  # capacity fade in %

for k in range(steps):
    # Coulomb counting
    soc -= (I[k] * dt) / (capacity_ah * 3600.0)
    soc = np.clip(soc, 0.0, 1.0)

    ocv = ocv_from_soc(soc)
    v_term = ocv - I[k]*internal_resistance  # terminal voltage

    # Thermal (simple 1st-order RC)
    power_loss = (I[k]**2) * internal_resistance  # W
    dT = (power_loss * thermal_resistance + (ambient_temp - temp)) / (thermal_resistance * thermal_capacitance)
    temp += dT * dt

    # Very rough degradation model: grows with high temp + high current at low SoC
    stress = max(0.0, (abs(I[k])/(1.0*capacity_ah)) - 0.3)  # above 0.3C is extra stress
    temp_factor = max(0.0, (temp - 35.0) / 20.0)            # >35C adds stress
    soc_factor = max(0.0, (0.4 - soc)) * 1.5                # low SoC increases stress
    fade += (stress + temp_factor + soc_factor) * 1e-4      # % per second (toy)

    soc_hist.append(soc*100.0)
    v_hist.append(v_term)
    temp_hist.append(temp)
    fade_hist.append(fade)

# --- Plots ---
plt.figure(figsize=(9,6))
plt.subplot(3,1,1); plt.plot(t/60, soc_hist); plt.ylabel("SoC (%)"); plt.grid(True)
plt.title("Battery Performance Simulation")
plt.subplot(3,1,2); plt.plot(t/60, v_hist); plt.ylabel("Voltage (V)"); plt.grid(True)
plt.subplot(3,1,3); plt.plot(t/60, temp_hist, label="Temp (°C)")
plt.plot(t/60, np.array(fade_hist), label="Fade (%)")
plt.xlabel("Time (min)"); plt.legend(); plt.grid(True)
plt.tight_layout(); plt.show()
