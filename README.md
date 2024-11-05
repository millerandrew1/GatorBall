# GatorBall
Sprint 1 10-8-2024 to 10-25-2024:
Work Completed: 
  This sprint we focuses on the front end of our design. We worked on showing dummy data and making the program that the referee will be using when determining the position of the football. We created a client that would act as our "football" and that would connect to a server and send dummy data which represents the distance from the anchor points. Then we have a python script called ble_triangulate.py that does the calculation of the exact position of the client and then we output that to our UI which displays the data. 

  We received our ESP-32 and DW3000 on Thursday the day before the Pre-Alpha was due so we did not have time to write a lot of code but we did have resources that we previously found and used that code to test our microchips. We were successfully able to send and receive data between the two chips and the data was the distance between the two microchips. In the future we will add the third DW3000 which will act as the football and it will take in the distance between the two microchips and then it will send that data to the ble_triangulate to calculate the position of the ball.


DEPENDENCIES

Bleak BLE - https://github.com/hbldh/bleak 
Localization - https://github.com/kamalshadi/Localization
Localization dependency (may not be needed) - https://shapely.readthedocs.io/en/stable/

Installation commands
pip install localization
pip install bleak
pip install shapely
