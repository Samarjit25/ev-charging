# EV Charging Cost & Degradation Impact (motorcycle-class EV)
# Run: python charging_cost_calculator.py
import math

# --- Inputs (edit these) ---
battery_kWh = 4.0          # total capacity
start_soc = 0.20           # fraction 0–1
end_soc = 0.90             # fraction 0–1
charger_power_kW = 3.0     # AC wallbox example
tariff_rs_per_kWh = 9.0    # local electricity price
charge_efficiency = 0.92   # wall->pack
mode = "fast"              # "slow" or "fast"

# Simple degradation model: equivalent full cycle cost
# Assume 1200 cycles at slow charging to 80% DoD; fast charging reduces life.
base_cycle_life = 1200
fast_penalty = 0.75        # life multiplier for fast charging (e.g., 25% fewer cycles)
degradation_cost_rs_per_kWh = 1.5  # fictional amortized health cost per kWh throughput

def energy_needed_kWh(batt, s_soc, e_soc):
    return batt * max(0.0, e_soc - s_soc)

def charge_time_hours(energy_kWh, power_kW, eff):
    grid_energy = energy_kWh / eff
    return grid_energy / max(0.2, power_kW)

def cost_rs(grid_energy_kWh, tariff):
    return grid_energy_kWh * tariff

def health_cost_rs(energy_kWh, mode, per_kWh_cost, fast_penalty):
    mult = 1.0 if mode == "slow" else (1.0/fast_penalty)
    return energy_kWh * per_kWh_cost * mult

if __name__ == "__main__":
    E_pack = energy_needed_kWh(battery_kWh, start_soc, end_soc)  # added to pack
    E_grid = E_pack / charge_efficiency                         # drawn from grid
    hours = charge_time_hours(E_pack, charger_power_kW, charge_efficiency)
    rupees = cost_rs(E_grid, tariff_rs_per_kWh)
    health_rs = health_cost_rs(E_pack, mode, degradation_cost_rs_per_kWh, fast_penalty)

    print("=== EV Charging Cost & Health Impact ===")
    print(f"Battery               : {battery_kWh:.2f} kWh")
    print(f"From SoC -> To SoC    : {start_soc*100:.0f}% -> {end_soc*100:.0f}%")
    print(f"Charger Power         : {charger_power_kW:.1f} kW | Mode: {mode}")
    print(f"Efficiency (wall->pack): {charge_efficiency:.2f}")
    print(f"\nEnergy to battery     : {E_pack:.2f} kWh")
    print(f"Energy from grid      : {E_grid:.2f} kWh")
    print(f"Time to charge        : {hours:.2f} h")
    print(f"Electricity cost      : ₹{rupees:.2f}")
    print(f"Degradation cost est. : ₹{health_rs:.2f}")
    print(f"Total estimated cost  : ₹{rupees + health_rs:.2f}")
    print("\nNote: Degradation cost is a simplified proxy for interview discussion (not a lab-grade model).")
