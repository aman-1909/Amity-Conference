import streamlit as st 
import time

st.set_page_config(page_title="Realistic Traffic Light", layout="centered")

st.title("🚦 Realistic AI Traffic Signal") st.markdown("Ultra‑realistic synchronized traffic light simulation")

User controls

green_time = st.slider("Green Duration (seconds)", 3, 15, 8) yellow_time = st.slider("Yellow Duration (seconds)", 1, 5, 2)

CSS for realistic traffic lights

light_css = """

<style>
.road {
    display:flex;
    justify-content:center;
    gap:120px;
    margin-top:40px;
}
.signal {
    width:80px;
    background:#111;
    border-radius:20px;
    padding:10px;
    box-shadow:0 0 20px rgba(0,0,0,0.6) inset, 0 0 10px #000;
}
.light {
    width:50px;
    height:50px;
    border-radius:50%;
    margin:10px auto;
    background:#222;
}
.red.on { background:red; box-shadow:0 0 20px red; }
.yellow.on { background:yellow; box-shadow:0 0 20px yellow; }
.green.on { background:lime; box-shadow:0 0 20px lime; }
.label { text-align:center; color:white; margin-top:5px; }
body { background:#0e1117; }
</style>"""

st.markdown(light_css, unsafe_allow_html=True)

placeholder = st.empty()

def render(a_red, a_yellow, a_green, b_red, b_yellow, b_green): html = f""" <div class="road"> <div> <div class="signal"> <div class="light red {'on' if a_red else ''}"></div> <div class="light yellow {'on' if a_yellow else ''}"></div> <div class="light green {'on' if a_green else ''}"></div> </div> <div class="label">Road A</div> </div> <div> <div class="signal"> <div class="light red {'on' if b_red else ''}"></div> <div class="light yellow {'on' if b_yellow else ''}"></div> <div class="light green {'on' if b_green else ''}"></div> </div> <div class="label">Road B</div> </div> </div> """ placeholder.markdown(html, unsafe_allow_html=True)

run = st.button("Start Simulation")

if run: while True: # A green render(0,0,1, 1,0,0) time.sleep(green_time)

# A yellow
    render(0,1,0, 1,0,0)
    time.sleep(yellow_time)

    # B green
    render(1,0,0, 0,0,1)
    time.sleep(green_time)

    # B yellow
    render(1,0,0, 0,1,0)
    time.sleep(yellow_time)
