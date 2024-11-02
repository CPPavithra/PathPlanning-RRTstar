import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# Initialize serial connection
try:
    ser = serial.Serial('my_port', 115200)
except serial.SerialException:
    print("Failed to connect to the serial port. Check the connection and port name.")
    exit()

plt.style.use('fivethirtyeight')

# Lists for sensor data
time_data = []
mq135_data = []
ammonia_data = []
co2_data = []

start_time = time.time()

def update(frame):
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        values = line.split(',')
        
        try:
            # Append new data
            mq135_value = int(values[0])
            ammonia_value = float(values[1])
            co2_value = float(values[2])

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
            plt.title('MQ135 Sensor Readings Over Time')
            plt.ylabel('MQ135 Value')
            plt.grid()
            plt.legend()

            plt.subplot(3, 1, 2)
            plt.plot(time_data, ammonia_data, label='Ammonia (NH₃) Concentration', color='green')
            plt.title('Ammonia Concentration Over Time')
            plt.ylabel('Concentration (ppm)')
            plt.grid()
            plt.legend()

            plt.subplot(3, 1, 3)
            plt.plot(time_data, co2_data, label='CO₂ Concentration', color='red')
            plt.title('CO₂ Concentration Over Time')
            plt.ylabel('Concentration (ppm)')
            plt.grid()
            plt.legend()

            plt.xlabel('Time (seconds)')
            plt.tight_layout()

        except (ValueError, IndexError):
            # Handle errors in data format
            print("Error parsing sensor data. Please check the serial output format.")
    
# Animation
ani = FuncAnimation(plt.gcf(), update, interval=1000)

plt.show()

