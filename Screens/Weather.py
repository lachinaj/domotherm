
def Print(thermostat):
    thermostat.Display.PrintTitle("WEATHER")
    thermostat.Display.Print("Temperature: " + "%.2f" % thermostat.Weather.Temperature + " 'C", 0, 20)
    thermostat.Display.Print("Humidity: " + "%.2f" % thermostat.Weather.Humidity + " %", 0, 30)
    thermostat.Display.Print("Pressure: " + "%.2f" % thermostat.Weather.Pressure + " hPa", 0, 40)
