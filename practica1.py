import RPi.GPIO as GPIO
import time

servoPIN = 18
coil_A_1_pin = 4
coil_A_2_pin = 17 
coil_B_1_pin = 27 
coil_B_2_pin = 22 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) 
p.start(2.5) 

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

def setAngle(angle):
    duty = (angle / 18) + 2
    p.ChangeDutyCycle(duty)
    time.sleep(0.4)
    p.ChangeDutyCycle(0)

StepCount = 8
Seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]


def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

def angleToSteps(angle):
    steps = 512
    result = int((angle*steps)/360)
    return result

def forward(angle):
    for i in range(angleToSteps(angle)):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(0.001)
    

def backwards(angle):
    for i in range(angleToSteps(angle)):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(0.001)


    
if __name__ == '__main__':
    AzimuthAngle = 0
    while True:

        try:
            angleAz = int (input("Angulo Azimuth: "))
            angleEl = int(input("Angulo de Elevación: "))
            if angleAz <361 and angleEl < 181:
                toMove = angleAz - AzimuthAngle
                print(toMove)
                if toMove >= 0:
                    forward(abs(toMove))
                    AzimuthAngle = angleAz
                    print(AzimuthAngle)
                else:
                    backwards(abs(toMove))
                    AzimuthAngle = angleAz
                    print(AzimuthAngle)
                    
                setAngle(angleEl)
            else:
                print("Angulos no validos")
        except ValueError:
            print("Solo numeros")
            
