import sys
import utime
from machine import *
import time
import _thread

fR = Pin(0, Pin.OUT)
pR = PWM(1)
pR.freq(15000)
percent = int(65535/100*50)
pR.duty_u16(percent)
y1 = Pin(2, Pin.OUT)
y2 = Pin(3, Pin.OUT)
y3 = Pin(4, Pin.OUT)
sensorA0 = Pin(19,Pin.IN)
sensorA1 = Pin(20,Pin.IN)
sensorB1 = Pin(21,Pin.IN)
#Variable de apoyo
prueba = Pin(25, Pin.OUT)

# Variables de comunicación entre hilo principal e hilo secundario
read = [] 
angle = 180
#prueba.on()
def servo(angle, frequency=50):
    duty = 500 + (angle/180)*2000
    duty_n = 1000000/frequency - duty
    fR.on()
    utime.sleep_us(int(duty))
    fR.off()
    utime.sleep_us(int(duty_n))


def reading():
    while True:
        global read
        global angle
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

_thread.start_new_thread(reading, ())
        
A0 = sensorA0.value() #variable de apoyo
A1 = sensorA1.value() #variable de apoyo
B1 = sensorB1.value() #variable de apoyo

while True:
    #reading()
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
    
    
    