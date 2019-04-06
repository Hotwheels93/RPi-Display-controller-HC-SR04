#Libraries
import RPi.GPIO as GPIO
import time
import os

#GPIO BOARD / BCM
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins 
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#GPIO PIN (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # Trigger HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # Trigger after 0.01ms LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    EndTime = time.time()
 
    # StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # EndTime
    while GPIO.input(GPIO_ECHO) == 1:
        EndTime = time.time()
 
    # Difference between Start und End
    TimeElapsed = EndTime - StartTime
    # multiply with speed of sound (34300 cm/s) 
    # divide by 2, for there and back 
    # Temperature as influencing factor of speed of sound, customize if needed. See table on github
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dis = distance()
            print ("Measured distance = %.1f cm" % dis)
            # Distance to power display, e.g. 90 cm
            if dis < 90:
                print("Display on")
                os.system("vcgencmd display_power 1")
                # Times until display power off in seconds
                time.sleep(60)
                os.system("vcgencmd display_power 0")
            else:
                print("Display off")
            time.sleep(1)
 
        # CTRL+C to stop
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
