import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random
import time

plt.style.use('fivethirtyeight')

# Lists for simulated sensor data
time_data = []
mq135_data = []
ammonia_data = []
co2_data = []

# Track start time
start_time = time.time()

def update(frame):
    # Generate random sensor values
    mq135_value = random.randint(200, 800)  # Simulated MQ135 reading (e.g., between 200-800)
    ammonia_value = random.uniform(0, 10)   # Simulated Ammonia (NH₃) in ppm
    co2_value = random.uniform(400, 1000)   # Simulated CO₂ concentration in ppm

    # Track time elapsed since start
    elapsed_time = time.time() - start_time
    time_data.append(elapsed_time)
    mq135_data.append(mq135_value)
    ammonia_data.append(ammonia_value)
    co2_data.append(co2_value)

    # Limit data length to the last 100 readings
    if len(time_data) > 100:
        time_data.pop(0)
        mq135_data.pop(0)
        ammonia_data.pop(0)
        co2_data.pop(0)

    # Clear current plot
    plt.clf()

    # Plotting
    plt.subplot(3, 1, 1)
    plt.plot(time_data, mq135_data, label='MQ135 Value', color='blue')
    plt.title('Simulated MQ135 Sensor Readings Over Time')
    plt.ylabel('MQ135 Value')
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time_data, ammonia_data, label='Ammonia (NH₃) Concentration', color='green')
    plt.title('Simulated Ammonia Concentration Over Time')
    plt.ylabel('Concentration (ppm)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time_data, co2_data, label='CO₂ Concentration', color='red')
    plt.title('Simulated CO₂ Concentration Over Time')
    plt.ylabel('Concentration (ppm)')
    plt.grid()
    plt.legend()

    plt.xlabel('Time (seconds)')
    plt.tight_layout()

# Animation
ani = FuncAnimation(plt.gcf(), update, interval=1000)

plt.show()

