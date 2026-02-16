import streamlit as st
import pygame
import random
import time

# =============================
# STREAMLIT UI
# =============================
st.set_page_config(layout="wide")
st.title("AI Controlled T-Intersection Traffic Simulation")

north_vol = st.slider("North Traffic Volume", 0, 20, 8)
south_vol = st.slider("South Traffic Volume", 0, 20, 6)
west_vol = st.slider("West Traffic Volume", 0, 20, 10)

emergency_lane = st.selectbox(
    "Emergency Vehicle Lane",
    ["None", "North", "South", "West"]
)

run = st.button("Start Simulation")

# =============================
# PYGAME SIMULATION
# =============================
if run:

    pygame.init()
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("T-Intersection AI Traffic")

    # Colors
    ROAD = (50, 50, 50)
    BG = (200, 220, 230)
    RED = (220, 30, 30)
    GREEN = (30, 200, 30)
    YELLOW = (250, 210, 50)
    CAR = (40, 120, 240)
    EMERGENCY = (240, 240, 40)
    WHITE = (255, 255, 255)

    clock = pygame.time.Clock()

    # =============================
    # SIGNAL CLASS
    # =============================
    class Signal:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.state = "RED"

        def draw(self):
            pygame.draw.rect(screen, (30,30,30), (self.x-10, self.y-30, 20, 60))
            color = RED if self.state=="RED" else GREEN
            pygame.draw.circle(screen, color, (self.x, self.y), 8)

    # =============================
    # CAR CLASS
    # =============================
    class Car:
        def __init__(self, lane, emergency=False):
            self.lane = lane
            self.emergency = emergency
            self.speed = 2.5 if not emergency else 3.5

            if lane == "North":
                self.x = WIDTH//2 - 10
                self.y = -random.randint(40,200)
                self.dx, self.dy = 0, 1

            elif lane == "South":
                self.x = WIDTH//2 + 10
                self.y = HEIGHT + random.randint(40,200)
                self.dx, self.dy = 0, -1

            elif lane == "West":
                self.x = -random.randint(40,200)
                self.y = HEIGHT//2 + 10
                self.dx, self.dy = 1, 0

        def stop_line(self):
            if self.lane == "North":
                return HEIGHT//2 - 60
            if self.lane == "South":
                return HEIGHT//2 + 60
            if self.lane == "West":
                return WIDTH//2 - 60

        def update(self, signal_state):
            stop = self.stop_line()

            if signal_state == "RED":
                if self.lane == "North" and self.y+self.speed < stop:
                    self.y += self.dy*self.speed
                elif self.lane == "South" and self.y-self.speed > stop:
                    self.y += self.dy*self.speed
                elif self.lane == "West" and self.x+self.speed < stop:
                    self.x += self.dx*self.speed
            else:
                self.x += self.dx*self.speed
                self.y += self.dy*self.speed

        def draw(self):
            color = EMERGENCY if self.emergency else CAR
            pygame.draw.rect(screen, color, (self.x, self.y, 18, 10))

    # =============================
    # CREATE SIGNALS
    # =============================
    signals = {
        "North": Signal(WIDTH//2 - 30, HEIGHT//2 - 80),
        "South": Signal(WIDTH//2 + 30, HEIGHT//2 + 80),
        "West": Signal(WIDTH//2 - 80, HEIGHT//2 + 30),
    }

    cars = []

    # Spawn initial cars
    for _ in range(north_vol):
        cars.append(Car("North"))
    for _ in range(south_vol):
        cars.append(Car("South"))
    for _ in range(west_vol):
        cars.append(Car("West"))

    if emergency_lane != "None":
        cars.append(Car(emergency_lane, emergency=True))

    # =============================
    # AI SIGNAL CONTROL
    # =============================
    def choose_green():
        if emergency_lane != "None":
            return emergency_lane

        counts = {
            "North": sum(1 for c in cars if c.lane=="North"),
            "South": sum(1 for c in cars if c.lane=="South"),
            "West": sum(1 for c in cars if c.lane=="West"),
        }
        return max(counts, key=counts.get)

    # =============================
    # DRAW ROADS
    # =============================
    def draw_roads():
        pygame.draw.rect(screen, ROAD, (WIDTH//2-40, 0, 80, HEIGHT))
        pygame.draw.rect(screen, ROAD, (0, HEIGHT//2-40, WIDTH//2, 80))

    # =============================
    # MAIN LOOP
    # =============================
    running = True
    current_green = choose_green()

    while running:
        screen.fill(BG)
        draw_roads()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update signals
        for k in signals:
            signals[k].state = "GREEN" if k == current_green else "RED"
            signals[k].draw()

        # Update cars
        for car in cars:
            car.update(signals[car.lane].state)
            car.draw()

        pygame.display.flip()
        clock.tick(60)

        # If emergency cleared → resume AI
        if emergency_lane != "None":
            if not any(c.emergency and 0<c.x<WIDTH and 0<c.y<HEIGHT for c in cars):
                emergency_lane = "None"
                current_green = choose_green()

    pygame.quit()