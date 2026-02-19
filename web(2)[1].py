import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("AI Priority Traffic Signal Simulation")
st.caption("Three-Road Intelligent Intersection (North–South–West)")

# ---------- Controls ----------
col1, col2, col3 = st.columns(3)
north = col1.slider("North Traffic", 0, 100, 50)
south = col2.slider("South Traffic", 0, 100, 40)
west  = col3.slider("West Traffic",  0, 100, 30)

emergency = st.selectbox(
    "Emergency Vehicle Priority",
    ["None", "North", "South", "West"]
)

# ---------- HTML Simulation ----------
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

body {{
    margin:0;
    background:#0b1220;
    display:flex;
    justify-content:center;
}}

.intersection {{
    position:relative;
    width:900px;
    height:700px;
}}

.road {{
    position:absolute;
    background:#2b2b2b;
}}

.roadV {{
    width:200px;
    height:100%;
    left:50%;
    transform:translateX(-50%);
}}

.roadH {{
    height:200px;
    width:50%;
    top:50%;
    left:0;
    transform:translateY(-50%);
}}

.laneMark {{
    position:absolute;
    width:6px;
    background:#facc15;
}}

.vLane1 {{ left:calc(50% - 50px); height:100%; }}
.vLane2 {{ left:calc(50% + 44px); height:100%; }}

.hLane {{ top:50%; height:6px; width:50%; transform:translateY(-50%); }}

.stopLine {{
    position:absolute;
    background:white;
}}

.nStop {{ width:200px; height:6px; top:260px; left:50%; transform:translateX(-50%); }}
.sStop {{ width:200px; height:6px; bottom:260px; left:50%; transform:translateX(-50%); }}
.wStop {{ height:200px; width:6px; left:260px; top:50%; transform:translateY(-50%); }}

.zebra div {{
    position:absolute;
    background:white;
}}

.nZebra div {{ width:200px; height:6px; left:50%; transform:translateX(-50%); }}
.sZebra div {{ width:200px; height:6px; left:50%; transform:translateX(-50%); }}
.wZebra div {{ height:200px; width:6px; top:50%; transform:translateY(-50%); }}

.centerIsland {{
    position:absolute;
    width:200px;
    height:200px;
    background:#3a3a3a;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    border-radius:12px;
}}

.signalPole {{
    position:absolute;
    width:10px;
    height:80px;
    background:#444;
}}

.signalBox {{
    position:absolute;
    width:46px;
    height:140px;
    background:#111;
    border-radius:10px;
    padding:8px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    align-items:center;
    box-shadow:0 0 12px #000;
}}

.light {{
    width:26px;
    height:26px;
    border-radius:50%;
    background:#1f2937;
}}

.red    {{ background:#ef4444; box-shadow:0 0 18px #ef4444; }}
.yellow {{ background:#facc15; box-shadow:0 0 18px #facc15; }}
.green  {{ background:#22c55e; box-shadow:0 0 18px #22c55e; }}

/* Positions */
#northPole {{ top:200px; left:50%; transform:translateX(-50%); }}
#southPole {{ bottom:200px; left:50%; transform:translateX(-50%); }}
#westPole  {{ left:200px; top:50%; transform:translateY(-50%); }}

#northSig {{ top:120px; left:50%; transform:translateX(-50%); }}
#southSig {{ bottom:120px; left:50%; transform:translateX(-50%); }}
#westSig  {{ left:120px; top:50%; transform:translateY(-50%) rotate(90deg); }}

.footer {{
    position:absolute;
    bottom:-40px;
    width:100%;
    text-align:center;
    color:#9ca3af;
    font-size:14px;
}}

</style>
</head>

<body>

<div class="intersection">

<div class="road roadV"></div>
<div class="road roadH"></div>

<div class="laneMark vLane1"></div>
<div class="laneMark vLane2"></div>
<div class="laneMark hLane"></div>

<div class="stopLine nStop"></div>
<div class="stopLine sStop"></div>
<div class="stopLine wStop"></div>

<div class="centerIsland"></div>

<div id="northPole" class="signalPole"></div>
<div id="southPole" class="signalPole"></div>
<div id="westPole"  class="signalPole"></div>

<div id="northSig" class="signalBox">
<div id="nR" class="light"></div>
<div id="nY" class="light"></div>
<div id="nG" class="light"></div>
</div>

<div id="southSig" class="signalBox">
<div id="sR" class="light"></div>
<div id="sY" class="light"></div>
<div id="sG" class="light"></div>
</div>

<div id="westSig" class="signalBox">
<div id="wR" class="light"></div>
<div id="wY" class="light"></div>
<div id="wG" class="light"></div>
</div>

<div class="footer">Made by Aman Kumar</div>

</div>

<script>

let density = {{
North:{north},
South:{south},
West:{west}
}};

let emergency = "{emergency}";

function clearAll() {{
document.querySelectorAll(".light").forEach(l=>l.className="light");
}}

function redAll() {{
clearAll();
nR.classList.add("red");
sR.classList.add("red");
wR.classList.add("red");
}}

function laneYellow(l) {{
if(l=="North") nY.classList.add("yellow");
if(l=="South") sY.classList.add("yellow");
if(l=="West")  wY.classList.add("yellow");
}}

function laneGreen(l) {{
if(l=="North") nG.classList.add("green");
if(l=="South") sG.classList.add("green");
if(l=="West")  wG.classList.add("green");
}}

function chooseLane() {{
if(emergency!="None") return emergency;
return Object.keys(density).reduce((a,b)=>density[a]>density[b]?a:b);
}}

function cycle() {{
let lane = chooseLane();

redAll();
setTimeout(()=>{{ redAll(); laneYellow(lane); }},1200);
setTimeout(()=>{{ redAll(); laneGreen(lane); }},2400);
}}

cycle();
setInterval(cycle,5000);

</script>

</body>
</html>
"""

components.html(html, height=760, width=900)