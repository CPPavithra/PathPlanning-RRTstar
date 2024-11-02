import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Simulated CO2 range (in ppm)
min_co2 = 400  # Minimum CO2 concentration in ppm (e.g., outdoor air level)
max_co2 = 1000  # Maximum CO2 concentration in ppm (e.g., indoor peak level)

# Parameters for the plot
moving_avg_window = 10  # Window size for moving average
times = deque(maxlen=100)  # Store up to 100 time points
co2_levels = deque(maxlen=100)  # Store up to 100 CO2 level points
smooth_co2_levels = deque(maxlen=100)

# Setup plot
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.set_title("Simulated Real-time CO2 Levels")
ax.set_xlabel("Time (s)")
ax.set_ylabel("CO2 Concentration (ppm)")

# Moving average function
def moving_average(data, window_size):
    if len(data) < window_size:
        return sum(data) / len(data)  # Average if data length < window
    return sum(data[-window_size:]) / window_size

# Initialize start time for plotting time on x-axis
start_time = time.time()

# Update function for live plotting
def update(frame):
    # Generate a random CO2 level within the specified range
    co2_level = random.uniform(min_co2, max_co2)
    current_time = time.time() - start_time

    # Append simulated data to lists
    times.append(current_time)
    co2_levels.append(co2_level)
    smooth_co2_levels.append(moving_average(co2_levels, moving_avg_window))
    
    # Update plot data
    ax.clear()
    ax.plot(times, smooth_co2_levels, label="Smoothed CO2 (ppm)", color='b')
    ax.set_xlim(left=max(0, current_time - 50), right=current_time + 10)  # Dynamic x-axis
    ax.set_ylim(bottom=0, top=max(smooth_co2_levels) * 1.1 if smooth_co2_levels else 100)  # Dynamic y-axis
    ax.set_title("Simulated Real-time CO2 Levels")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CO2 Concentration (ppm)")
    ax.legend(loc='upper left')

# Start live plot animation
ani = FuncAnimation(fig, update, interval=1000)  # Update every second
plt.show()

