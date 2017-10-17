import RPi.GPIO as IO
from time import sleep

PIR_DATA_PIN = 13
# Set the pin addressing mode
IO.setmode(IO.BOARD)

# Set IO pins
IO.setup(PIR_DATA_PIN, IO.IN, IO.PUD_DOWN)
# OUTPUT: IO.setup(PN, IO.OUT)

# Read from input Pin and do something
while True:
	print IO.input(PIR_DATA_PIN)
	sleep(0.25)

# INPUT	: IO.input(PIN_NUMBER)
# OUTPUT: IO.output(PIN_NUMBER, IO.HIGH)

