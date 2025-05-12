#coding:utf-8
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26

GPIO.setwarnings(False)

GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)


p1 = GPIO.PWM(ENA,20)
p1.start(30)
p2 = GPIO.PWM(ENB,20)
p2.start(30)

def Motor_back(speed,hz):
    print('motor back')

    p1.ChangeFrequency(hz)   # freq 为设置的新频率，单位为 Hz
    p2.ChangeFrequency(hz)

    # if speed 
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)

    # time.sleep(0.1)
    # GPIO.output(ENA,True)
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)


def Motor_Stop():
    print('motor stop')
    # p.stop()
    GPIO.output(ENA,True)
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(ENA,False)

    GPIO.output(ENB,True)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    GPIO.output(ENB,False)

def Motor_Forward(speed,hz):
    print('motor forward')
    print(speed,'%')

    p1.ChangeFrequency(hz)   # freq 为设置的新频率，单位为 Hz
    p2.ChangeFrequency(hz)

    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)
    # GPIO.output(ENA,True)
    GPIO.output(IN1,False)
    GPIO.output(IN2,True)
    # GPIO.output(ENA,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)

def conctrl():
    Motor_Forward(10,10)
    time.sleep(1)
    Motor_back(10,10)
    time.sleep(1)    
    Motor_Stop()
    time.sleep(1)

if __name__ == '__main__':

    # for i in range(1,3):
        # conctrl()

    #Motor_Forward(10,40)
    Motor_back(15,40)
    time.sleep(30)
    Motor_Stop()
    p1.stop()
    p2.stop()
    GPIO.cleanup()
