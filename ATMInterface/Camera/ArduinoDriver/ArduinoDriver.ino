/*
Verzija: 1.0
Opis: driver za elektronički sklop koji ogreće kameru prema detektiranom licu na videu.
Autor: Karlo Grlić
Datum: 07.2015.
*/

#include <Servo.h>
#include <NewPing.h>

Servo servoLR;
Servo servoUD;

struct coordinate{
  int angle;
  int distance;
};

//Definiranje konstatni
const int minSonarAngle = 20;//-60//51
const int midSonarAngle = 89;//0
const int maxSonarAngle = 170; //60//130

const int minFaceAngle = 45;//-60//51
const int midFaceAngle = 60;//0
const int maxFaceAngle = 75; //60//130

const int LR = midSonarAngle;//48 - 90, 15 - 45, 95 - 135
const int UD = midFaceAngle;//60
const int LRMotor = 4;
const int UDMotor = 6;
const int led = 9;
const int reset = 12;
const int enable = 13;

const int sonarTrigger = 7;
const int sonarEcho = 8;
const int maxDistance = 120;
const int scanningGroups = 5;

NewPing sonar(sonarTrigger, sonarEcho, maxDistance);
byte input;


//Metode za pomicanje motora
void moveRight(int i)
{
  servoLR.write(i + 1);
}

void moveLeft(int i)
{
  servoLR.write(i - 1);
}

void moveUp(int i)
{
  servoUD.write(i + 1);
}

void moveDown(int i)
{
  servoUD.write(i - 1);   
}

int calculateDistance(){
  long duration;
  int distance;
  digitalWrite(sonarTrigger, LOW); 
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(sonarTrigger, HIGH); 
  delayMicroseconds(10);
  digitalWrite(sonarTrigger, LOW);
  duration = pulseIn(sonarEcho, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  distance = duration*0.034/2;
  return distance;
}

void moveToNearestObject() {
    int angleStepSize = maxSonarAngle - minSonarAngle;
    coordinate coordinates [angleStepSize];
    
    servoLR.write(minSonarAngle);
    delay(1000);    
    int i = 0;
    int motorPosition = servoLR.read();
    while(motorPosition <= maxSonarAngle){

      unsigned int sonarPing = sonar.ping_cm();
      
      if(sonarPing == 0){
        sonarPing = 100;
      }
      
      coordinates[i].distance = sonarPing;
      coordinates[i].angle = motorPosition;
      moveRight(motorPosition);
      delay(5);

      motorPosition = servoLR.read();
      i++;      
    }
    
    coordinate averageCoordinates [angleStepSize/scanningGroups];    
    coordinate nearestCoordinate;
    
    nearestCoordinate.angle = coordinates[0].angle;
    nearestCoordinate.distance = coordinates[0].distance;
    
    int angleSum = 0;
    int distanceSum = 0;
    
    for(int i = 1; i <= angleStepSize; i++){
      angleSum += coordinates[i].angle;
      distanceSum += coordinates[i].distance;
      if(i%scanningGroups == 0){
        averageCoordinates[i/scanningGroups].angle = angleSum/scanningGroups;
        averageCoordinates[i/scanningGroups].distance = distanceSum/scanningGroups;
        angleSum = 0;
        distanceSum = 0;
      }
    }
    
    nearestCoordinate.angle = averageCoordinates[0].angle;
    nearestCoordinate.distance = averageCoordinates[0].distance;    

    for(int i = 1; i < angleStepSize/scanningGroups; i++){
      //Serial.println(averageCoordinates[i].angle);   
      //Serial.println(averageCoordinates[i].distance); 
      //Serial.println("-------------------"); 
      if(nearestCoordinate.distance > averageCoordinates[i].distance){
          nearestCoordinate.angle = averageCoordinates[i].angle;
          nearestCoordinate.distance = averageCoordinates[i].distance;
      }
    }
 
    //Serial.println(nearestCoordinate.angle);   
    //Serial.println(nearestCoordinate.distance);
    
    if(nearestCoordinate.angle >= 20 || nearestCoordinate.angle <= 170){
      /*if(nearestCoordinate.angle < midSonarAngle){
        servoLR.write(nearestCoordinate.angle - 5);
      }
      else if(nearestCoordinate.angle > midSonarAngle){
        servoLR.write(nearestCoordinate.angle + 5);
      }
      else{
        servoLR.write(nearestCoordinate.angle);
      }*/
      servoLR.write(nearestCoordinate.angle);
    }
    else{
      servoLR.write(midSonarAngle);
    }
    
    Serial.println("1");    
    
}

void setup()
{  
   pinMode(led, OUTPUT);
   pinMode(reset, INPUT_PULLUP);
   pinMode(enable, INPUT_PULLUP);
   pinMode(sonarTrigger, OUTPUT); // Sets the trigPin as an Output
   pinMode(sonarEcho, INPUT); // Sets the echoPin as an Input
   servoLR.attach(LRMotor);
   servoUD.attach(UDMotor);
   servoLR.write(LR);
   servoUD.write(UD);
   Serial.begin(9600);
   //moveToNearestObject();
}

void loop()
{  
  
  if(digitalRead(reset) == LOW)
  {
    digitalWrite(led, HIGH);
    delay(200);
    digitalWrite(led, LOW);
    moveToNearestObject();
    //setup();
  }
  
  if(Serial.available() > 0)
    {
      digitalWrite(led, HIGH); 
      switch (Serial.read()) {
        case 1:
          moveRight(servoLR.read());
          break;
        case 2:
          moveLeft(servoLR.read());
          break;
        case 3:
          moveUp(servoUD.read());
          break;
        case 4:
          moveDown(servoUD.read());
          break;
        case 5:
          moveToNearestObject();
          break;
        case 6:
          servoUD.write(minFaceAngle);
          break;
        case 7:          
          moveUp(servoUD.read());
          delay(60);
          break;
        case 8:
          setup();
          break;
      }      
      digitalWrite(led, LOW);      
    }
}
