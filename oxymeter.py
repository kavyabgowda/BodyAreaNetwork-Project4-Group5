import random
import sys
import time

import iot

class Oxymeter(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.oxy = 90.0
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 20.0:
            if self.oxy < 90.0:
                self.oxy += 0.1 * random.randint(-3, +3)
            elif self.oxy >= 100.0:
                self.oxy += 0.1 * random.randint(-3, +3)
            else:
                self.oxy += 0.1 * random.randint(-3, +3)
                
            if self.oxy < 90.0:
                info = "Below normal Oxygen level in Blood"
            elif self.oxy >= 91.0:
                info = "Above normal Oxygen level in Blood"
            else:
                return
                
            self.send(f'{self.oxy:.02f}mmhg {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = Oxymeter(id=int(sys.argv[1]))
    myDevice.start()
    print("started Oxymeter")
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
        print("stopped Oxymeter")
        sys.exit(0)
__main__()
