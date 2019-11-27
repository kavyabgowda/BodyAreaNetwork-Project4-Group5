import random
import sys
import time

import iot

class BP(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.bp = 80.0 #normal
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 1.0:
            if self.bp < 80.0:
                self.bp += 1 * random.randint(-3, +3)
            elif self.bp >= 100.0:
                self.bp += 1 * random.randint(-3, +3)
            else:
                self.bp += 1 * random.randint(-5, +5)
                
            if self.bp < 80.0:
                info = "Low BP ---> Medication required"
            elif self.bp >= 100.0:
                info = "High BP ---> Medication required"
            else:
                return
                
            self.send(f'{self.bp:.02f}mmhg {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = BP(id=int(sys.argv[1]))
    myDevice.start()
    print("Started BP Sensor")
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
        print("Stopped BP Sensor")
        sys.exit(0)
__main__()
