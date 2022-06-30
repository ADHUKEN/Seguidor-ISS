import RPi.GPIO as GPIO
import time
from RpiMotorLib import RpiMotorLib


    
servoPIN = 18
#Movimiento del azimut ingresado
direction= 20 # Direction (DIR) GPIO Pin
step = 21 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)
mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) 
p.start(0) 


def setAngle(angle):
    duty = (angle / 18) + 2
    p.ChangeDutyCycle(duty)
    time.sleep(0.2)
    p.ChangeDutyCycle(0)



def angleToSteps(angle):
    steps = 3200
    result = int((angle*steps)/360)
    return result


def backwards(angle):
    GPIO.output(EN_pin,GPIO.LOW) 
    mymotortest.motor_go(True, "1/16" , angleToSteps(angle), .0005, False, .05)


def forward(angle):
    GPIO.output(EN_pin,GPIO.LOW) 
    mymotortest.motor_go(False, "1/16" , angleToSteps(angle), .0005, False, .05)
