import sys
import utime
from machine import *
import time
import _thread

fR = Pin(22, Pin.OUT)
pR = PWM(21) 
pR.freq(15000)
y1 = Pin(26, Pin.OUT)
y2 = Pin(27, Pin.OUT)
y3 = Pin(28, Pin.OUT)
sensorA0 = Pin(0,Pin.IN)
sensorA1 = Pin(15,Pin.IN)
sensorB1 = Pin(14,Pin.IN)
#Variable de apoyo
prueba = Pin(25, Pin.OUT)

# Variables de comunicación entre hilo principal e hilo secundario
read = [] 
angle = 180
pressure = 1

#prueba.on()
def servo(angle, frequency=50):
    duty = 500 + (angle/180)*2000
    duty_n = 1000000/frequency - duty
    fR.off()
    utime.sleep_us(int(duty))
    fR.on()
    utime.sleep_us(int(duty_n))


def reading():
    while True:
        global read
        global angle
        global pressure
        data  = str(sys.stdin.readline())
        prueba.off()
        read = list(data)
        if read[0] == "A":
            if read[1] == '+':
                y1.on()
                y2.off()
            elif read[1] == '-':
                y1.off()
                y2.on()
            elif read[1] == '*':
                y1.off()
                y2.off()
        elif read[0] == "B":
            if read[1] == '+':
                y3.on()
            elif read[1] == '-':
                y3.off()
        elif read[0] == "F":
            num = ""
            for i in read[2:]:
                if i == "'\'": break
                num += i
            angle = int(num)
        elif read[0] == "P":
            num = ""
            for i in read[2:]:
                if i == "'\'": break
                num += i
            pressure = int(num)
        elif read[0] == 'S':
            while A0 != 1:
                y2.on()
                y1.off()
            while A1 == 0:
                y1.on()
                y2.off()
                utime.sleep_ms(100)
                y1.off()
                y3.on()
                utime.sleep_ms(100)
                y3.off()
            y2.on()
            
            
            

_thread.start_new_thread(reading, ())
        
A0 = sensorA0.value() #variable de apoyo
A1 = sensorA1.value() #variable de apoyo
B1 = sensorB1.value() #variable de apoyo

while True:
    #reading()
    #global A0
    #global A1
    #global B1
    servo(angle)
    changed = False
    if A0 != sensorA0.value():
        A0 = sensorA0.value()
        changed = True
    if A1 != sensorA1.value():
        A1 = sensorA1.value()
        changed = True
    if B1 != sensorB1.value():
        B1 = sensorB1.value()
        changed = True
    if changed:
        prueba.on()
        sender = f'A0: {A0} A1: {A1} B1: {B1}'
        sys.stdout.write(sender + '\r\n')
    pR.duty_u16(int(65535*pressure/100))
    
    
    
