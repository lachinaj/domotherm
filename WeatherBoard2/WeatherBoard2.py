#!/usr/bin/python
import SI1132
import BME280
import sys
import time
import os

from threading import Thread

class WeatherBoard2(Thread):
    Device = "/dev/i2c-1"
    
    #Datas
    UV_Index = 0.0
    Visible = 0.0      # LUX
    IR = 0.0           # LUX
    Temperature = 0.0  #'C
    Humidity = 0.0     # %
    Pressure = 0.0     # hPa
    Altitude = 0.0     # m

    def __init__(self):
        # I2C
        self.si1132 = SI1132.SI1132(self.Device)
        self.bme280 = BME280.BME280(self.Device, 0x03, 0x02, 0x02, 0x02)
        #Thread
        self.Continue = 1
        Thread.__init__(self)

    def get_altitude(self, pressure, seaLevel):
        self.atmospheric = pressure / 100.0
        return 44330.0 * (1.0 - pow(self.atmospheric/seaLevel, 0.1903))

    def run(self):
        while self.Continue:
            #======== si1132 ========
            self.UV_Index = (self.si1132.readUV() / 100.0)
            self.Visible = self.si1132.readVisible()
            self.IR = self.si1132.readIR()
            #======== bme280 ========
            self.Temperature = self.bme280.read_temperature()
            self.Humidity = self.bme280.read_humidity()
            p = self.bme280.read_pressure()
            self.Pressure = (p / 100.0)
            self.Altitude = self.get_altitude(p, 1024.25)

            time.sleep(1)
        
