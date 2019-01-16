#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RCLK  = 11
SRCLK = 12
SDI   = 13

#left reg controlls row
#right reg controlls column

#data fed right->left

#code_H = [0x01,0xff,0x80,0xff,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
#code_L = [0x00,0x7f,0x00,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xfe,0xfd,0xfb,0xf7,0xef,0xdf,0xbf,0x7f]

cTab = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
vTab = [0xfe, 0xfd, 0xfb, 0xf7, 0xef, 0xdf, 0xbf, 0x7f]

c =    [0x00, 0x00, 0xfc, 0xfc, 0xfc, 0xfc, 0x00, 0x00]
s =    [0x00, 0x00, 0xfc, 0x00, 0x00, 0x3f, 0x00, 0x00]
r =    [0b11000000, 0b11000000, 0b00111100, 0b00111100, 0b11000000, 0b11000000, 0b00111100, 0b00111100]

blank = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
grid = [0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101]

flashDelay = 0.0005

def print_msg():
        print( 'Program is running...')
        print( 'Please press Ctrl+C to end the program...')

def setup():
        GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
        GPIO.setup(SDI, GPIO.OUT)
        GPIO.setup(RCLK, GPIO.OUT)
        GPIO.setup(SRCLK, GPIO.OUT)
        GPIO.output(SDI, GPIO.LOW)
        GPIO.output(RCLK, GPIO.LOW)
        GPIO.output(SRCLK, GPIO.LOW)

def hc595_in(dat):
        for bit in range(0, 8): 
                GPIO.output(SDI, 0x80 & (dat << bit))
                GPIO.output(SRCLK, GPIO.HIGH)
                #time.sleep(0.00001)
                GPIO.output(SRCLK, GPIO.LOW)

def hc595_out():
        GPIO.output(RCLK, GPIO.HIGH)
        #time.sleep(0.001)
        GPIO.output(RCLK, GPIO.LOW)

def showChar(char, sec):
    duration = int(sec / flashDelay) #not actually accurate
    #print(duration)
    
    for i in range(duration):
        for j in range(0, len(char)):
            hc595_in(cTab[j])
            hc595_in(char[j])
            hc595_out()
        time.sleep(flashDelay)
        
def dotScan(delay):
    for i in range(8):
        for j in range(8):
            hc595_in(cTab[i])
            hc595_in(vTab[j])
            hc595_out()
            time.sleep(delay)
            
def sccrc(delay, blankDelay):
    showChar(s, delay)
    showChar(blank, blankDelay)
                
    showChar(c, delay)
    showChar(blank, blankDelay)
                
    showChar(c, delay)
    showChar(blank, blankDelay)
                
    showChar(r, delay)
    showChar(blank, blankDelay)
                
    showChar(c, delay)
    showChar(blank, blankDelay)
    
    showChar(grid, 0.3)
    showChar(blank, 0.1)
                

def loop():
    while True:
        dotScan(0.05)
        sccrc(0.3, 0.05)
        time.sleep(0.1)

def destroy():   # When program ending, the function is executed. 
        GPIO.cleanup()

if __name__ == '__main__':   # Program starting from here 
        print_msg()
        setup() 
        try:
                loop()  
        except KeyboardInterrupt:  
                destroy()  
