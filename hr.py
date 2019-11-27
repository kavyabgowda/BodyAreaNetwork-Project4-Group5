import random
import sys
import time

import iot

class heart_rate_monitor(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.heartrate = 60.0
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 5.0:
            if self.heartrate < 60.0:
                self.heartrate += 1 * random.randint(-10, +20)
            elif self.heartrate >= 110.0:
                self.heartrate += 1 * random.randint(-10, +20)
            else:
                self.heartrate += 1 * random.randint(-3, +3)
            if self.heartrate < 60.0:
                info = "Below normal heart beat --> Dead"
            elif self.heartrate >= 110.0:
                info = "Above normal heart beat --> Going to Die"
            else:
                return
            self.send(f'{self.heartrate:.02f}bpm {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = heart_rate_monitor(id=int(sys.argv[1]))
    myDevice.start()
    print("started heart_rate_monitoring")
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
        print("stopped heart_rate_monitoring")
        sys.exit(0)
__main__()
