from emulatorexec import *
import os
import time


x = EmulatorGBN()
x.setEmitterParams(winsz=10, timeout=10)
x.setConnectionParams(loss=3, rate=100000, distance=0, speed=10000)

while True:
    x.run()
    time.sleep(1)