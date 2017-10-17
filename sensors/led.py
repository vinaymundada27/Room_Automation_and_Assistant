import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

pin = 26
GPIO.setup(pin,GPIO.OUT)

while True:
	#print "LED on"
	GPIO.output(pin, True)
	time.sleep(1)
	#print "LED off"
	GPIO.output(pin, False)
	time.sleep(1)
