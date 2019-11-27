import paho.mqtt.client as mqtt

def on_connect(mqtt_client, obj, flags, rc):
    mqtt_client.subscribe("dev0/log")
    mqtt_client.subscribe("dev1/log")
    mqtt_client.subscribe("dev2/log")
    mqtt_client.subscribe("dev3/log")
    mqtt_client.subscribe("dev4/log")

def on_message(mqtt_client, obj, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("dev0/log")
mqtt_client.subscribe("dev1/log")
mqtt_client.subscribe("dev2/log")
mqtt_client.subscribe("dev3/log")
mqtt_client.subscribe("dev4/log")
print("started logger")
mqtt_client.loop_forever()
