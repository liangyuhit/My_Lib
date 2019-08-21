import serial
#import time

def getLaser(port_name):
    ser = serial.Serial( 
                  port =port_name,
                    baudrate=9600,
#                     baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=1,
                    bytesize=8,
                    xonxoff = 0
                  )

    #set timeout for readline
    ser.timeout = 1
    return ser