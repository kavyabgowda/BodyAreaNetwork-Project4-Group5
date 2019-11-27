import random
import sys
import time

import iot

class Thermometer(iot.IoTDevice):
    def __init__(self, config=iot.DEFAULT_CONFIG, id=0):
        iot.IoTDevice.__init__(self, config, id)
        self.lastReading = time.time()
        self.temp = 37.5
        
    def tick(self):
        iot.IoTDevice.tick(self)
        if time.time() - self.lastReading > 1.0:
            if self.temp < 37.0:
                self.temp += 0.01 * random.randint(-18, +20)
            elif self.temp >= 38.0:
                self.temp += 0.01 * random.randint(-20, +18)
            else:
                self.temp += 0.01 * random.randint(-25, +25)
                
            if self.temp < 37.0:
                info = "low temperature"
            elif self.temp >= 38.0:
                info = "fever"
            else:
                info = "normal"
                
            self.send(f'{self.temp:.02f}°C {info:s}')
            self.lastReading = time.time()
        
        
def __main__():
    myDevice = Thermometer(id=int(sys.argv[1]))
    myDevice.start()
    print("started thermometer")
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
        print("stopped thermometer")
        sys.exit(0)
__main__()
