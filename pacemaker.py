import random
import sys
import time

import iot

class pacemaker(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.load = 1050
        self.lastReading = time.time()
        
    def tick(self):
        iot.IoTDevice.tick(self)
        load = int(self.load)
        cap = self.config[iot.BATTERY_CAPACTIY]
        battery=load/cap
        if time.time() - self.lastReading > 1.0:
            if battery < 0.3:
                info = "Battery is going to die"
                self.send(f'{battery*100:.01f}% {info:s}')
                self.lastReading = time.time()
        
        
def __main__():
    myDevice = pacemaker(id=int(sys.argv[1]))
    myDevice.start()
    print("started pacemaker")
    try:
        while True:
            cmd = input()
            if cmd == 'charge on':
                myDevice.charging = True
            elif cmd == 'charge off':
                myDevice.charging = False
            elif cmd.startswith('send '):
                message = cmd[5:]
                myDevice.send(message)
                    
    except KeyboardInterrupt:
        myDevice.stop()
        print("stopped pacemaker")
        sys.exit(0)
__main__()
