import RPi.GPIO as GPIO

class Servo(object):
    pin = 17 #11
    percent = 0.0

    def __init__(self):
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(percent)

    def setPercent(self, value):
        percent = value
        self.pwm.ChangeDutyCycle(percent)
