String data;
#define cilindroEmpujador 1
#define cilindroCortador 11
#define retroceso 10
#define sensor 27
int i;

void setup() {
    Serial.begin(9600);
    pinMode(cilindroEmpujador, OUTPUT);
    pinMode(cilindroCortador, OUTPUT);
    pinMode(retroceso, OUTPUT);
    pinMode(sensor, INPUT);
}

void loop() {
    if (Serial.available() > 0) { 
        data = Serial.readStringUntil(','); 
        if(data == "EC"){
          digitalWrite(cilindroEmpujador, HIGH);
        }
        else if(data == "CC"){
          digitalWrite(cilindroEmpujador, LOW);
        }
        else if(data == "EG"){
          digitalWrite(cilindroCortador, HIGH);
        }
        else if(data == "CG"){
          digitalWrite(cilindroCortador, LOW);
        }
        else if(data == "SE"){
          i = 0;
          while( i< 10){
            digitalWrite(cilindroCortador, HIGH);
            delay(100);
            digitalWrite(cilindroCortador, LOW);
            delay(100);
            i++;
          }
        }
        else if (data == "PN"){
          i = 0;
          while(!digitalRead(sensor)){
            digitalWrite(cilindroEmpujador, HIGH);
            delay(1000);Z
            digitalWrite(cilindroEmpujador, LOW);
            digitalWrite(cilindroCortador, HIGH);
            delay(1000);
            digitalWrite(cilindroCortador, LOW);
            delay(1000);
            //i++;
          }
          digitalWrite(retroceso, HIGH);
          delay(5000);
          digitalWrite(retroceso, LOW);
          


        }
    }
}
