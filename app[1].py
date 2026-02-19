import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚦 AI Priority Traffic Signal Simulation")
st.subheader("Three-Road Intelligent Intersection (North–South–West)")

# ===================== CONTROLS =====================
st.sidebar.header("Traffic Settings")

north = st.sidebar.slider("North Traffic", 0, 10, 5)
south = st.sidebar.slider("South Traffic", 0, 10, 5)
west = st.sidebar.slider("West Traffic", 0, 10, 5)

emergency_lane = st.sidebar.selectbox(
    "Emergency Vehicle Lane",
    ["None", "North", "South", "West"]
)

# ===================== HTML SIMULATION =====================
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin:0;
    background:#0f172a;
    overflow:hidden;
}}

.road {{
    position:absolute;
    background:#374151;
}}

#northRoad {{ width:80px; height:240px; left:50%; transform:translateX(-50%); top:0; }}
#southRoad {{ width:80px; height:240px; left:50%; transform:translateX(-50%); bottom:0; }}
#westRoad  {{ height:80px; width:260px; left:0; top:50%; transform:translateY(-50%); }}

.light {{
    position:absolute;
    width:18px;
    height:18px;
    border-radius:50%;
    background:red;
    box-shadow:0 0 10px red;
}}

#northLight {{ top:250px; left:50%; transform:translateX(-50%); }}
#southLight {{ bottom:250px; left:50%; transform:translateX(-50%); }}
#westLight  {{ left:270px; top:50%; transform:translateY(-50%); }}

.vehicle {{
    position:absolute;
    width:34px;
    height:18px;
    transition:all 0.1s linear;
}}

</style>
</head>

<body>

<div id="northRoad" class="road"></div>
<div id="southRoad" class="road"></div>
<div id="westRoad"  class="road"></div>

<div id="northLight" class="light"></div>
<div id="southLight" class="light"></div>
<div id="westLight"  class="light"></div>

<script>

let northCount = {north};
let southCount = {south};
let westCount  = {west};

let emergency = "{emergency_lane}";

let green = "North";

function chooseGreen() {{
    if (emergency !== "None") {{
        green = emergency;
        return;
    }}

    let volumes = {{
        "North": northCount,
        "South": southCount,
        "West": westCount
    }};

    green = Object.keys(volumes).reduce((a,b)=>volumes[a]>volumes[b]?a:b);
}}

function updateLights() {{
    document.getElementById("northLight").style.background = green=="North"?"lime":"red";
    document.getElementById("southLight").style.background = green=="South"?"lime":"red";
    document.getElementById("westLight").style.background  = green=="West" ?"lime":"red";
}}

function spawnVehicles() {{

    for(let i=0;i<northCount;i++) {{
        let v = document.createElement("img");
        v.src = "assets/{"ambulance.png" if emergency_lane=="North" else "car.png"}";
        v.className="vehicle";
        v.style.left="calc(50% - 17px)";
        v.style.top = (i*40+10)+"px";
        document.body.appendChild(v);
        v.dataset.lane="North";
    }}

    for(let i=0;i<southCount;i++) {{
        let v = document.createElement("img");
        v.src = "assets/{"ambulance.png" if emergency_lane=="South" else "car.png"}";
        v.className="vehicle";
        v.style.left="calc(50% - 17px)";
        v.style.bottom = (i*40+10)+"px";
        document.body.appendChild(v);
        v.dataset.lane="South";
    }}

    for(let i=0;i<westCount;i++) {{
        let v = document.createElement("img");
        v.src = "assets/{"ambulance.png" if emergency_lane=="West" else "car.png"}";
        v.className="vehicle";
        v.style.top="calc(50% - 9px)";
        v.style.left = (i*40+10)+"px";
        document.body.appendChild(v);
        v.dataset.lane="West";
    }}
}}

function moveVehicles() {{
    document.querySelectorAll(".vehicle").forEach(v=>{{
        if(v.dataset.lane!==green) return;  // STOP at red

        if(v.dataset.lane=="North") {{
            let y = parseInt(v.style.top);
            if(y<260) v.style.top = (y+2)+"px";
        }}

        if(v.dataset.lane=="South") {{
            let y = parseInt(v.style.bottom);
            if(y<260) v.style.bottom = (y+2)+"px";
        }}

        if(v.dataset.lane=="West") {{
            let x = parseInt(v.style.left);
            if(x<260) v.style.left = (x+2)+"px";
        }}
    }});
}}

chooseGreen();
updateLights();
spawnVehicles();

setInterval(()=>{{
    chooseGreen();
    updateLights();
}},3000);

setInterval(moveVehicles,40);

</script>

</body>
</html>
"""

components.html(html, height=600)

# ===================== INFO =====================
st.markdown("---")
st.markdown(
"""
### 🚀 Project Description
AI-based adaptive traffic signal for three-road intersections with:
- Dynamic green selection by traffic volume
- Emergency vehicle priority override
- Realistic queue behavior
- Signal-aware vehicle motion

### 👨‍💻 Made by Aman Kumar
"""
)