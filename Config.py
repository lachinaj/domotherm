import ConfigParser, os, sys

class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser.ConfigParser()
        
        # Default value
        self.config.add_section('Main')
        self.config.set('Main', 'Name', 'Thermostat')
        self.config.set('Main', 'Language', 'English')
        self.config.set('Main', 'GMT', 0)
        self.config.set('Main', 'RequestTemperature', 21.0)
        self.config.set('Main', 'TemperatureOffset', 0.0)
        self.config.set('Main', 'TemperatureGain', 1.0)

        self.config.add_section('BlackScreen')
        self.config.set('BlackScreen', 'Auto', True)
        self.config.set('BlackScreen', 'Time', 10)
       
        self.config.add_section('PID')
        self.config.set('PID', 'Hysteresis', 1.0)

        self.config.read(filename)
       
    def getName(self):
        return self.config.get('Main', 'Name')

    def setName(self, Name):
        self.config.set('Main', 'Name', Name)
        self.save()

    def getLanguage(self):
        return self.config.get('Main', 'Language')

    def setLanguage(self, Langue):
        self.config.set('Main', 'Language', Langue)
        self.save()

    def getGMT(self):
        return self.config.get('Main', 'GMT')

    def setGMT(self, gmt):
        self.config.set('Main', 'GMT', gmt)
        self.save()

    def getRequestTemperature(self):
        return self.config.get('Main', 'RequestTemperature')

    def setRequestTemperature(self, value):
        self.config.set('Main', 'RequestTemperature', value)
        self.save()

    def getTemperatureOffset(self):
        return self.config.get('Main', 'TemperatureOffset')

    def setTemperatureOffset(self, value):
        self.config.set('Main', 'TemperatureOffset', value)
        self.save()

    def getTemperatureGain(self):
        return self.config.get('Main', 'TemperatureGain')

    def setTemperatureGain(self, value):
        self.config.set('Main', 'TemperatureGain', value)
        self.save()

    def getAutoBS(self):
        return self.config.get('BlackScreen', 'Auto')

    def setAutoBS(self, auto):
        self.config.set('BlackScreen', 'Auto', auto)
        self.save()

    def getTimeBS(self):
        return self.config.get('BlackScreen', 'Time')
        
    def setTimeBS(self, time):
        self.config.set('BlackScreen', 'Time', time)
        self.save()

    def getHysteresis(self):
        return self.config.get('PID', 'Hysteresis')
    
    def setHysteresis(self, value):
        self.config.set('PID', 'Hysteresis', value)
        self.save()

    def save(self):
        with open(self.filename, 'wb') as configfile:
            self.config.write(configfile)
