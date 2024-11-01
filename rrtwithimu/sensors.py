import time
import serial
from smbus2 import SMBus
from mpu6050 import mpu6050  # Library for MPU6050

class GPS:
    def __init__(self, port="/dev/ttyS0", baudrate=9600):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)

    def get_position(self):
        while True:
            line = self.serial_port.readline().decode("ascii", errors="replace")
            if line.startswith("$GPGGA"):
                data = line.split(",")
                latitude = self._parse_lat_lon(data[2], data[3])
                longitude = self._parse_lat_lon(data[4], data[5])
                return (latitude, longitude)

    def _parse_lat_lon(self, value, direction):
        if value and direction:
            degrees = float(value[:2])
            minutes = float(value[2:]) / 60
            result = degrees + minutes
            if direction in ["S", "W"]:
                result *= -1
            return result
        return None

class IMU:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

    def get_acceleration(self):
        accel_data = self.sensor.get_accel_data()
        return accel_data['x'], accel_data['y']

    def get_orientation(self):
        gyro_data = self.sensor.get_gyro_data()
        return gyro_data['x'], gyro_data['y'], gyro_data['z']

