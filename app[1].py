import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🚦 AI Smart Crossroad Traffic Simulation (Research Model)")

# -----------------------
# SIDEBAR CONTROLS
# -----------------------

st.sidebar.header("Traffic Parameters")

lane_capacity = st.sidebar.slider("Lane Capacity", 50, 300, 150)

directions = ["North", "South", "East", "West"]

volumes = {}
for d in directions:
    volumes[d] = st.sidebar.slider(f"{d} Volume", 0, 300, 120)

st.sidebar.subheader("🚑 Emergency Vehicle")
emergency_dir = st.sidebar.selectbox(
    "Select Emergency Direction",
    ["None"] + directions
)

# -----------------------
# AI SIGNAL OPTIMIZATION
# -----------------------

def optimize_green(volume, capacity, emergency=False):
    base = 20
    alpha = 40
    beta = 30
    density = volume / capacity
    green = base + alpha * density
    if emergency:
        green += beta
    return int(green)

ns_volume = volumes["North"] + volumes["South"]
ew_volume = volumes["East"] + volumes["West"]

ns_green = optimize_green(ns_volume, lane_capacity,
                          emergency_dir in ["North","South"])
ew_green = optimize_green(ew_volume, lane_capacity,
                          emergency_dir in ["East","West"])

yellow_time = 4
cycle_time = ns_green + ew_green + 2 * yellow_time

st.subheader("📊 Adaptive Signal Timing")
col1, col2 = st.columns(2)
col1.metric("NS Green Time", f"{ns_green} sec")
col2.metric("EW Green Time", f"{ew_green} sec")

# -----------------------
# IDM PARAMETERS
# -----------------------

v0 = 13
a_max = 1.5
b = 2.0
delta = 4
T = 1.5
s0 = 2
dt = 0.2

road_limit = 100
center = 50
stop_line = 48

# -----------------------
# INITIALIZE VEHICLES
# -----------------------

vehicle_positions = {}
vehicle_speeds = {}

for d in directions:
    count = int(volumes[d] * 0.15)
    vehicle_positions[d] = list(np.linspace(90, 70, count))
    vehicle_speeds[d] = [0.0]*count

# -----------------------
# SIMULATION VISUALIZATION
# -----------------------

st.subheader("🚗 4-Way Crossroad Microscopic Simulation")

fig, ax = plt.subplots(figsize=(6,6))
plot_area = st.pyplot(fig)

for t in range(cycle_time):

    ax.clear()
    ax.set_xlim(0, road_limit)
    ax.set_ylim(0, road_limit)

    ax.axhline(center)
    ax.axvline(center)

    phase_time = t % cycle_time

    # Phase determination
    if phase_time < ns_green:
        ns_active = True
        ew_active = False
    elif phase_time < ns_green + yellow_time:
        ns_active = False
        ew_active = False
    elif phase_time < ns_green + yellow_time + ew_green:
        ns_active = False
        ew_active = True
    else:
        ns_active = False
        ew_active = False

    for d in directions:

        if emergency_dir == d:
            green = True
        elif d in ["North", "South"]:
            green = ns_active
        else:
            green = ew_active

        new_pos = []
        new_speed = []

        vehicles = list(zip(vehicle_positions[d], vehicle_speeds[d]))
        vehicles.sort()

        for idx, (pos, speed) in enumerate(vehicles):

            # Red light stopping rule
            if not green and pos <= stop_line:
                accel = -b
            else:
                if idx == 0:
                    gap = pos
                    delta_v = 0
                else:
                    front_pos, front_speed = vehicles[idx-1]
                    gap = pos - front_pos - 2
                    delta_v = speed - front_speed

                s_star = s0 + speed*T + (speed*delta_v)/(2*np.sqrt(a_max*b))
                accel = a_max*(1 - (speed/v0)**delta - (s_star/max(gap,0.1))**2)

            speed = max(0, speed + accel*dt)
            pos = pos - speed*dt

            if pos > 0:
                new_pos.append(pos)
                new_speed.append(speed)

        # stochastic arrivals
        arrival_rate = volumes[d] / 300
        if np.random.rand() < arrival_rate:
            new_pos.append(95)
            new_speed.append(0)

        vehicle_positions[d] = new_pos
        vehicle_speeds[d] = new_speed

        # Draw vehicles
        for pos in new_pos:
            if d == "North":
                ax.scatter(center, pos, s=40)
            elif d == "South":
                ax.scatter(center, road_limit-pos, s=40)
            elif d == "East":
                ax.scatter(road_limit-pos, center, s=40)
            elif d == "West":
                ax.scatter(pos, center, s=40)

    # Draw signal indicators
    ax.text(center-5, center+12, "🟢" if ns_active else "🔴")
    ax.text(center-5, center-12, "🟢" if ns_active else "🔴")
    ax.text(center+12, center-5, "🟢" if ew_active else "🔴")
    ax.text(center-12, center-5, "🟢" if ew_active else "🔴")

    plot_area.pyplot(fig)
    time.sleep(0.1)

st.success("Simulation Completed")