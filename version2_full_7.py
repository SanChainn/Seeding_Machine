
from gpiozero import Button,LED
import RPi.GPIO as GPIO
from time import sleep
import pigpio
import sys
import time



relay = LED(10)

servoPIN=17
button1 = Button(0)
button2 = Button(11)

DIR_X= 20     # Direction GPIO Pin
DIR_Y = 19

STEP_X = 21    # Step GPIO Pin
STEP_Y = 26

SWITCH = 16  # GPIO pin of switch


#servo GPIO 

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(10.3) # Initialization
print("DutyCycle : 10.3 and angle 135")



# Connect to pigpiod daemon
pi_x = pigpio.pi()
pi_y = pigpio.pi()

# Set up pins as an output
pi_x.set_mode(DIR_X, pigpio.OUTPUT)
pi_x.set_mode(STEP_X, pigpio.OUTPUT)

pi_y.set_mode(DIR_Y, pigpio.OUTPUT)
pi_y.set_mode(STEP_Y, pigpio.OUTPUT)

# Set up input switch
pi_x.set_mode(SWITCH, pigpio.INPUT)
pi_x.set_pull_up_down(SWITCH, pigpio.PUD_UP)

pi_y.set_mode(SWITCH, pigpio.INPUT)
pi_y.set_pull_up_down(SWITCH, pigpio.PUD_UP)


MODE_X = (14, 15, 18)   # Microstep Resolution GPIO Pins
MODE_Y = (5, 6, 13) 

RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}


#dir_x = sys.argv[1]
#dir_y = sys.argv[2]


for i in range(3):
    pi_x.write(MODE_X[i], RESOLUTION['Full'][i])
    pi_y.write(MODE_Y[i], RESOLUTION['Full'][i])


# Set duty cycle and frequency
pi_x.set_PWM_dutycycle(STEP_X, 200)  # PWM 1/2 On 1/2 Off
pi_x.set_PWM_frequency(STEP_X, 1250)  # 500 pulses per second

pi_y.set_PWM_dutycycle(STEP_Y, 200)  # PWM 1/2 On 1/2 Off
pi_y.set_PWM_frequency(STEP_Y, 1250)  # 500 pulses


def move_x():
	pi_x.set_PWM_dutycycle(STEP_X, 200)  # PWM 1/2 On 1/2 Off
        pi_x.set_PWM_frequency(STEP_X, 1250)

        pi_y.set_PWM_dutycycle(STEP_Y, 0)  # PWM 1/2 On 1/2 Off
        pi_y.set_PWM_frequency(STEP_Y, 0)  # 500 pulses

def stop_x():
	pi_x.set_PWM_dutycycle(STEP_X,0)
        pi_x.set_PWM_frequency(STEP_X,0)

def stop_y():
        pi_y.set_PWM_dutycycle(STEP_Y,0)
        pi_y.set_PWM_frequency(STEP_Y,0)

def move_y():
	pi_x.set_PWM_dutycycle(STEP_X, 0)  # PWM 1/2 On 1/2 Off
        pi_x.set_PWM_frequency(STEP_X, 0)

        pi_y.set_PWM_dutycycle(STEP_Y, 200)  # PWM 1/2 On 1/2 Off
        pi_y.set_PWM_frequency(STEP_Y, 1250)  # 500 pulses


def servo():
	#8.2
    p.ChangeDutyCycle(8.3)
    print("DutyCycle : 8.3 and angle 100")
    time.sleep(0.2)

    
    p.ChangeDutyCycle(10.3)
    print("DutyCycle : 10 and angle 135")
    time.sleep(0.2)


def relay_on():
	relay.on()
	print("Relay ON")
	sleep(3)
	relay.off()
	print("Relay OFF")


def backword():
	pi_x.write(DIR_X,1)
	move_x()
	print("Moving Backword")

def right():
	pi_y.write(DIR_Y,0)
	move_y()
	print("Moving Right")

def mainn():
	for i in range(1,2):
		#pi_x.write(DIR_X,0)
	        #move_x()
        	#print("Moving Forward")
	        #sleep(3)
        	#stop_x()
	        #print("STOP Forward 1 second")
        	sleep(1)
		servo()
	        for i in range(3):
        	        move_y()
                	pi_y.write(DIR_Y,1)
	                print("Moving Left")
        	        sleep(12)
	                stop_y()
			sleep(0.5)
			#Servo Motor 
			servo()
        	        print("STOP LEFT 1 second")
	                sleep(1)
        	stop_x()
	        stop_y()

        	pi_x.write(DIR_X,0)
	        move_x()
        	print("Moving Forward")
	        sleep(11)
        	stop_x()
	        print("STOP Forward 1 second")
        	sleep(1)
		servo()
	        for i in range(3):
        	        move_y()
                	pi_y.write(DIR_Y,0)
	                print("Moving Right")
        	        sleep(12)
                	stop_y()

			#Servo Motor
			servo()
	                print("STOP LEFT 1 second")
        	        sleep(1)
	        stop_x()
        	stop_y()
		
		pi_x.write(DIR_X,0)
                move_x()
                print("Moving Forward")
                sleep(11)
		sleep(1)
		servo()
                stop_x()
                print("STOP Forward 1 second")
                sleep(1)

		for i in range(3):
                        move_y()
                        pi_y.write(DIR_Y,1)
                        print("Moving Left")
                        sleep(12)
                        stop_y()
                        sleep(0.5)
                        #Servo Motor
                        servo()
                        print("STOP LEFT 1 second")
                        sleep(1)
                #stop_x()
                #stop_y()



	print("FINISH ")
	sleep(3)
	#sensor_x = 0 
	#sensor_y = 0




sensor_x = 0
sensor_y = 0

try:
    while True:
        #pi_x.write(DIR_X,int(sys.argv[1]))  # Set direction
	#pi_y.write(DIR_Y,int(sys.argv[2]))
	
	#if dir_x == 'forward' and dir_y =='left':
	#backword()
	#sleep(1)
	
	if button1.is_pressed :
		print("Button1 is pressed")
		stop_x()
		sensor_x =1
		#sleep(0.5)
	elif button1.is_pressed == False and sensor_x == 0:
		#backword()
		pi_x.write(DIR_X,1)
		print("Moving Backword")
		#sleep(0.1)
	if button2.is_pressed:
		print("Button2 is pressed")
		stop_y()
		sensor_y =1
	elif button2.is_pressed == False and sensor_y == 0:
		#right()
		pi_y.write(DIR_Y,0)
		print("Moving Right")
		#sleep(0.1)
	if sensor_x == 1 and sensor_y ==1:
		mainn()
		relay_on()
		sensor_x =0
		sensor_y =0
		# Set duty cycle and frequency
		pi_x.set_PWM_dutycycle(STEP_X, 200)  # PWM 1/2 On 1/2 Off
		pi_x.set_PWM_frequency(STEP_X, 1250)  # 500 pulses per second

		pi_y.set_PWM_dutycycle(STEP_Y, 200)  # PWM 1/2 On 1/2 Off
		pi_y.set_PWM_frequency(STEP_Y, 1250)  # 500 pulses


except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
finally:
    pi_x.set_PWM_dutycycle(STEP_X, 0)  # PWM off
    pi_x.stop()
    pi_y.set_PWM_dutycycle(STEP_Y, 0)  # PWM off
    pi_y.stop()
