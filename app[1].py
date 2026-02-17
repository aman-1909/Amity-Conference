import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🚦 AI Traffic Signal Simulator ")

# -----------------------------
# USER INPUT
# -----------------------------
st.sidebar.header("Traffic Control")

north_vol = st.sidebar.slider("North Lane Volume", 0, 15, 8)
south_vol = st.sidebar.slider("South Lane Volume", 0, 15, 6)
west_vol = st.sidebar.slider("West Lane Volume", 0, 15, 5)

priority = st.sidebar.selectbox(
    "Emergency Vehicle Lane",
    ["None", "North", "South", "West"]
)

# -----------------------------
# AI SIGNAL DECISION
# -----------------------------
def choose_green(n, s, w, p):
    if p != "None":
        return p
    vols = {"North": n, "South": s, "West": w}
    return max(vols, key=vols.get)

green = choose_green(north_vol, south_vol, west_vol, priority)

# -----------------------------
# HTML SIMULATION
# -----------------------------
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin:0;
    background:#1e1e1e;
    overflow:hidden;
}}

.intersection {{
    position:relative;
    width:800px;
    height:600px;
    margin:auto;
    background:#2b2b2b;
}}

.roadV {{
    position:absolute;
    width:140px;
    height:600px;
    left:330px;
    background:#444;
}}

.roadH {{
    position:absolute;
    width:800px;
    height:140px;
    top:230px;
    background:#444;
}}

.light {{
    position:absolute;
    width:24px;
    height:70px;
    background:#000;
    border-radius:6px;
    padding:3px;
}}

.bulb {{
    width:18px;
    height:18px;
    border-radius:50%;
    margin:3px auto;
    background:#111;
}}

.red.on {{ background:red; }}
.yellow.on {{ background:yellow; }}
.green.on {{ background:lime; }}

.car {{
    position:absolute;
    width:18px;
    height:28px;
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

<div class="roadV"></div>
<div class="roadH"></div>

<!-- NORTH LIGHT -->
<div class="light" style="top:40px; left:388px;">
<div class="bulb red {"on" if green!="North" else ""}"></div>
<div class="bulb yellow"></div>
<div class="bulb green {"on" if green=="North" else ""}"></div>
</div>

<!-- SOUTH LIGHT -->
<div class="light" style="bottom:40px; left:408px;">
<div class="bulb red {"on" if green!="South" else ""}"></div>
<div class="bulb yellow"></div>
<div class="bulb green {"on" if green=="South" else ""}"></div>
</div>

<!-- WEST LIGHT -->
<div class="light" style="top:260px; left:40px;">
<div class="bulb red {"on" if green!="West" else ""}"></div>
<div class="bulb yellow"></div>
<div class="bulb green {"on" if green=="West" else ""}"></div>
</div>

</div>

<script>

const northVol = {north_vol};
const southVol = {south_vol};
const westVol = {west_vol};
const green = "{green}";
const priority = "{priority}";

function spawnCars() {{

    const inter = document.querySelector(".intersection");

    function laneCars(lane, count) {{

        for (let i=0;i<count;i++) {{

            let car = document.createElement("div");
            car.className = "car";

            if(priority===lane && i===0)
                car.classList.add("emergency");

            if(lane==="North") {{
                car.style.left="390px";
                car.style.top=(80 + i*35)+"px";

                if(green==="North")
                    move(car,0,1);
            }}

            if(lane==="South") {{
                car.style.left="410px";
                car.style.top=(520 - i*35)+"px";

                if(green==="South")
                    move(car,0,-1);
            }}

            if(lane==="West") {{
                car.style.top="250px";
                car.style.left=(80 + i*35)+"px";

                if(green==="West")
                    move(car,1,0);
            }}

            inter.appendChild(car);
        }}
    }}

    function move(car,dx,dy) {{
        let x=parseInt(car.style.left);
        let y=parseInt(car.style.top);

        function step() {{
            x+=dx*1.2;
            y+=dy*1.2;
            car.style.left=x+"px";
            car.style.top=y+"px";
            requestAnimationFrame(step);
        }}
        step();
    }}

    laneCars("North", northVol);
    laneCars("South", southVol);
    laneCars("West", westVol);
}}

spawnCars();

</script>

</body>
</html>
"""

components.html(html, height=620)
