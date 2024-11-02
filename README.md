# PathPlanning-RRTstar

# Autonomous Soil Sampling Rover

##THIS REPO CONTAINS
- Path Planning Code
- Arduino code for autonomous motor control
- Code to print out the coordinates
- Code to visualise the path on the occupancy grid
- Converting Point Cloud Output to occuoancy grid
- Code for remote piloting in case of emergencies
- Sample test codes that I have made which HAVE NOT been included finally/ have been MODIFIED and included.
- A folder to help navigate through the repo and also for sample output and visualisation

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [SLAM Dataset](#slam-data-set)
- [Code Explanation](#code-explanation)
- [Repo Guidance](#repo-guidance)
- [Future Improvements](#future-improvements)
- [Sample Output Images](#sample-output)

---

## Overview

This project involves building an autonomous rover capable of navigating through the terrain (Site of Detection- Black Canyon, Utah). This rover will navigate through using SLAM (V-I SLAM) and decide the most feasible path using Path Planning algorithm (RRT* Algorithm). Once the coordinates are decided, it will then send the coordinates to the arduino to which the motor drivers are connected. Using IMU calibration and direction and distance calculation, the rover will move to the desired coordinates. At the goal, it will then collect the soil sample and bring it back to the base station accordingly.


## Features

- **Autonomous Navigation**: The rover automatically moves to specified coordinates.
- **Path Planning**: RRT* algorithm has been used.
- **Direction Calibration**: The MPU6050 IMU along with basic mathematical calculation provides orientation data to keep the rover aligned with its destination.
- **Soil Collection**: Enables the rover to collect soil samples.
- **Obstacle Avoidance**: Designed for basic obstacle detection and path recalibration.
- **Visual Output**: This repo also has sample visual output.

## SLAM Data set

- Since the input for path planning occupancy grid is based on the output for V-I SLAM, I have taken an open-source dataset to calibirate the sample code.
- The dataset was taken from- https://ori-drs.github.io/newer-college-dataset/
- The specific database used is- https://drive.google.com/drive/folders/1y3IWSYhHWnpUsleXE0q23lnj0WCVo9ig ; where I have taken 2020 dataset-folder3-file12

## Repo Guidance

- Main files-> the main files for real time testing
- Motor Car-> Test code for the motor car using L298N
- rrtstar1-> TEST code with arduino and serial connection (NOT THE FINAL CODE)
- rrtwithimu-> Test code for imu calibiration and kf (NOT THE FINAL CODE)
- printing output-> Code for visualisation 
- FINAL CODE-> The code used for testing with the motor car+printing out the coordinates to test if it is being sent through serial connection or not.
- NOTE- the valid.py code is just a sample code to check which is the valid empty coordinates in the SLAM data set so that I can put the inital nodes and the goal nodes.

##Future Improvements

- Test the PID that has been included from motor control
- Make the obstacle detection using grid map better; right now I have used the logic of height threshhold (z axis) to help the rover navigate through and avoid the obstacles in sight.
The theshhold is set to 0.1, change it accordingly
- Remote Piloting

##Sample Output
- Coordinates printed on the terminal
![coordinates](https://github.com/user-attachments/assets/068e70ad-ed12-4ec1-a7f7-7391a69f1305)

- Path printed visually
![pathfar](https://github.com/user-attachments/assets/494481e8-48d1-4c8d-83e9-78bb67ae8bb1)

- Car testing video
![cartest](https://github.com/user-attachments/assets/5b36a402-0612-4014-998f-99aa3a2f788d)

- Full Project flowchart
![Full project plan](https://github.com/user-attachments/assets/02cc790d-309c-4dba-b521-18b0e1fa4c39)



