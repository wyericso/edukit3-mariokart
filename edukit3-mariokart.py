#!/usr/bin/python

# Code is based on:
################################################################################
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# wii_remote_1.py
# Connect a Nintendo Wii Remote via Bluetooth
# and  read the button states in Python.
#
# Project URL :
# http://www.raspberrypi-spy.co.uk/?p=1101
#
# Author : Matt Hawkins
# Date   : 30/01/2013
################################################################################
#
# It is modified to control CamJam EduKit 3 in Mario Kart Style.

# -----------------------
# Import required Python libraries
# -----------------------
import cwiid
import time
from gpiozero import CamJamKitRobot    # Import the GPIO Zero Library CamJam library
import math                            # Import for cosine calculation

button_delay = 0.1
# Left most tilt value returned from wiimote,
# when it is 90 degrees to the left.
lmv = 160
# Right most tilt value returned from wiimote,
# when it is 90 degrees to the right.
rmv = 105
# levelv = (lmv + rmv) / 2    # Level value
# halfrange = (lmv - rmv) / 2
levelv = 132.5    # Level value
halfrange = 27.5
robot = CamJamKitRobot()

print 'Press 1 + 2 on your Wii Remote now ...'
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Error opening wiimote connection"
  quit()

print 'Wii Remote connected...\n'
wii.rumble = 1
time.sleep(0.3)
wii.rumble = 0
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

while True:

  buttons = wii.state['buttons']

  # If Plus and Minus buttons pressed
  # together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
    print '\nClosing connection ...'
    wii.rumble = 1
    time.sleep(0.3)
    wii.rumble = 0
    exit(wii)  
  
  # Check if other buttons are pressed by
  # doing a bitwise AND of the buttons number
  # and the predefined constant for that button.
  if (buttons & cwiid.BTN_LEFT):
    print 'Left pressed'
    time.sleep(button_delay)         

  elif(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    time.sleep(button_delay)          

  elif (buttons & cwiid.BTN_UP):
    print 'Up pressed'        
    time.sleep(button_delay)          
    
  elif (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'      
    time.sleep(button_delay)  
    
  elif (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    tilt = wii.state['acc'][1]    # Get wiiremote tilt value.
    print tilt
    print -math.cos(math.radians((tilt - levelv) / halfrange * 90))
    
    if (tilt < levelv):           # Turning right.
      # robot.value = (left motor speed, right motor speed)
      robot.value = (-1, -math.cos(math.radians((tilt - levelv) / halfrange * 90)))
    else:                         # Turning left.
      robot.value = (-math.cos(math.radians((tilt - levelv) / halfrange * 90)), -1)
    time.sleep(button_delay)          

  elif (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    tilt = wii.state['acc'][1]    # Get wiiremote tilt value.
    print tilt
    print math.cos(math.radians((tilt - levelv) / halfrange * 90))

    if (tilt < levelv):           # Turning right.
      # robot.value = (left motor speed, right motor speed)
      robot.value = (1, math.cos(math.radians((tilt - levelv) / halfrange * 90)))
    else:                         # Turning left.
      robot.value = (math.cos(math.radians((tilt - levelv) / halfrange * 90)), 1)
    time.sleep(button_delay)          

  elif (buttons & cwiid.BTN_A):
    print 'Button A pressed'
    time.sleep(button_delay)          

  elif (buttons & cwiid.BTN_B):
    print 'Button B pressed'
    time.sleep(button_delay)          

  elif (buttons & cwiid.BTN_HOME):
    print 'Home Button pressed'
    time.sleep(button_delay)           
    
  elif (buttons & cwiid.BTN_MINUS):
    print 'Minus Button pressed'
    time.sleep(button_delay)   
    
  elif (buttons & cwiid.BTN_PLUS):
    print 'Plus Button pressed'
    time.sleep(button_delay)
    
  else:
    robot.value = (0, 0)