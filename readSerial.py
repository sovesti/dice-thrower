import serial
import os

ser = serial.Serial('COM3')
while(1):
    serialData = ser.readline()
    print(serialData)
    if(b"TIME_TO_TAKE_A_PICTURE" in serialData):
        os.system("python takePhoto.py")
ser.close()