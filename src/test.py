from emulatorexec import *
import os
import time


x = EmulatorSW()
x.setEmitterParams(timeout=10)
x.setConnectionParams(loss=40, rate=100000, distance=0, speed=10000)

while True:
    x.run()
    time.sleep(1)