import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AI Smart Traffic Simulation", layout="wide")

st.title("🚦 AI-Based Multi-Intersection Traffic Simulation")

# -----------------------
# Sidebar Controls
# -----------------------

st.sidebar.header("Simulation Controls")

num_intersections = st.sidebar.slider("Number of Intersections", 1, 5, 3)
lane_capacity = st.sidebar.slider("Lane Capacity", 50, 300, 150)

st.sidebar.subheader("Vehicle Volume per Intersection")

volumes = []
for i in range(num_intersections):
    vol = st.sidebar.slider(f"Intersection {i+1} Volume", 0, 300, 120, key=f"vol_{i}")
    volumes.append(vol)

st.sidebar.subheader("🚑 Emergency Vehicle")

emergency_intersection = st.sidebar.selectbox(
    "Select Emergency Intersection",
    ["None"] + [f"Intersection {i+1}" for i in range(num_intersections)]
)

# -----------------------
# AI Optimization Model
# -----------------------

def optimize_signal(volume, capacity, emergency_flag):
    base_time = 30
    alpha = 40
    beta = 60

    density = volume / capacity
    green_time = base_time + (alpha * density)

    if emergency_flag:
        green_time += beta

    return round(green_time), density


green_times = []
densities = []

for i, v in enumerate(volumes):
    is_emergency = (emergency_intersection == f"Intersection {i+1}")
    g, d = optimize_signal(v, lane_capacity, is_emergency)
    green_times.append(g)
    densities.append(d)

yellow_time = 3
red_time = 5
cycle_time = max(green_times) + yellow_time + red_time

# -----------------------
# Display Metrics
# -----------------------

st.subheader("📊 Intersection Metrics")

cols = st.columns(num_intersections)

for i in range(num_intersections):
    priority = (emergency_intersection == f"Intersection {i+1}")
    label = f"Intersection {i+1}"
    if priority:
        label += " 🚑 PRIORITY"

    cols[i].metric(
        label,
        f"{green_times[i]} sec",
        f"Density: {round(densities[i]*100,2)}%"
    )

# -----------------------
# Combined Queue + Moving Vehicle Simulation
# -----------------------

st.subheader("🚗 Live Signal + Queue + Vehicle Movement")

fig, ax = plt.subplots(figsize=(10, 5))
plot_area = st.pyplot(fig)

road_length = 100
vehicle_positions = []

# Initialize vehicles
for v in volumes:
    count = int(v * 0.2)
    positions = np.linspace(0, 20, count)
    vehicle_positions.append(list(positions))

arrival_rates = [v / 60 for v in volumes]
service_speed_normal = 2
service_speed_emergency = 5

queues = [int(v * 0.3) for v in volumes]

for t in range(cycle_time):

    ax.clear()
    ax.set_xlim(0, road_length)
    ax.set_ylim(0, num_intersections + 1)
    ax.set_title("Microscopic Traffic Simulation")
    ax.set_xlabel("Road Length")
    ax.set_ylabel("Intersection")

    for i in range(num_intersections):

        is_emergency = (emergency_intersection == f"Intersection {i+1}")

        offset = int(i * cycle_time / num_intersections)
        local_time = (t - offset) % cycle_time

        # Determine signal state
        if is_emergency:
            signal_state = "GREEN"
        elif local_time < green_times[i]:
            signal_state = "GREEN"
        elif local_time < green_times[i] + yellow_time:
            signal_state = "YELLOW"
        else:
            signal_state = "RED"

        speed = service_speed_emergency if is_emergency else service_speed_normal

        new_positions = []

        # Move vehicles
        for pos in vehicle_positions[i]:
            if signal_state == "GREEN":
                pos += speed
            if pos < road_length:
                new_positions.append(pos)

        # Arrival during RED
        if signal_state == "RED":
            arrivals = int(arrival_rates[i])
            for _ in range(arrivals):
                new_positions.append(0)

        vehicle_positions[i] = new_positions
        queues[i] = len(vehicle_positions[i])

        y_level = num_intersections - i

        # Draw vehicles
        ax.scatter(vehicle_positions[i],
                   [y_level]*len(vehicle_positions[i]),
                   s=80)

        # Draw traffic signal
        if signal_state == "GREEN":
            color = "green"
        elif signal_state == "YELLOW":
            color = "yellow"
        else:
            color = "red"

        ax.text(95, y_level, "●", fontsize=18, color=color)

        # Show queue text
        ax.text(5, y_level+0.2,
                f"Queue: {queues[i]}",
                fontsize=9)

    plot_area.pyplot(fig)
    time.sleep(0.12)

st.success("Simulation Cycle Completed")