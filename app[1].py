import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚦 AI Traffic Signal Simulator (3-Road Intersection)")

# -----------------------------
# USER CONTROLS
# -----------------------------
st.sidebar.header("Traffic Settings")

north_vol = st.sidebar.slider("North Traffic", 0, 20, 10)
south_vol = st.sidebar.slider("South Traffic", 0, 20, 8)
west_vol = st.sidebar.slider("West Traffic", 0, 20, 6)

priority_lane = st.sidebar.selectbox(
    "Emergency Vehicle Lane",
    ["None", "North", "South", "West"]
)

# -----------------------------
# SIMPLE AI SIGNAL LOGIC
# -----------------------------
def choose_green(n, s, w, priority):
    if priority != "None":
        return priority
    volumes = {"North": n, "South": s, "West": w}
    return max(volumes, key=volumes.get)

green_lane = choose_green(north_vol, south_vol, west_vol, priority_lane)

# -----------------------------
# HTML ANIMATION
# -----------------------------
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin:0;
    background:#222;
}}

.intersection {{
    position:relative;
    width:800px;
    height:600px;
    margin:auto;
    background:#333;
}}

.road {{
    position:absolute;
    background:#555;
}}

.vertical {{
    width:120px;
    height:600px;
    left:340px;
}}

.horizontal {{
    width:800px;
    height:120px;
    top:240px;
}}

.light {{
    position:absolute;
    width:20px;
    height:60px;
    background:black;
    border-radius:5px;
    padding:3px;
}}

.bulb {{
    width:14px;
    height:14px;
    border-radius:50%;
    margin:2px auto;
    background:#111;
}}

.red.on {{ background:red; }}
.yellow.on {{ background:yellow; }}
.green.on {{ background:lime; }}

.car {{
    position:absolute;
    width:18px;
    height:30px;
    background:cyan;
    border-radius:3px;
}}

.emergency {{
    background:red;
}}
</style>
</head>

<body>

<div class="intersection">

    <!-- ROADS -->
    <div class="road vertical"></div>
    <div class="road horizontal"></div>

    <!-- NORTH LIGHT -->
    <div class="light" style="top:40px; left:380px;">
        <div class="bulb red {'on' if green_lane!='North' else ''}"></div>
        <div class="bulb yellow"></div>
        <div class="bulb green {'on' if green_lane=='North' else ''}"></div>
    </div>

    <!-- SOUTH LIGHT -->
    <div class="light" style="bottom:40px; left:400px;">
        <div class="bulb red {'on' if green_lane!='South' else ''}"></div>
        <div class="bulb yellow"></div>
        <div class="bulb green {'on' if green_lane=='South' else ''}"></div>
    </div>

    <!-- WEST LIGHT -->
    <div class="light" style="top:260px; left:40px;">
        <div class="bulb red {'on' if green_lane!='West' else ''}"></div>
        <div class="bulb yellow"></div>
        <div class="bulb green {'on' if green_lane=='West' else ''}"></div>
    </div>

    <!-- CARS -->
    <script>
    const northVol = {north_vol};
    const southVol = {south_vol};
    const westVol = {west_vol};
    const green = "{green_lane}";
    const priority = "{priority_lane}";

    function createCars(lane, count) {{
        for (let i=0;i<count;i++) {{
            let car = document.createElement("div");
            car.className = "car";
            
            if(priority === lane && i===0)
                car.classList.add("emergency");

            if(lane==="North") noticing volume and green light. Make it smooth and understandable.