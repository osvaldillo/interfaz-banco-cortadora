String data;
#define cilinderAplus 4
#define cilinderAminus 3
#define cilinderB 2
#define sensorA0 12
#define sensorA1 11
#define sensorB1 10

int i;

void setup() {
    Serial.begin(9600);
    pinMode(cilinderAplus, OUTPUT);
    pinMode(cilinderAminus, OUTPUT);
    pinMode(cilinderB, OUTPUT);
    pinMode(sensorA0, INPUT);
    pinMode(sensorA1, INPUT);
    pinMode(sensorB1, INPUT);
}

void loop() {
    if (Serial.available() > 0) { 
        data = Serial.readStringUntil(','); 
        if(data == "A+"){
          digitalWrite(cilinderAplus, HIGH);
          delay(1000);
          digitalWrite(cilinderAplus, LOW);
        }
        else if(data == "A-"){
          digitalWrite(cilinderAminus, HIGH);
          delay(1000);
          digitalWrite(cilinderAminus, LOW);
        }
        else if(data == "B+"){
          digitalWrite(cilinderB, HIGH);
        }
        else if(data == "B-"){
          digitalWrite(cilinderB, LOW);
        }
        else if(data == "Start secuence"){
          while(!digitalRead(sensorA0) or digitalRead(sensorA1) or digitalRead(sensorB1)){
            digitalWrite(cilinderAminus, HIGH);
            digitalWrite(cilinderB, LOW);
          }
          digitalWrite(cilinderAminus, LOW);
          delay(500);
          while(!digitalRead(sensorA1)){
            digitalWrite(cilinderAplus, HIGH);
            delay(100);
            digitalWrite(cilinderAplus, LOW);
            digitalWrite(cilinderB, HIGH);
            delay(100);
            digitalWrite(cilinderB, LOW);
            delay(100);
          }
          while(!digitalRead(sensorA0)){
            digitalWrite(cilinderAminus, HIGH);
            delay(1000);
            digitalWrite(cilinderAminus, LOW);
          }
        }
    }
}
