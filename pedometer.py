import random
import sys
import time

import iot

class pedometer(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.pedo = 5.0
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 5.0:
            if self.pedo < 8.0:
                self.pedo += 1 * random.randint(-1, +1)
            elif self.pedo >= 12.0:
                self.pedo += 1 * random.randint(-1, +1)
                
            if self.pedo < 8.0:
                info = "Below normal step count"
            elif self.pedo >= 12.0:
                info = "Above normal step count"
            else:
                return
                
            self.send(f'{self.pedo:.02f}steps {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = pedometer(id=int(sys.argv[1]))
    myDevice.start()
    print("started pedometer")
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
        print("stopped pedometer")
        sys.exit(0)
__main__()
