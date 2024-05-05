import sys
import utime
from machine import *
import time
import _thread


read = []
flowReg = PWM(0)
flowReg.freq(50)
#presReg = PWM(1)
#presReg.freq(15000)
cilinderAplus = Pin(2, Pin.OUT)
cilinderAminus = Pin(3, Pin.OUT)
cilinderB = Pin(4, Pin.OUT)
sensorA0 = Pin(19,Pin.IN)
sensorA1 = Pin(20,Pin.IN)
sensorB1 = Pin(21,Pin.IN)
prueba = Pin(25, Pin.OUT)
A0 = sensorA0.value()
A1 = sensorA1.value()
B1 = sensorB1.value()

def reading():
    while True:
        global read
        data  = str(sys.stdin.readline())
        prueba.off()
        read = list(data)
        if read[0] == "A":
            if read[1] == '+':
                cilinderAplus.on()
                cilinderAminus.off()
            elif read[1] == '-':
                cilinderAplus.off()
                cilinderAminus.on()
        elif read[0] == "B":
            if read[1] == '+':
                cilinderB.on()
            elif read[1] == '-':
                cilinderB.off()
        elif read[0] == "F":
            num = ""
            #prueba.on()
            for i in read[2:]:
                if i == "'\'": break
                num += i
            duty = 1000 + int(7955*int(num)/180)
            print(duty)
            flowReg.duty_u16(duty)
        #else:
            #prueba.on()
        #utime.sleep(0.5)

#_thread.start_new_thread(reading, ())
        
    
while True:
    prueba.on()
    reading()
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
        sender = f'A0: {A0} A1: {A1} B1: {B1}'
        sys.stdout.write(sender + '\r\n')