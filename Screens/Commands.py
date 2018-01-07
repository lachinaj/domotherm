
def Print(thermostat):
    thermostat.Display.PrintTitle("COMMANDS")
    thermostat.Display.Print("NOT IMPLEMENTED", 0, 30)

def PrintAdd(thermostat):
    thermostat.Display.PrintTitle("ADD COMMAND")
    thermostat.Display.Print("Type: ", 0, 20)
    thermostat.Display.Print("Valeur: ", 0, 30)
    thermostat.Display.Print("Action: ", 0, 40)
    thermostat.Display.Print("When: ", 0, 50)
