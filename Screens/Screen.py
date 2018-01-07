from Info import Print as PrintInfo
from Weather import Print as PrintWeather
from Light import Print as PrintLight

from Network import Print as PrintNetwork
from Commands import Print as PrintCommands
from Main import Print as PrintMain

class Screen(object):
    MainScreens = [ PrintInfo, PrintWeather, PrintLight ]
    ConfigScreens = [ PrintMain, PrintNetwork, PrintCommands ]

    Level = 0

    isHide = False
    isConfig = False
    Current = 0

    def Next(self):
        self.Current += 1
        if self.isConfig:
            if self.Current >= len(self.ConfigScreens):
                self.Current = 0
        else:
            if self.Current >= len(self.MainScreens):
                self.Current = 0

    def Previous(self):
        self.Current -= 1
        if self.Current < 0:
            if self.isConfig:
                self.Current = len(self.ConfigScreens)-1
            else:
                self.Current = len(self.MainScreens)-1

    def PushA(self):
        print "Config"

    def Print(self, thermostat):
        try:
            if self.isHide == False:
                if self.isConfig:
                    self.ConfigScreens[self.Current](thermostat)
                else:
                    self.MainScreens[self.Current](thermostat)
        except:
            self.Current = 0
            self.isConfig = False
