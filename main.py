import turtle
import time
import geocoder
import math
import pandas as pd
import movAngle
from pathlib import Path
from datetime import datetime
import ephem
import giroscopio as giro

canv = turtle.Screen()

canv.setup(1280, 640)
canv.setworldcoordinates(-180, -90, 180, 90)
canv.bgpic("images/map.gif")
canv.register_shape("images/sat.gif")

g = geocoder.ipinfo('me')
me_location = g.latlng
turtle.color('red')
turtle.shape("circle")
turtle.shapesize(0.5,0.5,0)
turtle.penup()
turtle.goto(round(me_location[1],0),round(me_location[0],0))
print(me_location)

degrees_per_radian = 180.0 / math.pi
home = ephem.Observer()
home.lon = str(me_location[1])  # +E
home.lat = str(me_location[0])      # +N
home.elevation = 0 # meters
# Always get the latest ISS TLE data from:
# https://www.celestrak.com/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle
issTLE = ephem.readtle('ISS',                
'1 25544U 98067A   22181.17954266  .00008547  00000+0  15879-3 0  9990',
'2 25544  51.6441 272.2417 0004506 314.0546 243.2226 15.49773840347199'
)

# load the world map image
iss = turtle.Turtle()
iss.shape("images/sat.gif")
iss.setheading(45)
iss.color('#ffd000') 
iss.width(5)
iss.penup()
    
    
canvas = canv.getcanvas()  # or, equivalently: turtle.getcanvas()
root = canvas.winfo_toplevel()
def drawSaves():
    turtle.tracer(0, 0)
    source_dir = Path('saves/')
    files = source_dir.iterdir()

    tr = turtle.Turtle()
    tr.up()

    #scr = canv()

    for file in files:
        with file.open('r') as f_input :
            for row in f_input:
                row = row.strip('()\n').split(',')
                x = float(row[1])
                y = float(row[0])
                tr.color('#ffd000') 
                tr.hideturtle()
                tr.width(5)
                tr.goto(x,y)
                tr.speed(15)

                if -179 <= x >= 179:
                    tr.penup()
                else:
                    tr.pendown()
                
            tr.penup()
    turtle.update() 
    
def on_close():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", on_close)
lat = []
lon = []

drawSaves()

running = True


toZero = giro.Azimuth()
print("Moviendo a norte 0 : " , toZero)
movAngle.backwards(toZero)

AzimuthAngle = 0
while running:
    turtle.tracer(0, 0)
    # load the current status of the ISS in real-time
    home.date = datetime.utcnow()
    issTLE.compute(home)
    elevacion = round(issTLE.alt * degrees_per_radian,0)
    azimuth = round(issTLE.az * degrees_per_radian,0)
    print(('elevacion :' , elevacion, 'azimuth:' , azimuth))
    # Extract the ISS location
    x = issTLE.sublong* degrees_per_radian
    y = issTLE.sublat* degrees_per_radian
    # Ouput lon and lat to the terminal
    x = round(float(x),1)
    y = round(float(y),1)
    canv.title("Ubicación Estación Espacial Internacional     " + "   Longitud: " + str(x) + "   Latitud: " + str(y) )
    
    print('longitud: ' , x, 'latitud: ' , y)

    
    try:
        angleAz = float(azimuth)
        angleEl = float(elevacion+90)
        if angleAz <361 and angleEl < 181:
            toMove = round(angleAz - AzimuthAngle,0)
            print( 'nema angulo a mover: ' , toMove)
            if toMove >= 0:
                movAngle.forward(abs(toMove))
                AzimuthAngle = angleAz
                print(AzimuthAngle)
            else:
                movAngle.backwards(abs(toMove))
                AzimuthAngle = angleAz
                print(AzimuthAngle)
                    
            movAngle.setAngle(angleEl)
        else:
            print("Angulos no validos")
    except ValueError:
        print("Solo numeros")
    # Update the ISS location on the map
    iss.goto(x,y)
    if -179 <= x >= 179:
        iss.penup()
    else:
        iss.pendown()    
    
    lat.append(y)
    lon.append(x) 
        
    iss_movement = {
    'latitude':lat,
    'longitude' :lon,
        }
    df = pd.DataFrame(iss_movement)

    # Refresh each 5 seconds
    turtle.update() 
    time.sleep(0.5)
    if not running:
        if len(lat) > 300:
            print("Guardando datos...")
            timestr = time.strftime("%d-%m-%Y %Hh%Mm")
            df.to_csv("saves/"+timestr+".csv",header=False, index=False)
        canv.bye()
        break




info = home.next_pass(issTLE)

print("Rise time: %s azimuth: %s set time: %s " % ((ephem.localtime(info[0])), info[1], (ephem.localtime(info[4]))))