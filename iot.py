import paho.mqtt.client as mqtt
import time, threading

BATTERY_CAPACTIY       = "battery_capacity"
BATTERY_VOLTAGE        = "battery_volatage"
BATTERY_CHARGE_RAPID_P = "battery_charge_rapid_p"
BATTERY_CHARGE_NORMAL  = "battery_charge_normal"
BATTERY_CHARGE_RAPID   = "battery_charge_rapid"
CURRENT_IDLE           = "current_idle"
CURRENT_RECEIVE        = "current_receive"
CURRENT_SEND           = "current_send"
TRANSFER_BAUD_RATE     = "transfer_baud_rate"

DEFAULT_CONFIG = {
    BATTERY_CAPACTIY:      3500, #mAh
    BATTERY_VOLTAGE:        3.5, #V
    BATTERY_CHARGE_RAPID_P: 0.8, #Fraction 0.0 - 1.0
    BATTERY_CHARGE_NORMAL:  520, #mA
    BATTERY_CHARGE_RAPID:  1300, #mA
    CURRENT_IDLE:             5, #mA
    CURRENT_RECEIVE:        200, #mA
    CURRENT_SEND:           300, #mA
    TRANSFER_BAUD_RATE:    9600  #Bd = bit/s
}

ACTIVITY_RECEIVE = "activity_receive"
ACTIVITY_SEND    = "activity_send"

SIM_SPEED   = 1e1  #realtime
TICK_PERIOD = 5e-3 #5ms
LOG_PERIOD  = 3    #3s

class IoTDevice(threading.Timer):
    def __init__(self, config=None, id=0):
        threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.config = DEFAULT_CONFIG
        if config:
            self.config.update(config)
        self.load = self.config[BATTERY_CAPACTIY]
        self.charging = False
        self.id = id
        self.activity = []
        self.nextIOActivity = ACTIVITY_SEND
        self.rcvBuffer = []
        self.sndBuffer = []
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.connect("localhost", port=1883)
        self.mqttc.loop_start()
    
    def stop(self):
        self.stopEvent.set()
        self.mqttc.loop_stop()
        
    def run(self):
        self.currentTime = time.time()
        self.lastTick = self.currentTime
        self.deadlineIO = self.currentTime
        self.lastLog = self.currentTime
        while not self.stopEvent.wait(0.001) and not self.stopEvent.is_set():
            self.currentTime = time.time()
            if self.currentTime - self.lastTick >= TICK_PERIOD:
                self.tick()
                self.lastTick = self.currentTime
            if self.currentTime >= self.deadlineIO:
                self.handleIO()
            if self.currentTime - self.lastLog >= LOG_PERIOD:
                self.log()
                self.lastLog = self.currentTime
    
    def tick(self):
        deltaT = (self.currentTime - self.lastTick) * SIM_SPEED #s
        current = 0.0 #mA
        if len(self.activity) == 0:
            current -= self.config[CURRENT_IDLE]
        if ACTIVITY_SEND in self.activity:
            current -= self.config[CURRENT_SEND]
        if ACTIVITY_RECEIVE in self.activity:
            current -= self.config[CURRENT_RECEIVE]
        if self.charging:
            if self.isRapidCharging():
                current += self.config[BATTERY_CHARGE_RAPID]
            else:
                current += self.config[BATTERY_CHARGE_NORMAL]
        deltaLoad = current * deltaT / 3600 #mAh
        self.load += deltaLoad
        self.load = max(self.load, 0.0)
        self.load = min(self.load, self.config[BATTERY_CAPACTIY])
    
    def isRapidCharging(self):
        return self.load / self.config[BATTERY_CAPACTIY] < self.config[BATTERY_CHARGE_RAPID_P]
    
    def handleIO(self):
        if ACTIVITY_RECEIVE in self.activity:
            self.activity.remove(ACTIVITY_RECEIVE)
        if ACTIVITY_SEND in self.activity:
            self.activity.remove(ACTIVITY_SEND)
        
        canSend = len(self.sndBuffer) > 0
        canReceive = len(self.rcvBuffer) > 0 and '\n' in self.rcvBuffer
        if canSend and (not canReceive or self.nextIOActivity == ACTIVITY_SEND):
            n = min(200, len(self.sndBuffer))
            self.mqttc.publish(topic=f'dev{self.id:d}/out',
                               payload="".join(self.sndBuffer[:n]),
                               qos=0,
                               retain=False)
            self.sndBuffer = self.sndBuffer[n:]
            self.activity.append(ACTIVITY_SEND)
            self.deadlineIO = self.currentTime + n / self.config[TRANSFER_BAUD_RATE] / SIM_SPEED
            self.nextIOActivity = ACTIVITY_RECEIVE
        elif canReceive and (not canSend or self.nextIOActivity == ACTIVITY_RECEIVE):
            n = self.rcvBuffer.index('\n')
            self.receive("".join(self.rcvBuffer[:n]))
            self.activity.append(ACTIVITY_RECEIVE)
            self.rcvBuffer = self.rcvBuffer[n+1:]
            self.deadlineIO = self.currentTime + (n+1) / self.config[TRANSFER_BAUD_RATE] / SIM_SPEED
            self.nextIOActivity = ACTIVITY_SEND
    
    def send(self, message):
        self.sndBuffer.append(message)
        
    def receive(self, message):
        print("received message: " + message)
    
    def on_message(self, client, userdata, message):
        if message.topic == f'dev{self.id:d}/in':
            self.rcvBuffer += message.payload.decode("utf-8")
          
    def on_connect(self, mqtt_client, obj, flags, rc):
        for i in range(20):
            if i == self.id:
                self.mqttc.subscribe(f'dev{self.id:d}/in')
            else:
                self.mqttc.subscribe(f'dev{i:d}/log')
    
    def log(self):
        load = int(self.load)
        cap = self.config[BATTERY_CAPACTIY]
        if self.charging:
            if self.isRapidCharging():
                chargingInfo = 'rapid charging'
            else:
                chargingInfo = 'normal charging'
        else:
            chargingInfo = 'not charging'
        if len(self.activity) == 0:
            activityInfo = "idle"
        else:
            activityInfo = ""
            if len(self.rcvBuffer) > 0:
                activityInfo += "rcv"
            else:
                activityInfo += "   "
            activityInfo += " "
            if len(self.sndBuffer) > 0:
                activityInfo += "snd"
            else:
                activityInfo += "   "
        log = f'{self.load:04.0f}/{cap:04d}mAh {chargingInfo:15s} {activityInfo:s}'
        self.mqttc.publish(topic=f'dev{self.id:d}/log',
                           payload=log,
                           qos=0,
                           retain=False)
