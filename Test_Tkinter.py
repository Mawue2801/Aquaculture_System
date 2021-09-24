from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pandas as pd
import serial
import serial.tools.list_ports
import threading
import time

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

  
# Create Tk object 
window = Tk() 
  
# Set the window title 
window.title('AquaPak')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
app_width=1100
app_height=500
x = (screen_width/2)-(app_width/2)
y = (screen_height/2)-(app_height/2)-20

window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
window.configure(bg='white')
window.resizable(False, False)

# window_menu = Menu(window)
# window.config(menu=window_menu)

# def openSettings():
#     pass

# file_menu = Menu(window_menu,tearoff=0)
# window_menu.add_cascade(label="File",menu=file_menu)
# file_menu.add_command(label="Settings",command=openSettings)
# file_menu.add_separator()
# file_menu.add_command(label="Exit",command=window.quit)




# def Plot():
    # while ser.isOpen():
        # time.sleep(1)
        # # the figure that will contain the plot
        # fig = Figure(figsize = (5, 5),
        #             dpi = 100)
    
        # # adding the subplot
        # plot1 = fig.add_subplot(111)
        # #plot1.set_ylim(0,5)
    
        # # plotting the graph
        # plot1.plot(xList)
    
        # # creating the Tkinter canvas
        # # containing the Matplotlib figure
        # canvas = FigureCanvasTkAgg(fig,
        #                         master = window)  
        # canvas.draw()
        # # placing the canvas on the Tkinter window
        # canvas.get_tk_widget().pack()
        # print(xList)

def Connect():
    global ser
    ports = serial.tools.list_ports.comports()
    for i in ports:
        i = str(i)
        if 'Arduino' in i:
            commPort = i.split(' ')[0]
        if commPort != 'None':
            ser = serial.Serial(commPort,baudrate = 9600, timeout=1)
            print('Connected to ' + commPort)
        else:
            print('Connection Issue!')

    while True:
        while ser.inWaiting() == 0:
            pass
        arduinoString = ser.readline().decode()
        tempText.set(arduinoString)
    # with open("data.txt","w") as f:
    #     f.write("")
    # f.close()

def Start():
    global f
    global xList
    xList = []
    count = 1
    while True:
        while ser.inWaiting() == 0:
            pass
        arduinoString = ser.readline().decode()
        tempText.set(arduinoString)
        # with open("data.txt","a") as f:
        #     f.write(arduinoString)
        #print(arduinoString)
        # try:
        #     xList.append(float(arduinoString))
        # except:
        #     pass
        # count += 1
        # if count > 11:
        #     xList.pop(0)

def Disconnect():
    ser.close()
    doText.set("")
    tempText.set("")
    pHText.set("")
    waterLevelText.set("")
    #f.close()
    # print(xList)

def turnOnLED():
    text = 'O'
    ser.write(text.encode())

def turnOffLED(): 
    text = 'o'
    ser.write(text.encode())

def changeOnHover(widget, colorOnHover, colorOnLeave):
    # adjusting backgroung of the widget
    # background on entering widget
    widget.bind("<Enter>", func=lambda e: widget.config(highlightbackground=colorOnHover))
    
    # background color on leving widget
    widget.bind("<Leave>", func=lambda e: widget.config(highlightbackground=colorOnLeave))

