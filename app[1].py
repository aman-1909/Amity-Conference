import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Research AI Traffic Simulator", layout="wide")

st.title("🚦 Research-Level AI Adaptive Traffic Signal System")

# -----------------------
# Sidebar Inputs
# -----------------------
st.sidebar.header("Simulation Parameters")

num_intersections = st.sidebar.slider("Number of Intersections", 1, 6, 2)
vehicle_volume = st.sidebar.slider("Vehicle Volume per Lane", 0, 300, 120)
lane_capacity = st.sidebar.slider("Lane Capacity", 50, 300, 150)
emergency = st.sidebar.checkbox("Emergency Vehicle Present")

# -----------------------
# AI MODEL
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

green_time, density = optimize_signal(vehicle_volume, lane_capacity, emergency)

# -----------------------
# Performance Estimation
# -----------------------

avg_wait_time = max(5, 120 - green_time)
throughput = int(vehicle_volume * (green_time / 120))
congestion_score = round(density * 100, 2)

# -----------------------
# Output Metrics
# -----------------------

col1, col2, col3 = st.columns(3)

col1.metric("Green Signal Time (sec)", green_time)
col2.metric("Estimated Avg Waiting Time (sec)", avg_wait_time)
col3.metric("Congestion Score (%)", congestion_score)

# -----------------------
# Animated Signal
# -----------------------

st.subheader("🚥 Live Signal Simulation")

signal_box = st.empty()
timer_box = st.empty()

for sec in range(green_time, 0, -1):
    signal_box.markdown("## 🟢 GREEN")
    timer_box.markdown(f"### Time Remaining: {sec} sec")
    time.sleep(0.05)

signal_box.markdown("## 🟡 YELLOW")
time.sleep(1)

signal_box.markdown("## 🔴 RED")
time.sleep(1)

st.success("Cycle Completed")



# -----------------------
# Multi Intersection Summary
# -----------------------

st.subheader("📍 Intersection Summary")

for i in range(num_intersections):
    st.write(f"Intersection {i+1} → Green Time: {green_time} sec | Throughput: {throughput} vehicles")
