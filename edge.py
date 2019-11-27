import paho.mqtt.client as mqtt
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

id = sys.argv[1]

# Connect the socket to the port where the server is listening
server_address = (sys.argv[2], int(sys.argv[3]))
sock.connect(server_address)
sock.sendall(bytes("NEWEDGE " + id + "\n", "utf-8"))

def on_connect(mqtt_client, obj, flags, rc):
    for i in range(20):
        mqtt_client.subscribe(f'dev{i:d}/out')

def on_message(mqtt_client, obj, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    try:
        # Send data
        sock.sendall(bytes("UPDATE " + msg.topic[:4] + " " + str(msg.payload.decode("utf-8")) + "\n", "utf-8"))
    finally:
        a = 42

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)
for i in range(20):
    mqtt_client.subscribe(f'dev{i:d}/out')
mqtt_client.loop_start()
print("started edge node")
while True:
    cmd = input()
    if cmd.startswith('send '):
        topic = cmd.split(' ')[1]
        message = "".join(cmd.split(' ')[2:]) + "\n"
        mqtt_client.publish(topic=topic,
                            payload=message,
                            qos=0,
                            retain=False)
