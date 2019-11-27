import random
import sys
import time

import iot

class insulin(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.insulin = 90.0
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 30.0:
            if self.insulin < 90.0:
                self.insulin += 0.2 * random.randint(-20, +20)
            elif self.insulin >= 140.0:
                self.insulin += 0.2 * random.randint(-25, +25)
            else:
                self.insulin += 0.2 * random.randint(-25, +25)
            if self.insulin < 90.0:
                info = "Below Normal Insulin Rate --> Send data to Hospital"
            elif self.insulin >= 140.0:
                info = "Above Normal Insulin Rate --> Send data to Hospital"
            else:
                return
            self.send(f'{self.insulin:.02f}mg {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = insulin(id=int(sys.argv[1]))
    myDevice.start()
    print("started insulin monitoring")
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
        print("stopped insulin monitoring")
        sys.exit(0)
__main__()
