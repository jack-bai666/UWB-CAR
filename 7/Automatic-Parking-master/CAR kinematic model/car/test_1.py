import pwm_forward
import time
import servo


if __name__ == '__main__':

    print('running after 10s')
    time.sleep(1)
    try:  # try��exceptΪ�̶����䣬���ڲ�׽ִ�й����У��û��Ƿ�����ctrl+C��ֹ����
        for i in range(1,3):
            
            servo.motor_servo(50)
            pwm_forward.Motor_Forward(10)
            time.sleep(1)

            servo.motor_servo(120)
            pwm_forward.Motor_back(10)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    
    servo.motor_servo(90)
    pwm_forward.Motor_Stop()

    servo.stop()  
    p.stop()
    GPIO.cleanup()  # ����GPIO����