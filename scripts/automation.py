# Code for humidity sensor

################# IMPORTS ###############################
import RPi.GPIO as GPIO
import time, datetime
from time import sleep
import dht11
from gpiozero import LightSensor, Buzzer

from speech_text import *
from smart_agent import *
import thread

########## GLOBAL PARAMETERS #################
import settings

########## INITIALIZE GPIO ######################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


############################ HUMIDITY SENSOR #################################
def humidity():
	print("Humidity running")	
	HUMIDITY_DATA_PIN = 4
	scale = 0.35
	instance = dht11.DHT11(pin=HUMIDITY_DATA_PIN)
	old_temp = 30
	while settings.FAN_AUTOMATION_OFF :
	    result = instance.read()
	    if result.is_valid():
		temp = result.temperature
		humidity = result.humidity
		new_temp = temp
		diff = new_temp - old_temp
		
		#global FAN_FREQ
		settings.FAN_FREQ_TRUE = max(0.2, settings.FAN_FREQ_TRUE - diff * scale)
		settings.FAN_FREQ_FALSE = max(0.2, settings.FAN_FREQ_FALSE - diff * scale)
		
		old_temp = new_temp
	        print("Temperature: %d C" % temp)
        	print("Humidity: %d %%" % humidity) 		

	    time.sleep(1)
	print "---------------FAN AUTOMATION IS OFF-------------"


def fan_led():
	FAN_PIN = 26
	GPIO.setup(FAN_PIN,GPIO.OUT)
	
	while True:
	        #print "LED on"
       	 	GPIO.output(FAN_PIN, True)
	        time.sleep(settings.FAN_FREQ_TRUE)
        	#print "LED off"
	        GPIO.output(FAN_PIN, False)
	        time.sleep(settings.FAN_FREQ_FALSE)
	

######################################## LDR SENSOR ###############################################################
def ldr():
	print("LDR running")
	LDR_DATA_PIN = 22
	ldr = LightSensor(LDR_DATA_PIN)
	while settings.LIGHT_AUTOMATION_OFF:
		intensity = ldr.value
		print("ldr : " + str(intensity))
		if intensity == 0.0 :
			#global LIGHT_FREQ
			settings.LIGHT_FREQ_TRUE = 0.001
			settings.LIGHT_FREQ_FALSE = 0.001
		else:
			#global LIGHT_FREQ
			settings.LIGHT_FREQ_TRUE = 0.5
			settings.LIGHT_FREQ_FALSE = 0.5

		#elif intensity > 30 and intensity < 60:
			#global LIGHT_FREQ
		  	#settings.LIGHT_FREQ = 0.2

		#elif intensity > 60:
			#global LIGHT_FREQ
			#settings.LIGHT_FREQ = 0.5
		
		time.sleep(0.5)

	print "--------------LIGHTS AUTOMATION IS OFF-------------"
	print "true : ", settings.LIGHT_FREQ_TRUE
	print "false: ", settings.LIGHT_FREQ_FALSE
	settings.LIGHT_FREQ_TRUE = settings.MIN
	settings.LIGHT_FREQ_FALSE = settings.MAX


def light_led():
	LIGHT_PIN = 20
	GPIO.setup(LIGHT_PIN,GPIO.OUT)
	
	while True:
	        #print "LED on"
       	 	GPIO.output(LIGHT_PIN, True)
	        time.sleep(settings.LIGHT_FREQ_TRUE)
        	#print "LED off"
	        GPIO.output(LIGHT_PIN, False)
	        time.sleep(settings.LIGHT_FREQ_FALSE)


####################################### PIR SENSOR #################################################################
def pir():

	PIR_DATA_PIN = 27
	# Set the pin addressing mode
	#GPIO.setmode(IO.BOARD)	

	# Set GPIO pins
	GPIO.setup(PIR_DATA_PIN, GPIO.IN, GPIO.PUD_DOWN)
	# OUTPUT: GPIO.setup(PN, IO.OUT)

	# Read from input Pin and do something
	value = GPIO.input(PIR_DATA_PIN)
	print "Human detected %d " %value
	sleep(1)
	return value

	# INPUT	: IO.input(PIN_NUMBER)
	# OUTPUT: IO.output(PIN_NUMBER, IO.HIGH)


#### Start the mic #####
def start_mic():
	## Listen only for "hello buddy" ##
	keep_listening()


### Start automation ####
def start_automation():
	
	# trigger humidity sensor
	thread.start_new_thread(humidity,())
	thread.start_new_thread(fan_led,())

	# trigger ldr sensor
	thread.start_new_thread(ldr,())
	thread.start_new_thread(light_led,())


def trigger_auto_mic():
	
	# Start Thread 2 for Automation 
	start_automation()	

	# Start Thread 1 for Mic
	thread.start_new_thread(start_mic())	

def start():	
	while True:
		person_detected = pir()
		if person_detected:
			print("Person detected")
			speak("Person Detected. Welcome Geetha maam. I am BUDDY you'r personal voice assisntant")
			trigger_auto_mic()


print("starting the code")
start()
#trigger_auto_mic()

while 1:
	pass
