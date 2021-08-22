from time import sleep
import pigpio
import sys

DIR_X= 20     # Direction GPIO Pin
DIR_Y = 19

STEP_X = 21    # Step GPIO Pin
STEP_Y = 26

SWITCH = 16  # GPIO pin of switch


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


dir_x = sys.argv[1]
dir_y = sys.argv[2]


for i in range(3):
    pi_x.write(MODE_X[i], RESOLUTION['Full'][i])
    pi_y.write(MODE_Y[i], RESOLUTION['Full'][i])


# Set duty cycle and frequency
pi_x.set_PWM_dutycycle(STEP_X, 200)  # PWM 1/2 On 1/2 Off
pi_x.set_PWM_frequency(STEP_X, 1250)  # 500 pulses per second

pi_y.set_PWM_dutycycle(STEP_Y, 200)  # PWM 1/2 On 1/2 Off
pi_y.set_PWM_frequency(STEP_Y, 1250)  # 500 pulses

try:
    while True:
        #pi_x.write(DIR_X,int(sys.argv[1]))  # Set direction
	#pi_y.write(DIR_Y,int(sys.argv[2]))
	if dir_x == 'forward':
		print("Moving Forward")
		pi_x.write(DIR_X,0)
	elif dir_x == 'backward':
		print("Moving Backward")
		pi_x.write(DIR_X,1)
	#elif int(dir_x) == 0:
	else:
		pi_x.set_PWM_dutycycle(STEP_X, 0)  # PWM off
		#pi_x.stop()

        if dir_y == 'left':
		pi_y.write(DIR_Y,1)
		print("Moving Left")
        elif dir_y == 'right':
		pi_y.write(DIR_Y,0)
		print("Moving Right")
	else:
		pi_y.set_PWM_dutycycle(STEP_Y, 0)  # PWM off
    		#pi_y.stop()


except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
finally:
    pi_x.set_PWM_dutycycle(STEP_X, 0)  # PWM off
    pi_x.stop()
    pi_y.set_PWM_dutycycle(STEP_Y, 0)  # PWM off
    pi_y.stop()
