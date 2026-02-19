import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚦 AI Priority Traffic Signal Simulation")
st.subheader("Three-Road Intelligent Intersection (North–South–West)")

# ================= CONTROLS =================
st.sidebar.header("Traffic Settings")

north = st.sidebar.slider("North Traffic", 0, 10, 5)
south = st.sidebar.slider("South Traffic", 0, 10, 5)
west = st.sidebar.slider("West Traffic", 0, 10, 5)

emergency = st.sidebar.selectbox(
    "Emergency Lane",
    ["None", "North", "South", "West"]
)

# ================= HTML SIM =================
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

body {{
    margin:0;
    background:#0f172a;
    font-family:sans-serif;
}}

.road {{
    position:absolute;
    background:#374151;
}}

#northRoad {{ width:80px; height:260px; left:50%; transform:translateX(-50%); top:0; }}
#southRoad {{ width:80px; height:260px; left:50%; transform:translateX(-50%); bottom:0; }}
#westRoad  {{ height:80px; width:260px; left:0; top:50%; transform:translateY(-50%); }}

.signal {{
    position:absolute;
    width:28px;
    height:70px;
    background:#111827;
    border-radius:6px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:space-around;
    padding:4px;
}}

.light {{
    width:14px;
    height:14px;
    border-radius:50%;
    background:#222;
}}

#northSignal {{ top:270px; left:50%; transform:translateX(-50%); }}
#southSignal {{ bottom:270px; left:50%; transform:translateX(-50%); }}
#westSignal  {{ left:270px; top:50%; transform:translateY(-50%); }}

.bar {{
    position:absolute;
    background:#22c55e;
    opacity:0.8;
}}

#northBar {{ width:20px; left:50%; transform:translateX(-50%); bottom:300px; }}
#southBar {{ width:20px; left:50%; transform:translateX(-50%); top:300px; }}
#westBar  {{ height:20px; top:50%; transform:translateY(-50%); left:300px; }}

.emergency {{
    box-shadow:0 0 10px 3px yellow;
}}

</style>
</head>

<body>

<div id="northRoad" class="road"></div>
<div id="southRoad" class="road"></div>
<div id="westRoad"  class="road"></div>

<div id="northSignal" class="signal">
    <div class="light" id="nRed"></div>
    <div class="light" id="nYellow"></div>
    <div class="light" id="nGreen"></div>
</div>

<div id="southSignal" class="signal">
    <div class="light" id="sRed"></div>
    <div class="light" id="sYellow"></div>
    <div class="light" id="sGreen"></div>
</div>

<div id="westSignal" class="signal">
    <div class="light" id="wRed"></div>
    <div class="light" id="wYellow"></div>
    <div class="light" id="wGreen"></div>
</div>

<div id="northBar" class="bar"></div>
<div id="southBar" class="bar"></div>
<div id="westBar"  class="bar"></div>

<script>

let north = {north};
let south = {south};
let west  = {west};
let emergency = "{emergency}";

let green = "North";

function chooseGreen() {{
    if(emergency !== "None") {{
        green = emergency;
        return;
    }}

    let v = {{
        "North":north,
        "South":south,
        "West":west
    }};
    green = Object.keys(v).reduce((a,b)=>v[a]>v[b]?a:b);
}}

function resetLights() {{
    document.querySelectorAll(".light").forEach(l=>l.style.background="#222");
}}

function setSignal(lane) {{
    resetLights();

    if(lane=="North") {{
        nGreen.style.background="lime";
        sRed.style.background="red";
        wRed.style.background="red";
    }}
    if(lane=="South") {{
        sGreen.style.background="lime";
        nRed.style.background="red";
        wRed.style.background="red";
    }}
    if(lane=="West") {{
        wGreen.style.background="lime";
        nRed.style.background="red";
        sRed.style.background="red";
    }}
}}

function updateBars() {{
    northBar.style.height = north*12 + "px";
    southBar.style.height = south*12 + "px";
    westBar.style.width  = west*12 + "px";
}}

function highlightEmergency() {{
    document.querySelectorAll(".signal").forEach(s=>s.classList.remove("emergency"));
    if(emergency=="North") northSignal.classList.add("emergency");
    if(emergency=="South") southSignal.classList.add("emergency");
    if(emergency=="West")  westSignal.classList.add("emergency");
}}

function cycle() {{
    chooseGreen();
    setSignal(green);
    highlightEmergency();
}}

updateBars();
cycle();
setInterval(cycle,3000);

</script>
</body>
</html>
"""

components.html(html, height=600)

# ================= INFO =================
st.markdown("---")
st.markdown(
"""
### 🚀 Project Description
AI-controlled adaptive traffic signal for three-road intersections.

Features:
- Dynamic green selection by traffic density
- Emergency vehicle priority override
- Real-time signal visualization
- Queue density representation

### 👨‍💻 Made by Aman Kumar
"""
)