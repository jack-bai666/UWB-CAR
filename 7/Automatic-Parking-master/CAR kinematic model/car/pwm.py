import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12,GPIO.OUT)

GPIO.setmode(GPIO.BCM)
LED0 = 12

GPIO.setwarnings(False)
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.LOW)

p = GPIO.PWM(LED0,50)
p.start(3)
input('dian ji hui che ting zhi:')
p.stop()
GPIO.cleanup()