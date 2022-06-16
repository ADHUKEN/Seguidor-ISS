from logging import root
import turtle
import time
import geocoder
import ISS_Info
import pandas as pd
from pathlib import Path
import sys




screen = turtle.Screen()

screen.setup(1280, 640)
screen.setworldcoordinates(-180, -90, 180, 90)

g = geocoder.ipinfo('me')
me_location = g.latlng
print(me_location)
turtle.color('red')
turtle.shape("circle")
turtle.shapesize(0.5,0.5,0)
turtle.penup()
turtle.goto(round(me_location[1],0),round(me_location[0],0))



# load the world map image
screen.bgpic("map.gif")
screen.register_shape("sat.gif")
iss = turtle.Turtle()
iss.shape("sat.gif")
iss.setheading(45)
iss.color('#ffd000') 
iss.width(5)
iss.penup()
    
    
canvas = screen.getcanvas()  # or, equivalently: turtle.getcanvas()
root = canvas.winfo_toplevel()
def drawSaves():
    turtle.tracer(0, 0)
    source_dir = Path('saves/')
    files = source_dir.iterdir()

    tr = turtle.Turtle()
    tr.up()

    #scr = Screen()

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
while running:
    turtle.tracer(0, 0)
    # load the current status of the ISS in real-time
    iss_location = ISS_Info.iss_current_loc()     # Returns a dictionary with latitude, longitude, timestamp.


    # Extract the ISS location
    x = iss_location.get("iss_position").get("longitude")
    y = iss_location.get("iss_position").get("latitude")

    # Ouput lon and lat to the terminal
    x = round(float(x),1)
    y = round(float(y),1)
    screen.title("Ubicación Estación Espacial Internacional     " + "   Longitud: " + str(x) + "   Latitud: " + str(y) )
    print(iss_location.get("iss_position"), y , x)

    # Update the ISS location on the map
    iss.goto(x,y)
    iss.pendown()
    
    lat.append(y)
    lon.append(x)
    # elimina los duplicados al guardar en csv
    latSave = []
    [latSave.append(i) for i in lat if i not in latSave]
    
    lonSave = []
    [lonSave.append(i) for i in lon if i not in lonSave]
        
    iss_movement = {
    'latitude':lat,
    'longitude' :lon,
          }
    df = pd.DataFrame(iss_movement)

    # Refresh each 5 seconds
    turtle.update() 
    time.sleep(0.09)
    if not running:
        if len(lonSave) > 50:
            print("Guardando datos...")
            timestr = time.strftime("%d-%m-%Y %Hh%Mm")
            df.to_csv("saves/"+timestr+".csv",header=False, index=False)
        break
