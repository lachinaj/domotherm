import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from threading import Thread

class Display(Thread):
	# Input pins
	L_pin = 27
	R_pin = 23
	C_pin = 4
	U_pin = 17
	D_pin = 22

	A_pin = 5
	B_pin = 6

	# Raspberry Pi pin configuration
	RST = 24

	# Default values
	L = 0
	R = 0
	C = 0
	U = 0
	D = 0
	A = 0
	B = 0

	def __init__(self):
		# Events
		self._observers = []

		# Thread
		Thread.__init__(self)
		self.Continue = 1

		# GPIO
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# Display
		self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
		# Initialize library
		self.disp.begin()

		# Clear display
		self.disp.clear()
		self.disp.display()

		# Create blank image for drawing
		# Make sure to create image with mode '1' for 1-bit color
		self.image = Image.new('1', (self.disp.width, self.disp.height))

		# Get drawing object to draw on image
		self.draw = ImageDraw.Draw(self.image)

		self.Clear()

		self.font = ImageFont.load_default()

	def __exit__(self,  exc_type, exc_value, traceback):
		GPIO.cleanup()

	def Clear(self):
		# Draw a black filled box to clear the image
		self.draw.rectangle((0,0,self.disp.width, self.disp.height), outline=0, fill=0)

	def Print(self, Text, x, y):
		self.draw.text((x, y), Text, font=self.font, fill=255)
    
        def PrintTitle(self, Text):
            pos = (128/2) - ((len(Text)/2)*6)   # Width: 128 pixels & 1 char => 6 pixels
            line = "";

            for x in Text:
                line += "-"
            
            self.Print(Text, pos, 0)
            self.Print(line, pos, 7)

	def Update(self):
		self.disp.image(self.image)
		self.disp.display()
		time.sleep(.01)

	def run(self):
		while self.Continue:
			self.TestIO(self.A_pin, self.A, "A")
			self.TestIO(self.B_pin, self.B, "B")
			self.TestIO(self.U_pin, self.U, "U")
			self.TestIO(self.L_pin, self.L, "L")
			self.TestIO(self.R_pin, self.R, "R")
			self.TestIO(self.D_pin, self.D, "D")
			self.TestIO(self.C_pin, self.C, "C")

	def TestIO(self, pin, local, text):
		if GPIO.input(pin):
			local = 0
		else:
			if local == 0:
				self.SendCallback(text)
				time.sleep(.5)
			local = 1

	def SendCallback(self, pin):
		for callback in self._observers:
			callback(pin)

	def bind_to(self, callback):
		self._observers.append(callback)
