
def Print(thermostat):
    thermostat.Display.PrintTitle("MAIN")
    thermostat.Display.Print("Langue: " + thermostat.Config.getLanguage(), 0, 20)
    thermostat.Display.Print("Auto BS: " + thermostat.Config.getAutoBS(), 0, 30)
    thermostat.Display.Print("BS time: " + thermostat.Config.getTimeBS() + " sec", 0, 40)
    thermostat.Display.Print("GMT: " + thermostat.Config.getGMT(), 0, 50)


