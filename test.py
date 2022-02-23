# potentiometer.py

from os import read
import serial
import time
import csv
from datetime import datetime
import time


# make sure the 'COM#' is set according the Windows Device Manager

#
# Use Canvas to create a basic gauge
#
from tkinter import *

ser = serial.Serial('COM3', 9800, timeout=1)
time.sleep(2)
old_sensorvalue = -31
kuppeja_keitetty = 0
data = []
running = True
data_source = None
with open('data.csv', 'r') as file:
    data_source = file.read()  

def update():
    with open("data.csv","r") as f:
        data = f.read()
        text_widget.delete("1.0", "end")
        text_widget.insert(END ,data)
    text_widget.after(1000, update)

def update_gauge():
    global data_source
    with open('data.csv', 'r') as file:
        data_source = file.read()  
    global running
    if running == True :

        f = open('C:/Users/jope1/Desktop/Koulu dokkarit/IoT/data.csv', 'a')
        writer = csv.writer(f, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        global data
        global old_sensorvalue
        global kuppeja_keitetty
        now = datetime.now()  #

        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        line = ser.readline()   # read a byte
        if line:
            print(old_sensorvalue)
            sensorvalue = line.decode()  # convert the byte string to int
            print(sensorvalue)
            if int(sensorvalue) == int(old_sensorvalue) or int(sensorvalue) < int(old_sensorvalue+30):
                print("testi")

                writer.writerow(data)
                update()
                f.close()
                
                running = False
                
            elif int(sensorvalue) > 590 and int(sensorvalue) < 630:
                # Sensori arvo ylittää raja-arvon -> kirjataan excel tiedostoon
                old_sensorvalue = int(sensorvalue)
                data.append("Kuppi keitetty " + date_time)
                kuppeja_keitetty = 1 
                print(data)

            elif int(sensorvalue) > 631 and int(sensorvalue) < 680:
                # Sensori arvo ylittää raja-arvon -> kirjataan excel tiedostoon
                old_sensorvalue = int(sensorvalue)
                data = []
                data.append("Kaksi kuppia keitetty " + date_time)
                kuppeja_keitetty = 2
                print(data)

            elif int(sensorvalue) > 681 and int(sensorvalue) < 740:
                # Sensori arvo ylittää raja-arvon -> kirjataan excel tiedostoon
                old_sensorvalue = int(sensorvalue)
                data = []
                data.append("Kolme kuppia keitetty " + date_time)
                kuppeja_keitetty = 3
                print(data)

            elif int(sensorvalue) > 741 :
                # Sensori arvo ylittää raja-arvon -> kirjataan excel tiedostoon
                old_sensorvalue = int(sensorvalue)
                data = []
                data.append("Neljä kuppia keitetty " + date_time)
                kuppeja_keitetty = 4
                print(data)
    
    newvalue = kuppeja_keitetty
    cnvs.itemconfig(id_text, text=str(newvalue) + " kuppia")
    # Rescale value to angle range (0%=120deg, 100%=30 deg)
    angle = 180 * (hi_r - newvalue)/(hi_r - low_r)
    cnvs.itemconfig(id_needle, start=angle)


    root.after(30000, update_gauge)

 # Create Canvas objects


canvas_width = 360
canvas_height = 300

root = Tk()

cnvs = Canvas(root, width=canvas_width, height=canvas_height)
cnvs.pack()

coord = 10, 50, 350, 350  # define the size of the gauge
low_r = 0  # chart low range
hi_r = 4  # chart hi range

# Create a background arc and a pointer (very narrow arc)
cnvs.create_arc(coord, start=0, extent=180, fill="green", width=2)
id_needle = cnvs.create_arc(coord, start=180, extent=1, width=8)

# Add some labels
cnvs.create_text(180, 20, font="Times 20 italic bold", text="Kahvimaisteri")
cnvs.create_text(15, 220, font="Times 12 bold", text=low_r)
cnvs.create_text(350, 220, font="Times 12 bold", text=hi_r)
id_text = cnvs.create_text(175, 220, font="Times 15 bold")

text_widget = Text(root, width=250, height=40)
 
text_widget.insert(1.0, data_source)
text_widget.pack()

root.after(3000, update_gauge)
root.mainloop()

ser.close()






