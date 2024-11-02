// Pin definitions for Cytron Motor Driver with 4 wheels and 2 motor drivers
const int LEFT_MOTOR_DIR = 9;     // Direction pin for left motor driver
const int LEFT_MOTOR_PWM = 10;    // PWM pin for left motor driver
const int RIGHT_MOTOR_DIR = 7;    // Direction pin for right motor driver
const int RIGHT_MOTOR_PWM = 5;    // PWM pin for right motor driver

// Actuator pins
const int ACTUATOR_IN1 = 4;
const int ACTUATOR_IN2 = 3;
const int PWMACT = 2;

// Receiver Channels
const int CH1_PIN = 11; // Move forward/backward
const int CH2_PIN = 12; // Move left/right
const int CH3_PIN = 13; // Actuator control
const int MODE_PIN = 13; // Toggle between autonomous and manual mode

bool isAutonomousMode = true; // Start in autonomous mode

void setup() {
    Serial.begin(9600);
    
    pinMode(LEFT_MOTOR_DIR, OUTPUT);
    pinMode(LEFT_MOTOR_PWM, OUTPUT);
    pinMode(RIGHT_MOTOR_DIR, OUTPUT);
    pinMode(RIGHT_MOTOR_PWM, OUTPUT);
    
    pinMode(ACTUATOR_IN1, OUTPUT);
    pinMode(ACTUATOR_IN2, OUTPUT);
    pinMode(PWMACT, OUTPUT);

    pinMode(CH1_PIN, INPUT);
    pinMode(CH2_PIN, INPUT);
    pinMode(CH3_PIN, INPUT);
    pinMode(MODE_PIN, INPUT);
}

void loop() {
    // Check mode from MODE_PIN
    int modeSignal = pulseIn(MODE_PIN, HIGH, 25000);
    
    // Toggle between autonomous and manual modes
    if (modeSignal > 1500) {
        isAutonomousMode = true; // High signal, autonomous mode
    } else {
        isAutonomousMode = false; // Low signal, manual mode
    }

    if (isAutonomousMode) {
        // Autonomous mode - follow coordinates from serial input
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
    } else {
        // Manual piloting mode - control via remote
        manual_control();
    }
}

void manual_control() {
    int ch1Value = pulseIn(CH1_PIN, HIGH, 25000); // Forward/backward
    int ch2Value = pulseIn(CH2_PIN, HIGH, 25000); // Left/right
    int ch3Value = pulseIn(CH3_PIN, HIGH, 25000); // Actuator control
    int NEUTRAL_ZONE = 100; // Threshold for joystick dead zone

    // Forward/Backward Control
    if (ch1Value > 1500 + NEUTRAL_ZONE) {
        forward();
    } else if (ch1Value < 1500 - NEUTRAL_ZONE) {
        backward();
    } else {
        stop_motors();
    }

    // Left/Right Control
    if (ch2Value > 1500 + NEUTRAL_ZONE) {
        right();
    } else if (ch2Value < 1500 - NEUTRAL_ZONE) {
        left();
    }

    // Actuator Control
    if (ch3Value > 1500 + NEUTRAL_ZONE) {
        extend();
    } else if (ch3Value < 1500 - NEUTRAL_ZONE) {
        pullback();
    }
}

void move_rover_to_target(float targetX, float targetY) {
    // Autonomous movement logic
    float deltaX = targetX; // Replace with current position tracking if available
    float deltaY = targetY;

    float threshold = 0.1;

    while (true) {
        if (abs(deltaX) < threshold && abs(deltaY) < threshold) {
            stop_motors();
            break;
        }

        if (abs(deltaX) > abs(deltaY)) {
            if (deltaX > 0) forward();
            else backward();
        } else {
            if (deltaY > 0) right();
            else left();
        }
    }
}

// Motor Control Functions for Cytron Driver (2 motors for 4 wheels)
void forward() {   
    digitalWrite(LEFT_MOTOR_DIR, HIGH); // Set forward direction for left motor
    analogWrite(LEFT_MOTOR_PWM, 200);   // Set speed
    digitalWrite(RIGHT_MOTOR_DIR, HIGH); // Set forward direction for right motor
    analogWrite(RIGHT_MOTOR_PWM, 200);
}

void backward() {    
    digitalWrite(LEFT_MOTOR_DIR, LOW); // Set reverse direction for left motor
    analogWrite(LEFT_MOTOR_PWM, 200);  
    digitalWrite(RIGHT_MOTOR_DIR, LOW); // Set reverse direction for right motor
    analogWrite(RIGHT_MOTOR_PWM, 200); 
}

void left() {
    digitalWrite(LEFT_MOTOR_DIR, LOW); // Reverse left motor
    analogWrite(LEFT_MOTOR_PWM, 200);  
    digitalWrite(RIGHT_MOTOR_DIR, HIGH); // Forward right motor
    analogWrite(RIGHT_MOTOR_PWM, 200);  
}

void right() {
    digitalWrite(LEFT_MOTOR_DIR, HIGH); // Forward left motor
    analogWrite(LEFT_MOTOR_PWM, 200); 
    digitalWrite(RIGHT_MOTOR_DIR, LOW); // Reverse right motor
    analogWrite(RIGHT_MOTOR_PWM, 200); 
}

void stop_motors() {
    analogWrite(LEFT_MOTOR_PWM, 0);
    analogWrite(RIGHT_MOTOR_PWM, 0);
}

bool reached_target(float currentX, float currentY) {
    // Placeholder for checking if target is reached
    return true;
}

void collect_soil() {
    extend();
    delay(3000); 
    pullback();
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
