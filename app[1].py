import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Multi-Intersection AI Traffic System", layout="wide")

st.title("🚦 AI Enabled Traffic Signal System")

# -----------------------
# Sidebar Inputs
# -----------------------
st.sidebar.header("Simulation Parameters")

num_intersections = st.sidebar.slider("Number of Intersections", 1, 5, 3)
lane_capacity = st.sidebar.slider("Lane Capacity", 50, 300, 150)
emergency = st.sidebar.checkbox("Emergency Vehicle Present")

st.sidebar.subheader("Vehicle Volume per Intersection")

volumes = []
for i in range(num_intersections):
    vol = st.sidebar.slider(f"Intersection {i+1} Volume", 0, 300, 120)
    volumes.append(vol)

# -----------------------
# AI OPTIMIZATION MODEL
# -----------------------

def optimize_signal(volume, capacity, emergency_flag):
    base_time = 30
    alpha = 40
    beta = 50

    density = volume / capacity
    green_time = base_time + (alpha * density)

    if emergency_flag:
        green_time += beta

    return round(green_time), density

green_times = []
densities = []

for v in volumes:
    g, d = optimize_signal(v, lane_capacity, emergency)
    green_times.append(g)
    densities.append(d)

# Global synchronized cycle
yellow_time = 3
red_time = 5
cycle_time = max(green_times) + yellow_time + red_time

# -----------------------
# Metrics
# -----------------------

st.subheader("📊 Intersection Metrics")

cols = st.columns(num_intersections)

for i in range(num_intersections):
    cols[i].metric(
        f"Intersection {i+1} Green Time",
        f"{green_times[i]} sec",
        f"Density: {round(densities[i]*100,2)}%"
    )

# -----------------------
# SYNCHRONIZED SIGNAL ANIMATION
# -----------------------

st.subheader("🚥 Synchronized Traffic Lights")

signal_boxes = [st.empty() for _ in range(num_intersections)]

for t in range(cycle_time):

    for i in range(num_intersections):

        offset = int(i * cycle_time / num_intersections)
        local_time = (t - offset) % cycle_time

        if local_time < green_times[i]:
            signal_boxes[i].markdown(f"### Intersection {i+1} 🟢 GREEN")
        elif local_time < green_times[i] + yellow_time:
            signal_boxes[i].markdown(f"### Intersection {i+1} 🟡 YELLOW")
        else:
            signal_boxes[i].markdown(f"### Intersection {i+1} 🔴 RED")

    time.sleep(0.1)

st.success("Synchronized Cycle Completed")

