#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import numpy as np

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(10)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

#home koordinaları için uçağın anlık koordinatlarını al
#lon: boylam lat: enlem
#equ --> lon/lat x/y dönüşümü


lat_home =47.3977508
lon_home=85.456078

#------------------------------------------------------------------------------------------#
#-------------------------------- İLK DÜZLÜK ----------------------------------------------#
#------------------------------------------------------------------------------------------#

current_lat=lat_home
current_lon=lon_home

mission_distance=30

mission_distance_lon = (0.0011782*mission_distance)/100

max_lon_home = current_lon + mission_distance_lon

print("target location:",current_lat,max_lon_home)



while current_lon < max_lon_home:

    point1 = LocationGlobalRelative(current_lat, current_lon, 10)
    vehicle.simple_goto(point1)
    current_lon = current_lon + 0.000001
    """
    print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    print("Altitude relative to home_location: %s" % vehicle.location.global_relative_frame.alt)
    print("Local Location: %s" % vehicle.location.local_frame)
    """
    

print("current location:",current_lat,current_lon)


time.sleep(30)




#-------------------------------------------------------------------------------------------#
#--------------------------------- İLK YARIM ÇEMBER ----------------------------------------#
#-------------------------------------------------------------------------------------------#

lat_home = current_lat
lon_home = current_lon

radius=15.0

radius_lon=(0.0011782*radius)/100
radius_lat=(0.0009017*radius)/100

min_lon=lon_home-radius_lon
middle_lon=lon_home
max_lon=lon_home+radius_lon

equ_min_lon=(min_lon * 100)/0.0011782
equ_middle_lon=(middle_lon * 100)/0.0011782
equ_max_lon=(max_lon * 100)/0.0011782



min_lat=lat_home
middle_lat=lat_home+radius_lat
max_lat=middle_lat+radius_lat

equ_min_lat=(min_lat * 100)/0.0009017
equ_middle_lat=(middle_lat * 100)/0.0009017
equ_max_lat=(max_lat * 100)/0.0009017

