import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(layout="wide")

# ---------- LOAD IMAGES ----------
def load_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

car_img = load_base64("assets/car.png")
amb_img = load_base64("assets/ambulance.png")

# ---------- UI ----------
st.title("🚦 AI Priority Traffic Signal Simulation")
st.markdown("### Three-Road Intelligent Intersection (North–South–West)")

st.sidebar.header("Traffic Inputs")

north = st.sidebar.slider("North Lane Volume", 0, 20, 8)
south = st.sidebar.slider("South Lane Volume", 0, 20, 6)
west = st.sidebar.slider("West Lane Volume", 0, 20, 10)

priority = st.sidebar.selectbox(
    "Emergency Vehicle Lane",
    ["None", "North", "South", "West"]
)

# ---------- SIGNAL LOGIC ----------
lanes = {"North": north, "South": south, "West": west}
order = sorted(lanes, key=lanes.get, reverse=True)

if priority != "None":
    order.insert(0, order.pop(order.index(priority)))

green = order[0]

# ---------- HTML SIM ----------
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin:0;
    background:#0e1117;
}}

.road {{
    position:absolute;
    background:#2b2b2b;
}}

#north {{width:60px;height:200px;left:370px;top:0;}}
#south {{width:60px;height:200px;left:370px;bottom:0;}}
#west  {{height:60px;width:200px;left:0;top:270px;}}

.signal {{
    width:22px;height:22px;border-radius:50%;
    margin:4px;background:#333;
}}

.green {{background:#00ff6a;}}
.red {{background:#ff2e2e;}}

.sigbox {{
    position:absolute;
}}

#sn {{left:405px;top:210px;}}
#ss {{left:405px;bottom:210px;}}
#sw {{left:210px;top:285px;}}

.car {{
    position:absolute;
    width:40px;
}}

.ambulance {{
    position:absolute;
    width:45px;
}}

@keyframes moveN {{
    from {{top:-50px;}}
    to {{top:230px;}}
}}

@keyframes moveS {{
    from {{bottom:-50px;}}
    to {{bottom:230px;}}
}}

@keyframes moveW {{
    from {{left:-60px;}}
    to {{left:230px;}}
}}

</style>
</head>

<body>

<div id="north" class="road"></div>
<div id="south" class="road"></div>
<div id="west" class="road"></div>

<div id="sn" class="sigbox">
<div class="signal {"green" if green=="North" else "red"}"></div>
</div>

<div id="ss" class="sigbox">
<div class="signal {"green" if green=="South" else "red"}"></div>
</div>

<div id="sw" class="sigbox">
<div class="signal {"green" if green=="West" else "red"}"></div>
</div>

"""

# ---------- VEHICLES ----------
def cars(count, lane):
    html=""
    for i in range(count):
        top = -60 - i*50
        left = -60 - i*50
        
        if lane=="North":
            html+=f'<img src="data:image/png;base64,{amb_img if priority=="North" and i==0 else car_img}" class="{"ambulance" if priority=="North" and i==0 else "car"}" style="left:380px;top:{top}px;animation:moveN 4s linear infinite;">'
        if lane=="South":
            html+=f'<img src="data:image/png;base64,{amb_img if priority=="South" and i==0 else car_img}" class="{"ambulance" if priority=="South" and i==0 else "car"}" style="left:380px;bottom:{top}px;animation:moveS 4s linear infinite;">'
        if lane=="West":
            html+=f'<img src="data:image/png;base64,{amb_img if priority=="West" and i==0 else car_img}" class="{"ambulance" if priority=="West" and i==0 else "car"}" style="top:280px;left:{left}px;animation:moveW 4s linear infinite;">'
    return html

html += cars(north,"North")
html += cars(south,"South")
html += cars(west,"West")

html += "</body></html>"

components.html(html, height=520)

# ---------- PROJECT INFO ----------
st.markdown("---")
st.markdown("### 📄 Project Overview")
st.markdown("""
This research-grade simulation demonstrates an **AI-controlled adaptive traffic signal**
for a three-road intersection.  

The system dynamically allocates green signal priority based on:
- real-time traffic volume
- emergency vehicle detection
- lane-wise congestion ranking  

Emergency lanes automatically receive highest priority,
replicating intelligent urban traffic control systems.
""")

st.markdown("---")
st.markdown("**Made by Aman Kumar**")