# import streamlit as st
import pandas as pd
import serial
import serial.tools.list_ports
import time

def get_ports():

    ports = serial.tools.list_ports.comports()
    
    return ports

def findArduino(portsFound):
    
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        
        if 'Arduino' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort
            
                    
foundPorts = get_ports()        
connectPort = findArduino(foundPorts)

if connectPort != 'None':
    ser = serial.Serial(connectPort,baudrate = 9600, timeout=1)
    print('Connected to ' + connectPort)

else:
    print('Connection Issue!')
# col1,col2,col3 = st.columns(3)
while True:
    while ser.inWaiting() == 0:
        pass
    arduinoString = ser.readline().decode()
    print(arduinoString)
    # with open("Data.csv", "a") as f:
    #     f.write(arduinoString)

    # df = pd.read_csv("Data.csv")
    # col2.line_chart(df)