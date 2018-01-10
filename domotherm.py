#!/usr/bin/env python
from time import gmtime, strftime
from Display import Display
from WeatherBoard2 import WeatherBoard2
from Servo import Servo
from Screens import Screen
from PID import PID
import Config
from TimerReset import TimerReset

class Thermostat(object):
    def Initialize(self):
        print "Initialize"
        self.Config = Config.Config("/etc/domotherm.conf")
        self.Display = Display.Display()
        self.Display.bind_to(self.Button_Event)
        self.Screen = Screen.Screen()
        self.Weather = WeatherBoard2.WeatherBoard2(self.Config.getTemperatureOffset(), self.Config.getTemperatureGain())
        self.PID = PID.PID(self)
        self.PID.RequestTemperature = float(self.Config.getRequestTemperature())

        self.TimerBlackScreen = TimerReset(float(self.Config.getTimeBS()), self.BlackScreen)
        self.TimerBlackScreen.start()

        print "Ready"
        self.Weather.start()
        self.Display.start()
        self.PID.start()

    def BlackScreen(self):
        if self.Config.getAutoBS() == "On":
            self.Screen.isHide = True

    def Button_Event(self, Button):
        self.TimerBlackScreen.reset()
        if self.Screen.isHide:
            self.Screen.Current = 0
            self.isConfig = False
            self.Screen.isHide = False
            self.TimerBlackScreen = TimerReset(float(self.Config.getTimeBS()), self.BlackScreen)
            self.TimerBlackScreen.start()
        elif Button == "A":
            self.Screen.PushA()
        elif Button == "B":
            self.Screen.Current = 0
            self.Screen.isConfig = self.Screen.isConfig != True 
        elif Button == "U":
            self.PID.RequestTemperature += 0.5
            self.Config.setRequestTemperature(self.PID.RequestTemperature)
        elif Button == "D":
            self.PID.RequestTemperature -= 0.5
            self.Config.setRequestTemperature(self.PID.RequestTemperature)
        elif Button == "L":
            self.Screen.Previous()
        elif Button == "R":
            self.Screen.Next()
        elif Button == "C":
            self.Screen.isHide = True
       
    def run(self):
        self.Initialize()
        try:
            while 1:
    	    	# Clear display
	    	self.Display.Clear()

                # Print screen
                self.Screen.Print(self)

		# Update display
		self.Display.Update()

        except KeyboardInterrupt:
            print "Exit"
        except:
            print "Application error"
            self.Display.Clear()
            self.Display.Print("Application error",10,25)
            self.Display.Update()
        
        self.TimerBlackScreen.cancel()
        self.PID.Continue = 0
        self.Display.Continue = 0
        self.Weather.Continue = 0

if __name__ == '__main__':
    Thermostat().run()
