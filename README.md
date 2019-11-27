#Dependencies:

- Go: https://golang.org
- Python
  - pago mqtt: https://pypi.org/project/paho-mqtt/
- Mosquitto: https://mosquitto.org

Note: All instructions have to be executed from the project
directory (with all the source files).

#Cloud Server:
$ go run server.go

#Edge Node:
$ python3 edge.py [body-id] [server-ip] [server-port]

The body-id, server-ip, and server-port have to be filled in with values, e.g:
$ python3 edge.py alice 123.45.67.89 80

#Sensors:
$ python3 [sensor.py] [device_id]

The specific sensor file (replacing sensor.py) and the device_id (number) have to be filled in with values, e.g.:
$ python3 thermo.py 42
