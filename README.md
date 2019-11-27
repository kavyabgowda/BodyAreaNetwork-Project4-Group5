# Simulation of Body Area Network:
The aim of this project is to **Simulate a Body Area Network(BAN)** which is ***Scalable, Fault Tolerant, Energy Efficient, Robust*** and ***Realistic in Nature.*** This project is a Simulation of Human body with below mentioned sensors passing the signals to Sink (Edge Node). The communication between Sensors in a Human Body and Sink is achieved by MQTT Protocol in which Sink acts as a Edge Broker Node for all the sensors Subscribed to it. The data collected from Sensors are processed by Edge Node and sent to Private Cloud Server by all the Edges via TCP Connection. In this way the data transfer is made secure and can be scaled easily with the increase in number of sensors due to MQTT connection.

**List of Sensors Simulated in Body Area Network:**

* PaceMaker
* Blood Pressure Sensor
* Heart Rate Sensor
* Digital Insulin Sensor
* Oxymeter
* Pedometer
* Respiratory Sensor
* Temperature Sensor

These Sensors are Simulated by Executing the Sensor Programs in Local PCs as Human Bodies with Edge Program as Sink. The Private Cloud is again a Local PC in the same network or different network connected via Internet.

<p align="center">
  <img src="BAN Architecture Final.png" width="450" height="450" alt="accessibility text">
</p>

# Project Setup:
## Pre-Requisites:

Install the below mentioned softwares in three PCs to Simulate **two Human Bodies** and **one Private Cloud.**

- **Go:** (Download from: https://golang.org)
- **Python:**
  - **pago mqtt:** (Download from: https://pypi.org/project/paho-mqtt/)
- **Mosquitto:** https://mosquitto.org

## Running the code:

The **BodyAreaNetwork-Project4-Group5** Code Folder can be placed in any Directory and Executed

**Note:** All instructions have to be executed from the project root directory (with all the source files).*Mosquitto* has to be running in the background in all PCs along with Source Code. Then the components can be started in the order below. 

**Execute the files in command prompt of each PC using below commands**

## Cloud Server: 

In the First PC run the below command in command prompt to start the Cloud Server

$ go run server.go

## Edge Node: 

In the two sepearate PCs run the below commands in command prompt to start the Edge Node in each PC

$ python3 edge.py *[body-id]* *[server-ip]* *[server-port]*

The body-id, server-ip, and server-port have to be filled in with values, e.g:

$ python3 edge.py alice 123.45.67.89 80

## Logger: 

Execute the below command in Edge Node PCs command prompt

$ python3 logger.py

## Sensors: 

Exceute the below command in Edge Node PCs by opening seperate command prompts for each Sensor file

$ python3 *[sensor.py]* *[device_id]*

The specific sensor file (replacing sensor.py) and the device_id (number) have to be filled in with values, e.g.:

$ python3 thermo.py 0

- - - 


