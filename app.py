import streamlit as st
import numpy as np

st.set_page_config(page_title="AI Traffic Green Wave Simulator", layout="wide")

st.title("🚦 AI Adaptive Traffic Signal & Green Wave Simulation")

# -------------------------
# SIDEBAR INPUTS
# -------------------------
st.sidebar.header("Simulation Parameters")

num_intersections = st.sidebar.slider("Number of Intersections", 1, 6, 3)

volumes = []
for i in range(num_intersections):
    v = st.sidebar.slider(f"Vehicle Volume Intersection {i+1}", 0, 300, 120)
    volumes.append(v)

lane_capacity = st.sidebar.slider("Lane Capacity", 50, 300, 150)
emergency_idx = st.sidebar.selectbox(
    "Emergency Vehicle At Intersection",
    ["None"] + [f"Intersection {i+1}" for i in range(num_intersections)]
)

# -------------------------
# AI SIGNAL MODEL
# -------------------------
def optimize_signal(volume, capacity, emergency=False):
    base = 30
    alpha = 40
    beta = 50
    density = volume / capacity
    g = base + alpha * density
    if emergency:
        g += beta
    return round(g), density

greens = []
densities = []

for i, v in enumerate(volumes):
    emergency_here = (emergency_idx == f"Intersection {i+1}")
    g, d = optimize_signal(v, lane_capacity, emergency_here)
    greens.append(g)
    densities.append(d)

# -------------------------
# METRICS
# -------------------------
st.subheader("📊 Intersection Metrics")

cols = st.columns(num_intersections)
for i in range(num_intersections):
    cols[i].metric(
        f"Int {i+1} Green (s)",
        greens[i],
        f"Density {round(densities[i]*100,1)}%"
    )

# -------------------------
# GREEN WAVE ANIMATION
# -------------------------
st.subheader("🌊 Multi-Intersection Green Wave Corridor")

cycle = max(greens) + 20
phase_delay = cycle / num_intersections

signals_html = ""
cars_html = ""
queues_html = ""
turn_html = ""

for i in range(num_intersections):
    left = 8 + i * (84 / num_intersections)
    delay = i * phase_delay
    density = densities[i]

    # stop point based on density
    stop = 40 + density * 10

    # signal
    signals_html += f"""
    <div class="signal" style="left:{left}%;">
        <div class="light red"></div>
        <div class="light yellow"></div>
        <div class="light green"></div>
    </div>
    """

    # moving platoon
    cars_html += f"""
    <div class="car" style="animation-delay:{delay}s;"></div>
    """

    # queue vehicles
    queues_html += f"""
    <div class="qcar" style="left:calc({left}% - 30px); animation-delay:{delay}s;"></div>
    <div class="qcar2" style="left:calc({left}% - 60px); animation-delay:{delay}s;"></div>
    """

    # turning car
    turn_html += f"""
    <div class="turn" style="left:{left}%; animation-delay:{delay+1}s;"></div>
    """

# emergency
emergency_html = ""
if emergency_idx != "None":
    emergency_html = """
    <div class="ambulance"></div>
    """

html = f"""
<div style="position:relative; width:100%; height:320px; background:#2c2c2c; border-radius:12px; overflow:hidden;">

  <!-- road -->
  <div style="position:absolute; top:150px; width:100%; height:40px; background:#444;"></div>

  <!-- lane marking -->
  <div style="position:absolute; top:168px; width:100%; height:4px;
       background: repeating-linear-gradient(90deg, white 0px, white 25px, transparent 25px, transparent 50px);"></div>

  {signals_html}
  {queues_html}
  {turn_html}
  {cars_html}
  {emergency_html}

</div>

<style>

.signal {{
    position:absolute;
    top:95px;
    width:26px;
    height:74px;
    background:black;
    border-radius:6px;
    padding:4px;
}}

.light {{
    width:16px;
    height:16px;
    border-radius:50%;
    margin:2px auto;
    background:#222;
}}

.signal .green {{
    animation: greenWave {cycle}s linear infinite;
}}

.signal .yellow {{
    animation: yellowWave {cycle}s linear infinite;
}}

.signal .red {{
    animation: redWave {cycle}s linear infinite;
}}

@keyframes greenWave {{
    0% {{ background:lime; }}
    40% {{ background:lime; }}
    41% {{ background:#030; }}
    100% {{ background:#030; }}
}}

@keyframes yellowWave {{
    0% {{ background:#330; }}
    40% {{ background:#330; }}
    50% {{ background:yellow; }}
    60% {{ background:#330; }}
    100% {{ background:#330; }}
}}

@keyframes redWave {{
    0% {{ background:#300; }}
    60% {{ background:red; }}
    100% {{ background:red; }}
}}

.car {{
    position:absolute;
    top:158px;
    left:-120px;
    width:52px;
    height:24px;
    background:cyan;
    border-radius:6px;
    animation: moveCar {cycle}s linear infinite;
}}

@keyframes moveCar {{
    from {{ left:-120px; }}
    to {{ left:110%; }}
}}

.qcar {{
    position:absolute;
    top:158px;
    width:52px;
    height:24px;
    background:red;
    border-radius:6px;
}}

.qcar2 {{
    position:absolute;
    top:158px;
    width:52px;
    height:24px;
    background:orange;
    border-radius:6px;
}}

.turn {{
    position:absolute;
    top:158px;
    width:52px;
    height:24px;
    background:blue;
    border-radius:6px;
    animation: turnMove 6s linear infinite;
}}

@keyframes turnMove {{
    0% {{ top:158px; }}
    50% {{ top:158px; }}
    70% {{ top:120px; transform:rotate(-90deg); }}
    100% {{ top:-80px; transform:rotate(-90deg); }}
}}

.ambulance {{
    position:absolute;
    top:154px;
    left:-160px;
    width:64px;
    height:26px;
    background:white;
    border:2px solid red;
    border-radius:6px;
    animation: moveCar 4s linear infinite;
}}

</style>
"""

st.components.v1.html(html, height=340)

st.success("AI Coordinated Green Wave Active 🚦")
