from threading import Thread
import time
#from Servo import Servo

class PID(Thread):
    Status = False
    Hysteresis = 1.0
    RequestTemperature = 21.0
    Continue = True

    def __init__(self, thermostat):
        self.thermostat = thermostat
#        self.Servo = Servo.Servo()
        Thread.__init__(self)
        print "PID Start"

    def run(self):
        while self.Continue:
            CurrentTemp = float(self.thermostat.Weather.Temperature)
            Hysteresis = float(self.thermostat.Config.getHysteresis())

            if self.RequestTemperature > (CurrentTemp + Hysteresis) :
                if not self.Status:
                    print "Thermostat ON"
                    self.Status = True
#                    self.Servo.setPercent(100)
            else:
                if self.Status:
                    self.Status = False
                    print "Thermostat OFF"
#                    self.Servo.setPercent(0)

            time.sleep(1)
