/*
Verzija: 1.0
Opis: driver za elektronički sklop koji ogreće kameru prema detektiranom licu na videu.
Autor: Karlo Grlić
Datum: 07.2015.
*/

#include <Servo.h>
Servo servoLR;
Servo servoUD;

//Definiranje konstatni
const int LR = 55;
const int UD = 25;
const int LRMotor = 4;
const int UDMotor = 6;
const int led = 9;
const int reset = 12;
const int enable = 13;
const int seralPort = 9600;

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


void setup()
{  
   pinMode(led, OUTPUT);
   pinMode(reset, INPUT_PULLUP);
   pinMode(enable, INPUT_PULLUP);
   servoLR.attach(LRMotor);
   servoUD.attach(UDMotor);
   servoLR.write(LR);
   servoUD.write(UD);
   Serial.begin(seralPort);
}

void loop()
{  
  
  if(digitalRead(reset) == LOW)
  {
    digitalWrite(led, HIGH);
    delay(200);
    digitalWrite(led, LOW);
    servoLR.write(LR);
    servoUD.write(UD);    
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
      }      
      digitalWrite(led, LOW);      
    }
}
