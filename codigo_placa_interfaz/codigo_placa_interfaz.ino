String data;
#define cilindroEmpujador 12
#define cilindroCortador 11

void setup() {
    Serial.begin(9600);
    pinMode(cilindroEmpujador, OUTPUT);
    pinMode(cilindroCortador, OUTPUT);
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
    }
}
