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
    float deltaX, deltaY;

    while (true) {
        deltaX = targetX - currentX;
        deltaY = targetY - currentY;

        // Check if the target is reached
        if (abs(deltaX) < threshold && abs(deltaY) < threshold) {
            stop_motors();
            Serial.println("reached");  // Send acknowledgment to Python
            break;
        }

        // Calculate the angle to the target
        float angle = atan2(deltaY, deltaX);
        float distance = sqrt(deltaX * deltaX + deltaY * deltaY);

        // Determine direction and move accordingly
        if (distance > threshold) {
            if (abs(angle) < 0.1) { // Move forward
                forward();
                Serial.println("moving forward");
            } else if (abs(angle - PI) < 0.1 || abs(angle + PI) < 0.1) { // Move backward
                backward();
                Serial.println("moving backward");
            } else if (angle > 0) { // Target is to the left
                left();
                Serial.println("turning left");
            } else { // Target is to the right
                right();
                Serial.println("turning right");
            }

            delay(100); // Delay to allow movement; adjust based on speed
        } else {
            stop_motors();
            Serial.println("reached");  // Send acknowledgment to Python
            break;
        }

        // Update current position based on speed and time elapsed
        update_position(deltaX, deltaY);
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
