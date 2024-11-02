import plotly.graph_objs as go
from plotly.subplots import make_subplots
import random
import time
from collections import deque

# Simulated CO₂ range (in ppm)
min_co2 = 400  # Minimum CO₂ concentration in ppm
max_co2 = 1000  # Maximum CO₂ concentration in ppm

# Parameters for the plot
moving_avg_window = 10  # Window size for moving average
times = deque(maxlen=100)  # Store up to 100 time points
co2_levels = deque(maxlen=100)  # Store up to 100 CO₂ level points
smooth_co2_levels = deque(maxlen=100)

# Initialize start time
start_time = time.time()

# Moving average function
def moving_average(data, window_size):
    if len(data) < window_size:
        return sum(data) / len(data)
    return sum(data[-window_size:]) / window_size

# Simulate data points for initial plot
for i in range(100):
    current_time = time.time() - start_time
    co2_level = random.uniform(min_co2, max_co2)
    
    times.append(current_time)
    co2_levels.append(co2_level)
    smooth_co2_levels.append(moving_average(co2_levels, moving_avg_window))
    time.sleep(0.1)

# Create initial plot
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=list(times), y=list(smooth_co2_levels), mode='lines', name='Smoothed CO2 Level (ppm)'))

# Update layout
fig.update_layout(
    title="Simulated Real-time CO2 Levels",
    xaxis_title="Time (s)",
    yaxis_title="CO2 Concentration (ppm)",
    template="plotly_dark"
)

# Display the plot
fig.show()

