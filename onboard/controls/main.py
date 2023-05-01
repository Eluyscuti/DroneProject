from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil


#Set up option parsing to get connection string
import argparse

from DroneProject.onboard.controls.drone import Drone  

print('Create a new mission (for current location)')
vehicle = Drone()
vehicle.adds_square_mission(vehicle.location.global_frame,50)


# From Copter 3.3 you will be able to take off using a mission item. Plane must take off using a mission item (currently).
vehicle.arm_and_takeoff(10)

print("Starting mission")
# Reset mission set to first (0) waypoint
vehicle.commands.next=0

# Set mode to AUTO to start mission
vehicle.mode = VehicleMode("AUTO")


# Monitor mission. 
# Demonstrates getting and setting the command number 
# Uses distance_to_current_waypoint(), a convenience function for finding the 
#   distance to the next waypoint.


print('Return to launch')
vehicle.mode = VehicleMode("RTL")


#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if vehicle.sitl is not None:
    vehicle.sitl.stop() 