#bölge 4
current_lat=lat_home
current_lon=lon_home 

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]
while equ_current_lon < equ_max_lon:
    equ_current_lat=equ_min_lat
    
    while equ_current_lat < equ_middle_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            #print("points:",y,x)
            point = LocationGlobalRelative(y,x, 10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon+0.001   


#bölge 1
current_lat=middle_lat
current_lon=max_lon

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon > equ_middle_lon:
    equ_current_lat=equ_middle_lat
    
    while equ_current_lat < equ_max_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            current_lon=(0.0011782*equ_current_lon)/100
            current_lat=(0.0009017*equ_current_lat)/100
            #print("points:",y,x)
            point = LocationGlobalRelative(current_lat,current_lon, 10)
            vehicle.simple_goto(point) 

    
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon-0.001   



#----------------------------------------------------------------------------------------------#
#----------------------------------- İKİNCİ DÜZLÜK --------------------------------------------#
#----------------------------------------------------------------------------------------------#



mission_distance=30

mission_distance_lon = (0.0011782*mission_distance)/100

min_lon_home = current_lon - mission_distance_lon

print("target location:",current_lat,current_lon)

while current_lon > min_lon_home:

    point1 = LocationGlobalRelative(current_lat,current_lon, 10)
    vehicle.simple_goto(point1)
    current_lon = current_lon - 0.000001
    """
    print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    print("Altitude relative to home_location: %s" % vehicle.location.global_relative_frame.alt)
    print("Local Location: %s" % vehicle.location.local_frame)
    """
    print("current location:",current_lat,current_lon)

time.sleep(30)


#---------------------------------------------------------------------------------------------#
#---------------------------------------- TAM ÇEMBER -----------------------------------------#
#---------------------------------------------------------------------------------------------#

#   YÖNÜ TERSİNE ÇEVRİLCEK

lat_home =current_lat
lon_home=current_lon

radius=10.0

radius_lon=(0.0011782*radius)/100
radius_lat=(0.0009017*radius)/100

min_lon=lon_home-radius_lon
middle_lon=lon_home
max_lon=lon_home+radius_lon

equ_min_lon=(min_lon * 100)/0.0011782
equ_middle_lon=(middle_lon * 100)/0.0011782
equ_max_lon=(max_lon * 100)/0.0011782



min_lat=lat_home
middle_lat=lat_home+radius_lat
max_lat=middle_lat+radius_lat

equ_min_lat=(min_lat * 100)/0.0009017
equ_middle_lat=(middle_lat * 100)/0.0009017
equ_max_lat=(max_lat * 100)/0.0009017


#bölge 4
current_lat=lat_home
current_lon=lon_home

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon < equ_max_lon:
    equ_current_lat=equ_min_lat
    
    while equ_current_lat < equ_middle_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            print("points:",y,x)
            point = LocationGlobalRelative(y,x, 10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon+0.001   


#bölge 1
current_lat=middle_lat
current_lon=max_lon

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon > equ_middle_lon:
    equ_current_lat=equ_middle_lat
    
    while equ_current_lat < equ_max_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            print("points:",y,x)
            point = LocationGlobalRelative(y,x, 10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat+0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon-0.001   


#bölge 2
current_lat=max_lat
current_lon=middle_lon

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon > equ_min_lon:
    equ_current_lat=equ_max_lat
    
    while equ_current_lat > equ_middle_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            print("points:",y,x)
            point = LocationGlobalRelative(y,x,10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon-0.001   


#bölge 3
current_lat=middle_lat
current_lon=min_lon

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon < equ_middle_lon:
    equ_current_lat=equ_middle_lat
    
    while equ_current_lat > equ_min_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            print("points:",y,x)
            point = LocationGlobalRelative(y,x, 10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon+0.001   


#-------------------------------------------------------------------------------------------#
#-------------------------------- ÜÇÜNCÜ DÜZLÜK --------------------------------------------#
#-------------------------------------------------------------------------------------------#

current_lat=lat_home
current_lon=lon_home

mission_distance=30

mission_distance_lon = (0.0011782*mission_distance)/100

min_lon_home = current_lon - mission_distance_lon

print("target location:",current_lat,current_lon)

while current_lon > min_lon_home:

    point1 = LocationGlobalRelative(current_lat,current_lon, 10)
    vehicle.simple_goto(point1)
    current_lon = current_lon - 0.000001
    """
    print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    print("Altitude relative to home_location: %s" % vehicle.location.global_relative_frame.alt)
    print("Local Location: %s" % vehicle.location.local_frame)
    """
    print("current location:",current_lat,current_lon)

time.sleep(30)


#-------------------------------------------------------------------------------------------#
#---------------------------- İKİNCİ YARIM ÇEMBER ------------------------------------------#
#-------------------------------------------------------------------------------------------#



radius=15.0

radius_lon=(0.0011782*radius)/100
radius_lat=(0.0009017*radius)/100

lat_home = current_lat - 2*radius_lat
lon_home = current_lon

min_lon=lon_home-radius_lon
middle_lon=lon_home
max_lon=lon_home+radius_lon

equ_min_lon=(min_lon * 100)/0.0011782
equ_middle_lon=(middle_lon * 100)/0.0011782
equ_max_lon=(max_lon * 100)/0.0011782



min_lat=lat_home
middle_lat=lat_home+radius_lat
max_lat=middle_lat+radius_lat

equ_min_lat=(min_lat * 100)/0.0009017
equ_middle_lat=(middle_lat * 100)/0.0009017
equ_max_lat=(max_lat * 100)/0.0009017



#bölge 2

current_lat=max_lat
current_lon=middle_lon

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon > equ_min_lon:
    equ_current_lat=equ_max_lat
    
    while equ_current_lat > equ_middle_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            print("points:",y,x)
            point = LocationGlobalRelative(y,x, 10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon-0.001   


#bölge 3
current_lat=middle_lat
current_lon=min_lon

equ_current_lon= (current_lon * 100)/0.0011782
equ_current_lat= (current_lat * 100)/0.0009017


pointsx=[]
pointsy=[]

while equ_current_lon < equ_middle_lon:
    equ_current_lat=equ_middle_lat
    
    while equ_current_lat > equ_min_lat:
        equ=(equ_current_lon-equ_middle_lon)**2+(equ_current_lat-equ_middle_lat)**2
        
        #print("current:",equ)
        if ((radius**2)-0.0001000000)<equ<((radius**2)+0.0001000000):
            pointsx.append(equ_current_lon)
            pointsy.append(equ_current_lat)
            #print("kareler:",equ_current_lon-equ_middle_lon,equ_current_lat-equ_middle_lat)
            x=(0.0011782*equ_current_lon)/100
            y=(0.0009017*equ_current_lat)/100
            print("points:",y,x)
            point = LocationGlobalRelative(y,x, 10)
            vehicle.simple_goto(point) 

          
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü1:",equ_current_lat-equ_middle_lat,equ_current_lon-equ_middle_lon)
        else:
     
            equ_current_lat=equ_current_lat-0.001
            #print("iç döngü2:",current_lat,current_lon)

    #print("dıs döngü:",current_lat,current_lon)
    equ_current_lon=equ_current_lon+0.001   


"""

#---------------------------------------------------------------------------------------------#
#--------------------------------- DÖRDÜNCÜ DÜZLÜK -------------------------------------------#
#---------------------------------------------------------------------------------------------#

mission_distance=30

mission_distance_lon = (0.0011782*mission_distance)/100

max_lon_home = current_lon + mission_distance_lon

print("target location:",current_lat,max_lon_home)



while current_lon < max_lon_home:

    point1 = LocationGlobalRelative(current_lat, current_lon, 10)
    vehicle.simple_goto(point1)
    current_lon = current_lon + 0.000001

    #print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    #print("Altitude relative to home_location: %s" % vehicle.location.global_relative_frame.alt)
    #print("Local Location: %s" % vehicle.location.local_frame)
    
    

print("current location:",current_lat,current_lon)


time.sleep(30)

"""





print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()

