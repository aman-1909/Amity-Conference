import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("🚦 AI Traffic Signal Simulator (Realistic Visual)")

# ----------------------
# USER INPUT
# ----------------------

north_vol = st.sidebar.slider("North Traffic", 0, 20, 8)
south_vol = st.sidebar.slider("South Traffic", 0, 20, 6)
west_vol = st.sidebar.slider("West Traffic", 0, 20, 5)

emergency_lane = st.sidebar.selectbox(
    "Emergency Vehicle Lane",
    ["None", "North", "South", "West"]
)

# ----------------------
# AI SIGNAL TIMING
# ----------------------

base = 6
north_green = base + north_vol
south_green = base + south_vol
west_green = base + west_vol

if emergency_lane == "North":
    north_green += 8
if emergency_lane == "South":
    south_green += 8
if emergency_lane == "West":
    west_green += 8

# ----------------------
# HTML SIMULATION
# ----------------------

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin:0;
    background:#2b2b2b;
}}

.intersection {{
    position:relative;
    width:600px;
    height:600px;
    margin:auto;
    background:#3a3a3a;
}}

.road-v {{
    position:absolute;
    left:260px;
    width:80px;
    height:600px;
    background:#2a2a2a;
}}

.road-h {{
    position:absolute;
    top:260px;
    width:600px;
    height:80px;
    background:#2a2a2a;
}}

.signal {{
    position:absolute;
    width:22px;
    height:22px;
    border-radius:50%;
    background:red;
    box-shadow:0 0 10px #000;
}}

#sigN {{ top:200px; left:300px; }}
#sigS {{ top:360px; left:300px; }}
#sigW {{ top:300px; left:200px; }}

.car {{
    position:absolute;
    width:32px;
    height:60px;
    background-image:url('assets/car.png');
    background-size:contain;
    background-repeat:no-repeat;
}}

.ambulance {{
    background-image:url('assets/ambulance.png');
}}

</style>
</head>
<body>

<div class="intersection">

<div class="road-v"></div>
<div class="road-h"></div>

<div id="sigN" class="signal"></div>
<div id="sigS" class="signal"></div>
<div id="sigW" class="signal"></div>

</div>

<script>

let northVol={north_vol};
let southVol={south_vol};
let westVol={west_vol};

let northGreen={north_green};
let southGreen={south_green};
let westGreen={west_green};

let emergency="{emergency_lane}";

let container=document.querySelector(".intersection");

function spawnCars(lane,count){{

    for(let i=0;i<count;i++){{

        let car=document.createElement("div");
        car.className="car";

        if(lane===emergency && i===0){{
            car.classList.add("ambulance");
        }}

        if(lane==="North") {{
            car.style.left="295px";
            car.style.top=(20+i*70)+"px";
            car.style.transform="rotate(180deg)";
        }}

        if(lane==="South") {{
            car.style.left="315px";
            car.style.top=(520-i*70)+"px";
        }}

        if(lane==="West") {{
            car.style.top="295px";
            car.style.left=(20+i*70)+"px";
            car.style.transform="rotate(90deg)";
        }}

        container.appendChild(car);
    }}
}}

spawnCars("North",northVol);
spawnCars("South",southVol);
spawnCars("West",westVol);

function setSignal(n,s,w){{
    document.getElementById("sigN").style.background=n;
    document.getElementById("sigS").style.background=s;
    document.getElementById("sigW").style.background=w;
}}

async function cycle(){{

    while(true){{

        setSignal("lime","red","red");
        await sleep(northGreen*500);

        setSignal("red","lime","red");
        await sleep(southGreen*500);

        setSignal("red","red","lime");
        await sleep(westGreen*500);
    }}
}}

function sleep(ms){{ return new Promise(r=>setTimeout(r,ms)); }}

cycle();

</script>

</body>
</html>
"""

html(html_code, height=650)