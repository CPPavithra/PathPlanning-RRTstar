import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Configuration
serial_port = 'COM3'  # Replace with your Arduino's COM port
baud_rate = 9600
moving_avg_window = 10  # Number of points for moving average

# Initialize serial connection
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    time.sleep(2)  # Allow time for connection
except Exception as e:
    print(f"Error: Unable to open serial port - {e}")
    exit()

# Data lists
times = deque(maxlen=100)  # Store up to 100 points for time
co2_levels = deque(maxlen=100)  # Store up to 100 points for CO2 levels
smooth_co2_levels = deque(maxlen=100)

# Setup plot
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.set_title("Real-time CO2 Levels from MQ135 Sensor")
ax.set_xlabel("Time (s)")
ax.set_ylabel("CO2 Concentration (ppm)")
line, = ax.plot([], [], label="CO2 (ppm)", color='b')

# Moving average function
def moving_average(data, window_size):
    if len(data) < window_size:
        return sum(data) / len(data)  # Average if data length < window
    return sum(data[-window_size:]) / window_size

# Update function for live plotting
start_time = time.time()

def update(frame):
    try:
        # Read CO2 level from Arduino and convert to float
        raw_data = ser.readline().decode('utf-8').strip()
        if "Error" not in raw_data:
            co2_level = float(raw_data)
            current_time = time.time() - start_time

            # Append data to lists
            times.append(current_time)
            co2_levels.append(co2_level)
            smooth_co2_levels.append(moving_average(co2_levels, moving_avg_window))
            
            # Update plot data
            ax.clear()
            ax.plot(times, smooth_co2_levels, label="Smoothed CO2 (ppm)", color='b')
            ax.set_xlim(left=max(0, current_time - 50), right=current_time + 10)  # Dynamic x-axis
            ax.set_ylim(bottom=0, top=max(smooth_co2_levels) * 1.1 if smooth_co2_levels else 100)  # Dynamic y-axis
            ax.set_title("Real-time CO2 Levels from MQ135 Sensor")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("CO2 Concentration (ppm)")
            ax.legend(loc='upper left')
            
        else:
            print("Invalid data received")

    except Exception as e:
        print(f"Error reading data: {e}")

# Start live plot
ani = FuncAnimation(fig, update, interval=1000)  # Update every second
plt.show()

# Close serial port after plot is closed
ser.close()

