# domotherm
This thermostat allow this features:
- Temperature control (open and close thermovanne)
- Luminosity control (open and close rolling shutter)
- Humidity control (turn on and off fan)
- Light control (turn on and off light)

#### [Raspberry PI Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w)
<TABLE>
<TR>
<TD width="200px"><img src="https://www.raspberrypi.org/app/uploads/2017/05/Pi-Zero-W-Tilt-462x322.jpg" alt="Raspberry PI Zero W"></TD>
<TD>
<B>Technical Specifications</B>

The Raspberry Pi Zero W extends the Pi Zero family. Launched at the end of February 2017, the Pi Zero W has all the functionality of the original Pi Zero, but comes with with added connectivity, consisting of:
- 802.11 b/g/n wireless LAN
- Bluetooth 4.1
- Bluetooth Low Energy (BLE)
- 1GHz, single\-core CPU
- 512MB RAM
- Mini HDMI and USB On-The-Go ports
- Micro USB power
- HAT-compatible 40\-pin header
- Composite video and reset headers
- CSI camera connector
</TD>
</TR>
</TABLE>


#### [Weather Board 2](https://wiki.odroid.com/accessory/sensor/weather-board/weather-board)
<TABLE>
<TR>
<TD WIDTH="200px"><img src="http://dn.odroid.com/homebackup/201510/WeatherBoardM.jpg" alt="Weather Board 2"></TD>
<TD>
<B>Technical Specification</B>
  
The Weather board has an environmental sensors can measure:
- temperature, 
- humidity,
- barometric pressure, 
- altitude, 
- ultraviolet light index,
- ambient light.
</TD>
</TR>
</TABLE>

#### [Adafruit OLED 128x64 Bonnet 1,3"](https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi)
<TABLE>
  <TR>
    <TD WIDTH="200px"><img src="https://cdn-shop.adafruit.com/970x728/3531-02.jpg" alt="Adafruit OLED 128x64 Bonnet"></TD>
    <TD>
<P>
<B>Technical Specifications</B>
      
- Product Dimensions: 65.3mm x 30.7mm x 15.5mm / 2.6" x 1.2" x 0.6"
- Product Weight: 11.4g / 0.4oz 
</P>
    </TD>
  </TR>
</TABLE>

## Install
- Enable I2C on Raspberry: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
- Install: https://github.com/adafruit/Adafruit_SSD1306
``` bash
sudo cp domotherm.conf /etc/
./domotherm.py
```

#### Install into service
``` bash
sudo cp domotherm /etc/init.d
sudo systemctl daemon-reload
sudo systemctl enable domotherm.service
sudo systemctl start domotherm.service
```

## ChangeLog
#### Initial version
- Communicate with WeatherBoard2
- Read buttons
- Read configuration
- Screens:
  - Main info screen:
    - Current temperature
    - Request temperature
    - Date/Time
  - Weather screen:
    - Current temperature
    - Current humidity
    - Current pressure
  - Light screen:
    - UV Index
    - Luminosity
    - IR
- Configuration:
  - Main configuration
    - Language
    - Auto BlackScreen
    - BlackScreen Time
    - Set GMT time
    - Temperature Gain and Offset
  - Network configuration
    - SSID
    - IP
    - MAC
