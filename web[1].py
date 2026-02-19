import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚦 AI Priority Traffic Signal Simulation")
st.subheader("Three-Road Intelligent Intersection (North–South–West)")

# ===== SIDEBAR =====
st.sidebar.header("Traffic Density")

north = st.sidebar.slider("North", 0, 10, 6)
south = st.sidebar.slider("South", 0, 10, 4)
west = st.sidebar.slider("West", 0, 10, 3)

emergency = st.sidebar.selectbox(
    "Emergency Lane",
    ["None", "North", "South", "West"]
)

# ===== HTML =====
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

body {{
    margin:0;
    background:#0f172a;
}}

.road {{
    position:absolute;
    background:#d1d5db;
}}

#northRoad {{ width:90px;height:280px;left:50%;transform:translateX(-50%);top:0; }}
#southRoad {{ width:90px;height:280px;left:50%;transform:translateX(-50%);bottom:0; }}
#westRoad  {{ height:90px;width:280px;left:0;top:50%;transform:translateY(-50%); }}

.signal {{
    position:absolute;
    width:36px;
    height:110px;
    background:#111827;
    border-radius:10px;
    display:flex;
    flex-direction:column;
    justify-content:space-around;
    align-items:center;
    padding:6px;
}}

.light {{
    width:18px;
    height:18px;
    border-radius:50%;
    background:#222;
    box-shadow:none;
}}

.glow-red    {{ background:#ef4444; box-shadow:0 0 12px #ef4444; }}
.glow-yellow {{ background:#facc15; box-shadow:0 0 12px #facc15; }}
.glow-green  {{ background:#22c55e; box-shadow:0 0 12px #22c55e; }}

#northSig {{ top:300px; left:50%; transform:translateX(-50%); }}
#southSig {{ bottom:300px; left:50%; transform:translateX(-50%); }}
#westSig  {{ left:300px; top:50%; transform:translateY(-50%); }}

.emergency {{
    box-shadow:0 0 15px 4px yellow;
}}

</style>
</head>

<body>

<div id="northRoad" class="road"></div>
<div id="southRoad" class="road"></div>
<div id="westRoad"  class="road"></div>

<div id="northSig" class="signal">
    <div id="nR" class="light"></div>
    <div id="nY" class="light"></div>
    <div id="nG" class="light"></div>
</div>

<div id="southSig" class="signal">
    <div id="sR" class="light"></div>
    <div id="sY" class="light"></div>
    <div id="sG" class="light"></div>
</div>

<div id="westSig" class="signal">
    <div id="wR" class="light"></div>
    <div id="wY" class="light"></div>
    <div id="wG" class="light"></div>
</div>

<script>

let density = {{
    North:{north},
    South:{south},
    West:{west}
}};

let emergency = "{emergency}";
let order = ["North","South","West"];
let current = 0;

function clearAll() {{
    document.querySelectorAll(".light").forEach(l=>l.className="light");
}}

function setRedAll() {{
    clearAll();
    nR.classList.add("glow-red");
    sR.classList.add("glow-red");
    wR.classList.add("glow-red");
}}

function setLane(lane,color) {{
    if(lane=="North") nR.classList.remove("glow-red"),nY.classList.remove("glow-yellow"),nG.classList.remove("glow-green");
    if(lane=="South") sR.classList.remove("glow-red"),sY.classList.remove("glow-yellow"),sG.classList.remove("glow-green");
    if(lane=="West")  wR.classList.remove("glow-red"),wY.classList.remove("glow-yellow"),wG.classList.remove("glow-green");

    if(lane=="North") {{
        if(color=="green") nG.classList.add("glow-green");
        if(color=="yellow") nY.classList.add("glow-yellow");
        if(color=="red") nR.classList.add("glow-red");
    }}
    if(lane=="South") {{
        if(color=="green") sG.classList.add("glow-green");
        if(color=="yellow") sY.classList.add("glow-yellow");
        if(color=="red") sR.classList.add("glow-red");
    }}
    if(lane=="West") {{
        if(color=="green") wG.classList.add("glow-green");
        if(color=="yellow") wY.classList.add("glow-yellow");
        if(color=="red") wR.classList.add("glow-red");
    }}
}}

function chooseNext() {{
    if(emergency!="None") return emergency;
    return Object.keys(density).reduce((a,b)=>density[a]>density[b]?a:b);
}}

function cycle() {{
    let lane = chooseNext();

    setRedAll();

    setTimeout(()=>{{
        setRedAll();
        setLane(lane,"yellow");
    }},1000);

    setTimeout(()=>{{
        setRedAll();
        setLane(lane,"green");
    }},2000);
}}

cycle();
setInterval(cycle,5000);

</script>
</body>
</html>
"""

components.html(html, height=650)

st.markdown("---")
st.markdown(
"""
### 🚀 Project Description
AI-controlled adaptive traffic signal for 3-road intersections with:

- Coordinated signals
- Realistic Red → Yellow → Green phases
- Emergency vehicle override
- Density-based priority

### 👨‍💻 Made by Aman Kumar
"""
)