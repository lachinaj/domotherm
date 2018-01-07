from datetime import datetime, timedelta


def Print(thermostat):
    thermostat.Display.PrintTitle(thermostat.Config.getName())

    # Print temperatures
    thermostat.Display.Print("Current: " + "%.1f" % thermostat.Weather.Temperature + " 'C", 0, 20)
    thermostat.Display.Print("Request: " + "%.1f" % thermostat.PID.RequestTemperature + " 'C", 0, 30)

    # Print PID
    if thermostat.PID.Status:
        thermostat.Display.Print("A", 0, 0)

    # Print time
    thermostat.Display.Print(getDateTime(thermostat), 0, 55)

def getDateTime(thermostat):
    gmt = int(thermostat.Config.getGMT())
    now = datetime.now() + timedelta(0,60*60*gmt)
    return '{:%d-%m-%Y %H:%M:%S}'.format(now)
