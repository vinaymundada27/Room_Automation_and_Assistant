import RPi.GPIO as IO
from time import sleep

# Set the pin addressing mode
IO.setmode(IO.BCM)

from gpiozero import LightSensor, Buzzer

LDR_DATA_PIN = 22
ldr = LightSensor(LDR_DATA_PIN)
while True:
	print(ldr.value)


