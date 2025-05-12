# 在这里写上你的代码 :-)
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED0 = 10
LED1 = 9
LED2 = 25
GPIO.setwarnings(False)
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)
def init_light():

    GPIO.output(LED0,True)
    GPIO.output(LED1,False)
    GPIO.output(LED2,False)
    print(1)

    time.sleep(1)

    GPIO.output(LED0,False)
    GPIO.output(LED1,True)
    GPIO.output(LED2,True)
    print(2)
    time.sleep(1)

for i in range(1,5):
    init_light()

GPIO.cleanup()

