# define PIN_MOTOR 9
# define PIN_TRIG 3
# define PIN_ECHO 2
# define SMALL_DISTANCE 50
# define SOUND_SPEED_COEFF 58
int distances[20];
int numOfDists = 20;

void setup() {
  pinMode(PIN_MOTOR, OUTPUT);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  Serial.begin(9600);
  resetDistance();
}

void deceleration() {
  for(int i = 127; i >= 15; i-= 16) {
    if (i % 64 == 63) Serial.println("decelerating...");
    analogWrite(PIN_MOTOR, i);
    delay(20);
  }
  analogWrite(PIN_MOTOR, 20);
  delay(2500);
  analogWrite(PIN_MOTOR, 0);
  Serial.println("decelerated!");
}

void acceleration(){
  for(int i = 0; i < 256; i++) {
    if (i % 64 == 0) Serial.println("accelerating..."); 
    analogWrite(PIN_MOTOR, i);
    delay(1);
  }
  for (int i = 255; i >= 110; i--) {
    analogWrite(PIN_MOTOR, i);
    delay(1);
  }
  Serial.println("accelerated!");
}

void resetDistance(){
  for (int i = 0; i < numOfDists; i++){
    distances[i] = 100;
  }
}

void updateDistance(){
  for(int i = 0; i < numOfDists; i++) {
    distances[i] = distances[i + 1];
  }
  distances[numOfDists - 1] = distance();
}

int distance() {
  int duration, cm;
  digitalWrite(PIN_TRIG, LOW); 
  delayMicroseconds(2); 
  digitalWrite(PIN_TRIG, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(PIN_TRIG, LOW); 
  duration = pulseIn(PIN_ECHO, HIGH); 
  cm = duration/SOUND_SPEED_COEFF;
  return cm;
}

boolean isNear(){
  updateDistance();
  int avgDist = 0;
  for (int i = 0; i < numOfDists; i++) {
    avgDist = avgDist + distances[i];
  }
  avgDist = avgDist/numOfDists;
  if (avgDist < 0) return isNear();
  Serial.println(avgDist);
  if (avgDist < SMALL_DISTANCE) { 
    return true; 
  }
  else {
    return false;
  }
  
}

void loop() {
  delay(2000);
  acceleration();
  delay(2000);
  while (!isNear()) { delay(1); }
  deceleration();
  delay(2000);
  Serial.println("TIME_TO_TAKE_A_PICTURE");
  resetDistance();
}
