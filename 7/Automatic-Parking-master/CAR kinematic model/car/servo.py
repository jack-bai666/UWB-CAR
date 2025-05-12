#!/usr/bin/python
# coding:utf-8
# servo_PWM_GPIO.py
# ��ݮ��GPIO�����ⲿ�������ذڶ����Ƕȷ�ΧΪ33~147�㣬����Ϊ4�롣(90��+-57��)

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges. "
          " You can achieve this by using 'sudo' to run your script")
import time
# import pwm_forward

def servo_map(before_value, before_range_min, before_range_max, after_range_min, after_range_max):
    percent = (before_value - before_range_min) / (before_range_max - before_range_min)
    after_value = after_range_min + percent * (after_range_max - after_range_min)
    return after_value


GPIO.setmode(GPIO.BCM)  # ��ʼ��GPIO���ű��뷽ʽ
servo_SIG = 12
servo_freq = 50
servo_time = 0.1
servo_width_min = 2.5
servo_width_max = 12.5
# servo_degree_div =servo_width_max - servo_width_min)/180
GPIO.setup(servo_SIG, GPIO.OUT)
# ��������Ҫ�������Ÿ��þ��棬������GPIO.setwarnings(False)
# GPIO.setwarnings(False)
servo = GPIO.PWM(servo_SIG, servo_freq)  # �ź�����=servo_SIG Ƶ��=servo_freq in HZ
servo.start((servo_width_min+servo_width_max)/2)
# servo.ChangeDutyCycle((servo_width_min+servo_width_max)/2)  # �ع�������λ

def motor_servo(dc):
    # 41 ~ 146

    if dc < 41:
        dc = 41
    elif dc > 146:
        dc = 146

    dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max)
    servo.ChangeDutyCycle(dc_trans)
    time.sleep(0.1)

def servoclose():
    motor_servo(90)
    servo.stop()

if __name__ == '__main__':
    for i in range(30):
    
    	print('running after 1s')
    	time.sleep(1)
    	motor_servo(90)
    servo.stop()  # ֹͣpwm
    GPIO.cleanup()  # ����GPIO����

# time.sleep(servo_time)
# motor_servo(75)
# if __name__ == '__main__':

#     print('running after 2s')
#     time.sleep(2)
#     try:  # try��exceptΪ�̶����䣬���ڲ�׽ִ�й����У��û��Ƿ�����ctrl+C��ֹ����
#         while 1:
#             pwm_forward.Motor_Forward(10)
#             for dc in range(33, 157+1, 1):
#                 dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max)
#                 servo.ChangeDutyCycle(dc_trans)
#                 # print(dc_trans)
#                 time.sleep(servo_time)
#             time.sleep(0.1)
#             pwm_forward.Motor_back(10)
#             # pwm_forward.Motor_Stop()
#             for dc in range(157, 33-1, -1):
#                 dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max)
#                 servo.ChangeDutyCycle(dc_trans)
#                 # print(dc_trans)
#                 time.sleep(servo_time)
#             time.sleep(0.1)
#     except KeyboardInterrupt:
#         pass
    # servo.stop()  # ֹͣpwm
    # GPIO.cleanup()  # ����GPIO����

# servo.stop()  # ֹͣpwm
# GPIO.cleanup()  # ����GPIO����
