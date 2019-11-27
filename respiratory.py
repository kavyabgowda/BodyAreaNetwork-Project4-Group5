import random
import sys
import time

import iot

class respiratory(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.respiratory = 12.0
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 20.0:
            if self.respiratory < 12.0:
                self.respiratory += 1 * random.randint(-3, +3)
            elif self.respiratory >= 20.0:
                self.respiratory += 1 * random.randint(-3, +3)
            else:
                self.respiratory += 1 * random.randint(-3, +3)
            if self.respiratory < 12.0:
                info = "Below Normal Breathes per Minute - Contact Doctor"
            elif self.respiratory >= 20.0:
                info = "Above Normal Breathes per Minute - Contact Doctor"
            else:
                return
            self.send(f'{self.respiratory:.02f}bpm {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = respiratory(id=int(sys.argv[1]))
    myDevice.start()
    print("started monitoring respiratory")
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
        print("stopped monitoring respiratory")
        sys.exit(0)
__main__()
