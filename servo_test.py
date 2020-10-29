# import libraries
import RPi.GPIO as GPIO
import time

# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# set pin 11 as an output and set servo1 as pin as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11, 50 hz

# start PWM but with a zero value
servo1.start(0)
print("waiting for 2 seconds!")
time.sleep(2)

# move the servo
print("Rotating 180 degrees in 10 steps")

duty = 2

# loop duty values between 2 and 12
while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty +1

time.sleep(2)

# turn back to 90 degrees
print("Turning back to 90 degrees for 2 seconds")
servo1.ChangeDutyCycle(7)
time.sleep(2)

# turn back to 0 degrees
print("Turning back to 0 degrees for 2 seconds")
servo1.ChangeDutyCycle(2)
time.sleep(2)

# clean things up
servo1.stop()
GPIO.cleanup()
print("Goodbye!")

