// Motor A - Left side
const int IN1 = 9;
const int IN2 = 8;
const int ENA = 10;

// Motor B - Right side
const int IN3 = 7;
const int IN4 = 6;
const int ENB = 5;

// Variables for tracking position
float currentX = 0; 
float currentY = 0;

// Speed settings
const int motorSpeed = 200;  // Set the motor speed (0-255)

void setup() {
    Serial.begin(9600);
    
    // Motor pin modes
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);
}
void loop() {
    if (Serial.available()) {
        String coords = Serial.readStringUntil('\n');
        int commaIndex = coords.indexOf(',');
        if (commaIndex > 0) {
            String xStr = coords.substring(0, commaIndex);
            String yStr = coords.substring(commaIndex + 1);
            float targetX = xStr.toFloat();
            float targetY = yStr.toFloat();
            
            Serial.print("Moving to: ");
            Serial.print(targetX);
            Serial.print(", ");
            Serial.println(targetY);
            
            move_rover_to_target(targetX, targetY);
            Serial.println("reached"); // Send acknowledgment after reaching the target
            delay(100); // Add a delay after sending acknowledgment
        }
    }
}


void move_rover_to_target(float targetX, float targetY) {
    float threshold = 0.1; // Acceptable distance to consider the target reached
    
    while (true) {
        float deltaX = targetX - currentX;
        float deltaY = targetY - currentY;

        // Check if the target is reached
        if (abs(deltaX) < threshold && abs(deltaY) < threshold) {
            stop_motors();
            Serial.println("reached");
            break;
        }

        if (abs(deltaX) > abs(deltaY)) {
            // Move along X-axis
            if (deltaX > 0) {
                forward(); // Moving forward towards positive X
            } else {
                backward(); // Moving backward towards negative X
            }
            // Minor adjustment along Y-axis
            if (deltaY > threshold) {
                right();
            } else if (deltaY < -threshold) {
                left();
            }
        } else {
            // Move along Y-axis
            if (deltaY > 0) {
                right(); // Moving towards positive Y
            } else {
                left(); // Moving towards negative Y
            }
            // Minor adjustment along X-axis
            if (deltaX > threshold) {
                forward();
            } else if (deltaX < -threshold) {
                backward();
            }
        }
        delay(100); // Delay for smoother movement control
    }
}

     



void update_position(float deltaX, float deltaY) {
    // Assume the rover moves 1 unit in x or y for every update
    // Adjust these values based on your movement speed and time
    currentX += (abs(deltaX) > abs(deltaY)) ? (deltaX > 0 ? 1 : -1) : 0;
    currentY += (abs(deltaY) > abs(deltaX)) ? (deltaY > 0 ? 1 : -1) : 0;
}

void forward() {   
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, motorSpeed); // Set left motor speed
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, motorSpeed); // Set right motor speed
}

void backward() {    
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, motorSpeed);  // Set left motor speed
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, motorSpeed);  // Set right motor speed
}

void left() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);      // Stop left motor
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, motorSpeed);    // Run right motor forward
    delay(500); // Adjust the rotation duration
}

void right() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, motorSpeed);    // Run left motor forward
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, 0);      // Stop right motor
    delay(500); // Adjust the rotation duration
}

void stop_motors() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}
