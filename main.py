from machine import Pin

X = Pin(13, Pin.IN)
Y = Pin(14, Pin.IN)
Z = Pin(0, Pin.IN)

while True:
    print(f'X: {X.value()} Y: {Y.value()} Z: {Z.value()}')