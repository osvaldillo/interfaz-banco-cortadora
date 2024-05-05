import asyncio
import serial

async def tarea1():
    ser = serial.Serial('COM6', 9600)
    while True:
        await asyncio.sleep(5)
        if ser.in_waiting > 0:
            print(ser.readline().decode('utf-8'))
            ser.write('A'.encode())

    #print("Tarea 1 iniciada")
    #await asyncio.sleep(1)
    #print("Tarea 1 finalizada")

async def tarea2():
    i = 0
    while True:
        i += 1
        print(i)
        await asyncio.sleep(1)

async def tareasParalelo():
    #crear dos tareas a partir de las funciones tarea1 y tarea2
    _tarea1 = asyncio.create_task(tarea1())
    _tarea2 = asyncio.create_task(tarea2())

    #Ejecutar ambas tareas
    await asyncio.gather(_tarea1, _tarea2)

#Ejecutar la función tareasParalelo

asyncio.run(tareasParalelo())


