# SPDX-FileCopyrightText: 2019 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import random
import turtle
import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import math

i2c = busio.I2C(board.SCL, board.SDA)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

def Azimuth():
    mag_x, mag_y, mag_z = mag.magnetic
    AZCompass = round(math.degrees(math.atan2(mag_y,mag_x)),2)
    if AZCompass < 0:
        AZCompass += 360
    return AZCompass

def Elevation():
    accel_x, accel_y, accel_z = accel.acceleration
    ELCompass =  round(math.degrees(math.atan2(math.sqrt(math.pow(accel_x,2)+math.pow(accel_y,2)),accel_z)),2)
    return ELCompass

def giro():




    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.setworldcoordinates(-20, -20, 20, 20)
    screen.bgpic("images/brujula.gif")

    arrow = turtle.Turtle()
    arrow.shape("classic")
    arrow.setheading(45)
    arrow.color('red')
    arrow.turtlesize(4,9,1) 
    arrow.width(10)
    arrow.penup()

    arrowElevation = turtle.Turtle()
    arrowElevation.shape("classic")
    arrowElevation.setheading(45)
    arrowElevation.color('blue')
    arrowElevation.turtlesize(4,9,1) 
    arrowElevation.width(10)
    arrowElevation.penup()
        
        
    canvas = screen.getcanvas()  # or, equivalently: turtle.getcanvas()
    root = canvas.winfo_toplevel()

    def on_close():
        global running
        running = False
    root.protocol("WM_DELETE_WINDOW", on_close)



        

    running = True
    while running:
        

            
        turtle.tracer(0, 0)

        arrow.seth(90-Azimuth())
        arrow.penup()
        arrow.forward(14)
        
        arrowElevation.seth(90-Elevation())
        arrowElevation.penup()
        arrowElevation.forward(20)
        turtle.update()
        
        
        arrow.home()
        arrow.clear() 
        arrowElevation.home()
        arrowElevation.clear() 
            
        screen.title("[Rojo] Azimuth: " +  str(Azimuth()) +  "   [Azul] Elevacion: " + str(Elevation()) )


        print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
        print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)
        print("AZIMUTH = " , Azimuth())
        print("ELEVACION = " , Elevation()) 
        print("")
        time.sleep(0.05)
        if not running:
            screen.bye()
            break