# GatorBall
Sprint 1 10-8-2024 to 10-25-2024:
Work Completed: 
  This sprint we focuses on the front end of our design. We worked on showing dummy data and making the program that the referee will be using when determining the position of the football. We created a client that would act as our "football" and that would connect to a server and send dummy data which represents the distance from the anchor points. Then we have a python script called ble_triangulate.py that does the calculation of the exact position of the client and then we output that to our UI which displays the data. 

  We also wrote code for our ESP-32 and the DW3000 that uses Ultra Wide Band technology to track positioning using anchor points. However, we were unable to test it due to the fact that the shipping is taking longer than expected. 


DEPENDENCIES

Bleak BLE - https://github.com/hbldh/bleak 
Localization - https://github.com/kamalshadi/Localization
Localization dependency (may not be needed) - https://shapely.readthedocs.io/en/stable/

Installation commands
pip install localization
pip install bleak
pip install shapely
