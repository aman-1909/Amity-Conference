import streamlit as st import streamlit.components.v1 as components

st.set_page_config(page_title="AI Traffic Research Simulator", layout="wide")

st.title("🚦 Research‑Grade AI Traffic Signal Simulator")

---------------- Sidebar Controls ----------------

st.sidebar.header("Traffic Volume per Lane") north_vol = st.sidebar.slider("North Lane Volume", 0, 30, 10) south_vol = st.sidebar.slider("South Lane Volume", 0, 30, 10) west_vol = st.sidebar.slider("West Lane Volume", 0, 30, 10)

emergency_lane = st.sidebar.selectbox( "Emergency Vehicle Lane", ["None", "North", "South", "West"] )

---------------- AI Timing Logic ----------------

def compute_times(n, s, w, emergency): base = 3 scale = 0.4 times = { "North": base + n * scale, "South": base + s * scale, "West": base + w * scale } if emergency != "None": times[emergency] += 3 return times

times = compute_times(north_vol, south_vol, west_vol, emergency_lane)

---------------- HTML Simulation ----------------

html = f"""

<!DOCTYPE html><html>
<head>
<style>
body {{ margin:0; background:#111; overflow:hidden; }}
canvas {{ background:#1a1a1a; display:block; margin:auto; border-radius:10px; }}
</style>
</head>
<body>
<canvas id="sim" width="600" height="600"></canvas>
<script>
const canvas = document.getElementById("sim");
const ctx = canvas.getContext("2d");let greenLane = "North"; let timer = 0;

const times = {{ North: {times['North']*60}, South: {times['South']*60}, West: {times['West']*60} }};

function createCars(count, lane) {{ let arr = []; for(let i=0;i<count;i++){{ if(lane=="North") arr.push({{x:290,y:50+i25}}); if(lane=="South") arr.push({{x:310,y:550-i25}}); if(lane=="West") arr.push({{x:50+i*25,y:290}}); }} return arr; }}

let carsNorth = createCars({north_vol},"North"); let carsSouth = createCars({south_vol},"South"); let carsWest = createCars({west_vol},"West");

function drawRoads(){{ ctx.fillStyle="#444"; ctx.fillRect(280,0,40,600); ctx.fillRect(0,280,320,40); }}

function drawLights(){{ function light(x,y,active){{ ctx.beginPath(); ctx.arc(x,y,10,0,Math.PI*2); ctx.fillStyle = active?"#0f0":"#400"; ctx.fill(); }} light(300,120,greenLane=="North"); light(300,480,greenLane=="South"); light(120,300,greenLane=="West"); }}

function moveCars(){{ if(greenLane=="North"){{ carsNorth.forEach(c=>{{ if(c.y<260) c.y+=1.2; }}); }} if(greenLane=="South"){{ carsSouth.forEach(c=>{{ if(c.y>340) c.y-=1.2; }}); }} if(greenLane=="West"){{ carsWest.forEach(c=>{{ if(c.x<260) c.x+=1.2; }}); }} }}

function drawCars(){{ ctx.fillStyle="#4fc3f7"; carsNorth.forEach(c=>ctx.fillRect(c.x,c.y,12,22)); carsSouth.forEach(c=>ctx.fillRect(c.x,c.y,12,22)); carsWest.forEach(c=>ctx.fillRect(c.x,c.y,22,12)); }}

function updateSignal(){{ timer++; if(timer>times[greenLane]){{ timer=0; if(greenLane=="North") greenLane="South"; else if(greenLane=="South") greenLane="West"; else greenLane="North"; }} }}

function loop(){{ ctx.clearRect(0,0,600,600); drawRoads(); drawLights(); moveCars(); drawCars(); updateSignal(); requestAnimationFrame(loop); }} loop(); </script>

</body>
</html>
"""components.html(html, height=620)