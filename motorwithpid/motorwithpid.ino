
const int IN1 = 9;
const int IN2 = 8;
const int ENA = 10;

const int IN3 = 7;
const int IN4 = 6;
const int ENB = 5;


float currentX = 0; 
float currentY = 0;


const int maxMotorSpeed = 255;  
int motorSpeed = 0; 

float Kp = 0.5;  
float Ki = 0.1;  
float Kd = 0.05; 

float integralX = 0, integralY = 0;
float previousErrorX = 0, previousErrorY = 0;
unsigned long lastTime;

void setup() {
    Serial.begin(9600);
    
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);

    lastTime = millis();
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
            Serial.println("reached"); 
            delay(100); 
        }
    }
}

void move_rover_to_target(float targetX, float targetY) {
    float threshold = 0.1; 

    while (true) {
        float errorX = targetX - currentX;
        float errorY = targetY - currentY;

        if (sqrt(errorX * errorX + errorY * errorY) < threshold) {
            stop_motors();
            Serial.println("reached");  
            break;
        }

        unsigned long currentTime = millis();
        float deltaTime = (currentTime - lastTime) / 1000.0; // Convert to seconds
        lastTime = currentTime;

        integralX += errorX * deltaTime;
        float derivativeX = (errorX - previousErrorX) / deltaTime;
        previousErrorX = errorX;

        // PID for Y
        integralY += errorY * deltaTime;
        float derivativeY = (errorY - previousErrorY) / deltaTime;
        previousErrorY = errorY;

        float controlX = Kp * errorX + Ki * integralX + Kd * derivativeX;
        float controlY = Kp * errorY + Ki * integralY + Kd * derivativeY;

        float angle = atan2(controlY, controlX);
        motorSpeed = constrain(sqrt(controlX * controlX + controlY * controlY), 0, maxMotorSpeed);

        if (abs(controlX) > abs(controlY)) {
            if (controlX > 0) {
                forward();
            } else {
                backward();
            }
        } else {
            if (controlY > 0) {
                right();
            } else {
                left();
            }
        }

        update_position(controlX, controlY);

        delay(100); 
    }
}

void update_position(float deltaX, float deltaY) {
    currentX += (abs(deltaX) > abs(deltaY)) ? (deltaX > 0 ? 0.1 : -0.1) : 0;
    currentY += (abs(deltaY) > abs(deltaX)) ? (deltaY > 0 ? 0.1 : -0.1) : 0;
}

void forward() {   
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, motorSpeed); 
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, motorSpeed); 
}

void backward() {    
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, motorSpeed);  
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, motorSpeed);  
}

void left() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);      
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, motorSpeed);    
    delay(500); 
}

void right() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, motorSpeed);    
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, 0);     
    delay(500); 
}

void stop_motors() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}
