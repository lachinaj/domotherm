
def Print(thermostat):
    thermostat.Display.PrintTitle("LIGHT")
    thermostat.Display.Print("UV Index: " + "%.2f" % thermostat.Weather.UV_Index, 0, 20)
    thermostat.Display.Print("Visible: " + "%.2f" % thermostat.Weather.Visible + " %", 0, 30)
    thermostat.Display.Print("IR: " + "%.2f" % thermostat.Weather.IR + " hPa", 0, 40)
