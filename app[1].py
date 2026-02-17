import streamlit as st import numpy as np import matplotlib.pyplot as plt import matplotlib.animation as animation

st.set_page_config(layout="wide")

st.title("AI Traffic Signal Simulation — 3‑Way Intersection")

===================== USER INPUT =====================

col1, col2, col3 = st.columns(3)

with col1: north_vol = st.slider("North Traffic", 0, 20, 8) with col2: south_vol = st.slider("South Traffic", 0, 20, 6) with col3: west_vol = st.slider("West Traffic", 0, 20, 10)

priority_lane = st.selectbox( "Emergency Vehicle Lane", ["None", "North", "South", "West"] )

start_btn = st.button("Start Simulation")

===================== SIMULATION =====================

if start_btn: fig, ax = plt.subplots(figsize=(6, 6)) ax.set_xlim(0, 10) ax.set_ylim(0, 10) ax.axis("off")

# Draw roads
ax.add_patch(plt.Rectangle((4, 0), 2, 10, color="gray"))
ax.add_patch(plt.Rectangle((0, 4), 10, 2, color="gray"))

# Traffic lights positions
lights = {
    "North": (5.7, 7.5),
    "South": (4.1, 2.0),
    "West": (2.0, 4.3)
}

light_objs = {}
for lane, (x, y) in lights.items():
    light_objs[lane] = ax.add_patch(
        plt.Circle((x, y), 0.25, color="red")
    )

# Cars storage
cars = []

def create_cars(volume, lane):
    lane_cars = []
    for i in range(volume):
        if lane == "North":
            rect = plt.Rectangle((4.5, 10 + i), 0.4, 0.8, color="blue")
        elif lane == "South":
            rect = plt.Rectangle((5.1, -i), 0.4, 0.8, color="green")
        elif lane == "West":
            rect = plt.Rectangle((-i, 4.5), 0.8, 0.4, color="orange")
        ax.add_patch(rect)
        lane_cars.append(rect)
    return lane_cars

cars_n = create_cars(north_vol, "North")
cars_s = create_cars(south_vol, "South")
cars_w = create_cars(west_vol, "West")

phase = 0

def set_lights(active_lane):
    for lane in light_objs:
        if lane == active_lane:
            light_objs[lane].set_color("green")
        else:
            light_objs[lane].set_color("red")

def move_lane(cars, lane, green):
    for i, car in enumerate(cars):
        x, y = car.get_xy()

        if lane == "North":
            stop_y = 6.2 + i * 0.9
            if green or y > stop_y:
                car.set_xy((x, y - 0.15))

        elif lane == "South":
            stop_y = 3.0 - i * 0.9
            if green or y < stop_y:
                car.set_xy((x, y + 0.15))

        elif lane == "West":
            stop_x = 3.2 + i * 0.9
            if green or x > stop_x:
                car.set_xy((x + 0.15, y))

def update(frame):
    nonlocal phase

    # Emergency override
    if priority_lane != "None":
        active = priority_lane
    else:
        active = ["North", "South", "West"][phase // 40 % 3]

    set_lights(active)

    move_lane(cars_n, "North", active == "North")
    move_lane(cars_s, "South", active == "South")
    move_lane(cars_w, "West", active == "West")

    phase += 1
    return []

ani = animation.FuncAnimation(
    fig,
    update,
    frames=200,
    interval=50,
    blit=True
)

st.pyplot(fig)