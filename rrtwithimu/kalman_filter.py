import numpy as np

class KalmanFilter:
    def __init__(self):
        self.state = np.zeros(4)  # [x, y, vx, vy]
        self.covariance = np.eye(4)
        self.process_noise = np.eye(4) * 0.1
        self.measurement_noise = np.eye(2) * 0.1
        self.measurement_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])

    def predict(self, dt, imu_acc):
        transition_matrix = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
        ax, ay = imu_acc
        control_input = np.array([0.5 * ax * dt**2, 0.5 * ay * dt**2, ax * dt, ay * dt])
        self.state = np.dot(transition_matrix, self.state) + control_input
        self.covariance = np.dot(np.dot(transition_matrix, self.covariance), transition_matrix.T) + self.process_noise

    def update(self, gps_position, imu_acc, imu_orientation):
        dt = 0.1
        self.predict(dt, imu_acc)
        gps_measurement = np.array(gps_position)
        y = gps_measurement - np.dot(self.measurement_matrix, self.state)
        s = np.dot(self.measurement_matrix, np.dot(self.covariance, self.measurement_matrix.T)) + self.measurement_noise
        kalman_gain = np.dot(np.dot(self.covariance, self.measurement_matrix.T), np.linalg.inv(s))
        self.state = self.state + np.dot(kalman_gain, y)
        self.covariance = np.dot((np.eye(4) - np.dot(kalman_gain, self.measurement_matrix)), self.covariance)
        return self.state[:2]

