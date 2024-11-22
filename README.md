# GatorBall
Sprint 1 10-8-2024 to 10-25-2024:
Work Completed: 
  This sprint we focuses on the front end of our design. We worked on showing dummy data and making the program that the referee will be using when determining the position of the football. We created a client that would act as our "football" and that would connect to a server and send dummy data which represents the distance from the anchor points. Then we have a python script called ble_triangulate.py that does the calculation of the exact position of the client and then we output that to our UI which displays the data. 

  We received our ESP-32 and DW3000 on Thursday the day before the Pre-Alpha was due so we did not have time to write a lot of code but we did have resources that we previously found and used that code to test our microchips. We were successfully able to send and receive data between the two chips and the data was the distance between the two microchips. In the future we will add the third DW3000 which will act as the football and it will take in the distance between the two microchips and then it will send that data to the ble_triangulate to calculate the position of the ball.

Sprint 2 10-26-2024 to 11-22-2024
This sprint we focued on getting the data from our tag to print to the UI. We tried to use another DW3000 to be the football but due to issues with Ardunio and there not being a compatible library we are sticking with the 1 anchor point and 1 tag for the prototype. The tag takes data from the anchor point through UWB and then is connected through bluetooth to our UI using a COM Port where we display the distance from the tag from the anchor point on the football field. We also have it continuously send data through the bluetooth so that every few miliseconds it gets new data and updates the UI. Also when the tag moves it is shown on the UI as a football moving on the field. 

Future plans for next sprint involve trying to incorporate a second anchor point so we can get a 2D position field instead of the 1D field we have now. We also need to make a PCB with the DW3000 and the ESP-32 along with including a power source. This will then need to be incorporated into a football. We also plan on transferring our python UI into a react application in order to make the project accessable for apps to be able to use it. Along with that we want to make our UI more interactable which will take in more inputs like line of scrimmage, first down line, and other various things involved in a football game (score, team names, clock time). We also have a football moving on the screen but we want to be able to visually show the line of scrimmage and the first down line.  


PROCESS FOR RUNNING CODE AND CONNECTING BLUETOOTH TO PC

First go to src/hardware/range_rx and upload that Arduino code to one of the DW3000 ESP 32 modules. That is now the tag. Then in src/hardware/range_tx upload that to the other one and that is your anchor point. They should now be sending data to each other and the tag should be serial printing the distance. To connect the tag to the bluetooth go to bluetooth settings and scroll down and click devices then in there click more bluetooth settings. In there click the tab that says COM PORTS and click add and add the ESP_32. Take note of what COM Port it is connected to. Finally go to src/FrontEnd/ui.py. Change line 44 to reflect what COM port the bluetooth is transmitting through. Then run the UI and you should see data printing to the UI.

BUGS

Bluetooth and UWB, like many other wireless protocols, are finicky. Throughout our design process, we have encountered many situations where connecting to the ESP32 tag that we will be putting into a football over Bluetooth has been unreliable and difficult to get working at times. Furthermore, after testing the UWB capabilities of the DWM3000 modules, we’ve discovered that it is prone to interference from physical obstructions like walls and even people as the transmission of data is impeded by these effects. Our workaround to these issues for the purpose of the prototype has been to disconnect and reconnect to the Bluetooth device as well as maintaining “line of sight” for the two ESP32s communicating over UWB. Also, we check to ensure that the data we are receiving is of the valid format (i.e., a numerical float value). We have determined that at this time, so long as the proper preparations have been made, there is currently no need for any other error correction or recovery mechanisms for the prototype. However, in the future, we would like to implement an Automatic Repeat Request (ARQ) system for 1) the device communicating with the tag over Bluetooth and 2) the tags and anchors communicating over UWB. This will assist in ensuring that instances of data are received correctly by the relevant devices and provide us with more precision with the real-time location tracking of the football. 

DEPENDENCIES

Bleak BLE - https://github.com/hbldh/bleak 
Localization - https://github.com/kamalshadi/Localization
Localization dependency (may not be needed) - https://shapely.readthedocs.io/en/stable/

Installation commands
pip install localization
pip install bleak
pip install shapely
