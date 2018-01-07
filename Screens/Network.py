from subprocess import check_output
import fcntl, socket, struct, os

def Print(thermostat):
    thermostat.Display.PrintTitle("Network")
    thermostat.Display.Print("SSID: " + Network.getSSID(), 0, 20)
    thermostat.Display.Print("IP: " + Network.getAddress(), 0, 30)
    thermostat.Display.Print("MAC: " + Network.getHwAddr(), 0, 40)

class Network(object):
    @staticmethod
    def getAddress():
        ifname = "wlan0"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 
                                0x8915,  # SIOCGIFADDR
                                struct.pack('256s', ifname[:15])
                               )[20:24])
    @staticmethod
    def getSSID():
        ifname = "wlan0"
        ssid = os.popen("iwconfig wlan0 \
                         | grep 'ESSID' \
                         | awk '{print $4}' \
                         | awk -F\\\" '{print $2}'").read()

        return ssid


    @staticmethod
    def getSSIDerr():
        scanoutput = check_output(["iwlist", "wlan0", "scan"])

        for line in scanoutput.split():
              if line.startswith("ESSID"):
                      ssid = line.split('"')[1]

        return ssid

    @staticmethod
    def getHwAddr():
        ifname = "wlan0"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        addr = ''.join(['%02x' % ord(char) for char in info[18:24]])
        return addr
