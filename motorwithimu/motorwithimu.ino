#include <Wire.h>
#include <MPU6050.h>

MPU6050 imu;

const int AIN1 = 9;
const int AIN2 = 8;
const int PWMA = 10;
const int BIN1 = 7;
const int BIN2 = 6;
const int PWMB = 5;

const int ACTUATOR_IN1 = 4;
const int ACTUATOR_IN2 = 3;
const int PWMACT = 2;

float currentHeading = 0.0;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    imu.initialize();
    
    if (!imu.testConnection()) {
        Serial.println("MPU6050 connection failed!");
        while (1);
    } else {
        Serial.println("MPU6050 connection successful!");
    }

    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(PWMA, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    pinMode(PWMB, OUTPUT);
    
    pinMode(ACTUATOR_IN1, OUTPUT);
    pinMode(ACTUATOR_IN2, OUTPUT);
    pinMode(PWMACT, OUTPUT);
}

void loop() {
    if (Serial.available()) {
        String coords = Serial.readStringUntil('\n');
        int commaIndex = coords.indexOf(',');
        if (commaIndex > 0) {
            String xStr = coords.substring(0, commaIndex);
            String yStr = coords.substring(commaIndex + 1);
            float x = xStr.toFloat();
            float y = yStr.toFloat();
            
            move_rover_to_target(x, y);
            
            if (reached_target(x, y)) {
                collect_soil();
            }
        }
    }
}

void move_rover_to_target(float targetX, float targetY) {
    while (true) {
        // Update current heading with IMU data
        currentHeading = getHeading(); // Custom function to fetch heading
        
        float deltaX = targetX - currentX;
        float deltaY = targetY - currentY;
        float desiredHeading = atan2(deltaY, deltaX) * 180 / PI; // Calculate angle in degrees
        
        // Rotate to face the target
        if (abs(desiredHeading - currentHeading) > 5) {  // Adjust threshold as needed
            if (desiredHeading > currentHeading) {
                right();
            } else {
                left();
            }
        } else {
            forward();
        }

        // Check if the rover is within range of the target
        float threshold = 0.1;
        if (abs(deltaX) < threshold && abs(deltaY) < threshold) {
            stop_motors();
            break;
        }
    }
}

// Function to read heading from IMU
float getHeading() {
    int16_t ax, ay, az, gx, gy, gz;
    imu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // Calculate heading angle in degrees using gyro and accelerometer data
    return atan2(ay, ax) * 180 / PI;
}

void forward(){   
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 200); 
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 200);  
    delay(1000);  
}

void backward(){    
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 200);  
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 200); 
    delay(1000); 
}

void left(){
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    analogWrite(PWMA, 200);  
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 200);  
    delay(1000);  
}

void right(){
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 200); 
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    analogWrite(PWMB, 200); 
    delay(1000);  
}

void stop_motors() {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, LOW);
}

bool reached_target(float currentX, float currentY) {
    return true;
}

void collect_soil() {
    extend();
    delay(3000); 
    retract_actuator();
    delay(3000);
}

void extend() {
    digitalWrite(ACTUATOR_IN1, HIGH);
    digitalWrite(ACTUATOR_IN2, LOW);
    analogWrite(PWMACT, 255);  
}

void pullback() {
    digitalWrite(ACTUATOR_IN1, LOW);
    digitalWrite(ACTUATOR_IN2, HIGH);
    analogWrite(PWMACT, 255);  
}