def round_rectangle(canvas,x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


canvas1 = tk.Canvas(window,background='white',highlightbackground='white',highlightcolor='white')
canvas1.place(x=250,y=10,width=500,height=500)
rectangle1 = round_rectangle(canvas1,5, 5, 195, 195, radius=50, fill="#e0f4ff")
titleRectangle1 = round_rectangle(canvas1,7, 7, 193, 70, radius=50, fill="white")
mainRectangle1 = round_rectangle(canvas1,5, 50, 195, 195, radius=50, fill="#e0f4ff")
doLabel = tk.Label(canvas1,text="Dissolved Oxygen",font=('Montserrat',12),bg='white')
doLabel.place(x=28,y=20)

doText = tk.StringVar()
# doText.set("4.95")
doDisplay = tk.Label(canvas1,textvariable=doText,font=('Montserrat',50),bg='#e0f4ff',fg='#5c5c5c')
doDisplay.place(x=25,y=60)


canvas2 = tk.Canvas(window,background='white',highlightbackground='white',highlightcolor='white')
canvas2.place(x=460,y=10,width=500,height=500)
rectangle2 = round_rectangle(canvas2,5, 5, 195, 195, radius=50, fill="#e0f4ff")
titleRectangle2 = round_rectangle(canvas2,7, 7, 193, 70, radius=50, fill="white")
mainRectangle2 = round_rectangle(canvas2,5, 50, 195, 195, radius=50, fill="#e0f4ff")
tempLabel = tk.Label(canvas2,text="Temperature",font=('Montserrat',12),bg='white')
tempLabel.place(x=45,y=20)

tempText = tk.StringVar()
# tempText.set("4.95")
tempDisplay = tk.Label(canvas2,textvariable=tempText,font=('Montserrat',50),bg='#e0f4ff',fg='#5c5c5c')
tempDisplay.place(x=25,y=60)


canvas3 = tk.Canvas(window,background='white',highlightbackground='white',highlightcolor='white')
canvas3.place(x=670,y=10,width=500,height=500)
rectangle3 = round_rectangle(canvas3,5, 5, 195, 195, radius=50, fill="#e0f4ff")
titleRectangle3 = round_rectangle(canvas3,7, 7, 193, 70, radius=50, fill="white")
mainRectangle3 = round_rectangle(canvas3,5, 50, 195, 195, radius=50, fill="#e0f4ff")
pHLabel = tk.Label(canvas3,text="pH",font=('Montserrat',12),bg='white')
pHLabel.place(x=85,y=20)

pHText = tk.StringVar()
# pHText.set("4.95")
pHDisplay = tk.Label(canvas3,textvariable=pHText,font=('Montserrat',50),bg='#e0f4ff',fg='#5c5c5c')
pHDisplay.place(x=25,y=60)


canvas4 = tk.Canvas(window,background='white',highlightbackground='white',highlightcolor='white')
canvas4.place(x=880,y=10,width=500,height=500)
rectangle4 = round_rectangle(canvas4,5, 5, 195, 195, radius=50, fill="#e0f4ff")
titleRectangle4 = round_rectangle(canvas4,7, 7, 193, 70, radius=50, fill="white")
mainRectangle4 = round_rectangle(canvas4,5, 50, 195, 195, radius=50, fill="#e0f4ff")
waterlevelLabel = tk.Label(canvas4,text="Water Level",font=('Montserrat',12),bg='white')
waterlevelLabel.place(x=50,y=20)

waterLevelText = tk.StringVar()
# waterLevelText.set("4.95")
waterLevelDisplay = tk.Label(canvas4,textvariable=waterLevelText,font=('Montserrat',50),bg='#e0f4ff',fg='#5c5c5c')
waterLevelDisplay.place(x=25,y=60)


background = tk.Canvas(window,background='white',highlightbackground='white',highlightcolor='white')
background.place(x=0,y=205,width=app_width,height=app_height-300)

controlsFrame = tk.LabelFrame(window,text="Controls",bg='white')
controlsFrame.place(x=15,y=20)

connect_button = tk.Button(controlsFrame,text='Connect',width=25,command=lambda:threading.Thread(target=Connect).start())
connect_button.grid(row=0,column=1,padx=17,pady=26)

disconnect_button = tk.Button(controlsFrame,text='Disconnect',width=25,command=lambda:threading.Thread(target=Disconnect).start())
disconnect_button.grid(row=1,column=1,pady=26)



thresholdsFrame = tk.LabelFrame(window,text="Thresholds",bg='white')
thresholdsFrame.place(x=15,y=220)

tempThresholdLabel = tk.Label(thresholdsFrame, text="Temperature",font=('Arial',8,'bold'),bg='white')
tempThresholdLabel.grid(row=0,column=0,padx=5,pady=15)

tempMinLabel = tk.Label(thresholdsFrame, text="Min",font=('Arial',8),bg='white')
tempMinLabel.grid(row=0,column=1,padx=5,pady=15)

tempMinEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1")
tempMinEntry.grid(row=0,column=2,padx=15)

tempMaxLabel = tk.Label(thresholdsFrame, text="Max",font=('Arial',8),bg='white')
tempMaxLabel.grid(row=0,column=3,padx=5,pady=15)

tempMaxEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1")
tempMaxEntry.grid(row=0,column=4,padx=15)



doThresholdLabel = tk.Label(thresholdsFrame, text="Dissolved Oxygen",font=('Arial',8,'bold'),bg='white')
doThresholdLabel.grid(row=1,column=0,padx=5,pady=15)

doMinLabel = tk.Label(thresholdsFrame, text="Min",font=('Arial',8),bg='white')
doMinLabel.grid(row=1,column=1,padx=5,pady=15)

doMinEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1")
doMinEntry.grid(row=1,column=2,padx=15)

doMaxLabel = tk.Label(thresholdsFrame, text="Max",font=('Arial',8),bg='white')
doMaxLabel.grid(row=1,column=3,padx=5,pady=15)

doMaxEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1")
doMaxEntry.grid(row=1,column=4,padx=15)


pHThresholdLabel = tk.Label(thresholdsFrame, text="pH",font=('Arial',8,'bold'),bg='white')
pHThresholdLabel.grid(row=2,column=0,padx=5,pady=15)

pHMinLabel = tk.Label(thresholdsFrame, text="Min",font=('Arial',8),bg='white')
pHMinLabel.grid(row=2,column=1,padx=5,pady=15)

pHMinEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1")
pHMinEntry.grid(row=2,column=2,padx=15)

pHMaxLabel = tk.Label(thresholdsFrame, text="Max",font=('Arial',8),bg='white')
pHMaxLabel.grid(row=2,column=3,padx=5,pady=15)

pHMaxEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1")
pHMaxEntry.grid(row=2,column=4,padx=15)



fishWeightLabel = tk.Label(thresholdsFrame, text="Fish Weight",font=('Arial',8,'bold'),bg='white')
fishWeightLabel.grid(row=3,column=0,padx=5,pady=15)

fishWeightEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1",width=55)
fishWeightEntry.grid(row=3,column=1,padx=5,columnspan=4)



waterChangeLabel = tk.Label(thresholdsFrame, text="% Water Change",font=('Arial',8,'bold'),bg='white')
waterChangeLabel.grid(row=4,column=0,padx=5,pady=15)

waterChangeEntry = Entry(thresholdsFrame,highlightthickness=2,borderwidth=0,highlightcolor= "#2696FF",highlightbackground="#D1D1D1",width=55)
waterChangeEntry.grid(row=4,column=1,padx=5,columnspan=4)




window.mainloop()