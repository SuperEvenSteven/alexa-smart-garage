#alexa-fauxmo-garage-door
A Python example of an alexa controlled garage door using a Rapsberry Pi running fauxmo. 

## How it works
The Raspberry Pi poses as a Belkin WeMo switch using the Fauxmo service which can be detected by an Amazon Alexa device 
without the need of an IoT Alexa Skill and app. This allows Alexa to perform on, off commands as well as query the 
status of the Fauxmo switch. The Fauxmo service is configured (see config.json) to run the garage_door_btn.py script to
open/close the garage door and the garage_status.py to get the status of the door. i.e. is it open or closed?

### Triggering the Door
The Raspberry Pi is connected to a relay switch that grounds the OSC (Open/Stop/Close) input port of the garage door
opener. To open/close the relay switch the Raspberry Pi grounds the signal input.

### Sensing the Door Status
Two photo resistors (a.k.a LDR) were used to detect the status of the door. One LED on the garage door opener lit up 
solid when the door was open, the other when closed. Each LDR was placed over the garage door opener status LEDs and
a luminescense threshold was set in code to differentiate between LED on/off in the given environment scenarios. i.e. 
LED lit and ambient light present, or LED lit and no ambient light present.

## Installing & Configuring Fauxmo
1. Install raspbian lite on the Raspberry Pi
2. Clone the fauxmo and fauxmo-plugins git projects to the /home/pi location
3. Clone this repository to the /home/pi location
4. Copy the fauxmo.service and garage.door.service files to /etc/systemd/system/ (you will need sudo do do this)
5. Update systemd `sudo systemctl daemon-relaod && sudo systemctl enable fauxmo.service && sudo system enable garage.door.service`
6. Start the services `sudo systemctl start fauxmo.service && sudo systemctl start garage.door.service`

### Door Logic
The python scripts follow the following state machine:

![alternative text](http://www.plantuml.com/plantuml/proxy?src=file:///stat_diagram.puml)


## Alexa, open/close garage door
1. With the Alexa device on the same network as the Raspberry Pi, Open the Alexa app and select add a device
2. Select Other Devices
3. Wait for the app to finish scanning
4. The Belkin WeMo Switch should be detected
5. It will appear as Garage Door and only have on/off keyword capability. i.e. Alexa turn on Garage Door
6. (Optional) Create an Alexa Routine in the app with whatever keyphrase you want e.g. 'Alexa, Open Seasame!'


### References
* https://github.com/n8henrie/fauxmo/blob/master/README.md
* https://raspberrypi.stackexchange.com/questions/83610/gpio-pinout-orientation-raspberypi-zero-w
* https://pimylifeup.com/raspberry-pi-light-sensor/
* http://www.piddlerintheroot.com/5v-relay/
