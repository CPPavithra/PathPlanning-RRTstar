// Refined Arduino code for MQ135 CO2 sensor
const int mq135Pin = A0; // Define the analog pin for MQ135
float CO2Curve[3] = { 116.6020682, 2.769034857, -0.47 }; // Adjust based on calibration

void setup() {
  Serial.begin(9600); // Start serial communication
  delay(30000); // Warm-up time for MQ135 (usually 24-48 hours for best accuracy)
}

void loop() {
  int sensorValue = analogRead(mq135Pin); // Read the analog value
  if (sensorValue > 0 && sensorValue < 1024) { // Validate sensor reading range
    float ppm = calculateCO2(sensorValue); // Calculate CO2 concentration
    Serial.println(ppm); // Send ppm value to Serial
  } else {
    Serial.println("Error: Out of range");
  }
  
  delay(1000); // Delay for 1 second
}

float calculateCO2(int rawValue) {
  float rs = (1023.0 / rawValue) - 1.0; // Calculate RS
  float ppm = CO2Curve[0] * pow(rs, CO2Curve[1]); // Convert to ppm using calibration curve
  return ppm;
}
