import cv2
import numpy as np
from time import sleep
import argparse
import time

from environment import Environment, Parking1
from pathplanning import PathPlanning, ParkPathPlanning, interpolate_path
from control import Car_Dynamics, MPC_Controller, Linear_MPC_Controller
from utils import angle_of_line, make_square, DataLogger

import plath_test
import ttt

import sys   #导入sys模块
sys.path.append("../car")
from car import servo
from car import pwm_forward


if __name__ == '__main__':
    # time.sleep(10)

    parser = argparse.ArgumentParser()
    parser.add_argument('--x_start', type=int, default=0, help='X of start')
    parser.add_argument('--y_start', type=int, default=90, help='Y of start')
    parser.add_argument('--psi_start', type=int, default=90, help='psi of start')
    parser.add_argument('--x_end', type=int, default=90, help='X of end')
    parser.add_argument('--y_end', type=int, default=80, help='Y of end')
    parser.add_argument('--parking', type=int, default=12, help='park position in parking1 out of 24')

    # 属性给与args实例： 把parser中设置的所有"add_argument"给返回到args子类实例当中， 那么parser中增加的属性内容都会在args实例中，使用即可。
    args = parser.parse_args()
    logger = DataLogger()

    ########################## default variables ################################################
    # start = np.array([args.x_start, args.y_start])
    end = np.array([args.x_end, args.y_end])
    # 仅考虑泊车路径的情况下，把新起点设为new_end(89 32)
    # start = np.array([89, 29])
    # start = np.array([87, 29])
    start = np.array([5, 5])
    #############################################################################################

    # environment margin  : 5
    # pathplanning margin : 5

    ########################## defining obstacles ###############################################
    parking1 = Parking1(args.parking)
    # end：目标停车位的中心点   obs：障碍物矩阵
    end, obs = parking1.generate_obstacles()

    print("end1:", end)
    # add squares
    # square1 = make_square(10,65,20)
    # square2 = make_square(15,30,20)
    # square3 = make_square(50,50,10)
    # obs = np.vstack([obs,square1,square2,square3])

    # Rahneshan logo
    # start = np.array([50,5])
    # end = np.array([35,67])
    # rah = np.flip(cv2.imread('READ_ME/rahneshan_obstacle.png',0), axis=0)
    # obs = np.vstack([np.where(rah<100)[1],np.where(rah<100)[0]]).T

    # new_obs = np.array([[89,32],[79,79],[78,79]])
    # obs = np.vstack([obs,new_obs])
    #############################################################################################

    ########################### initialization ##################################################
    env = Environment(obs)  # 产生仿真环境
    my_car = Car_Dynamics(start[0], start[1], 0, np.deg2rad(args.psi_start), length=2, dt=0.35)
    MPC_HORIZON = 5  # MPC区间
    # controller = MPC_Controller()
    controller = Linear_MPC_Controller()

    res = env.render(my_car.x, my_car.y, my_car.psi, 0)
    #cv2.imshow('environment', res)
    #key = cv2.waitKey(1)
    # key = cv2.waitKey(0)
    #############################################################################################

    ############################# path planning #################################################
    park_path_planner = ParkPathPlanning(obs)
    path_planner = PathPlanning(obs)

    print('planning park scenario ...')  # park_path 泊车路径
    # 泊车路径采用直线——圆弧——圆弧——直线的形式，ensure_path1与ensure_path2为两条直线路径
    new_end, park_path, ensure_path1, ensure_path2 = park_path_planner.generate_park_scenario(int(start[0]),
                                                                                              int(start[1]),
                                                                                              int(end[0]), int(end[1]))
    # print('ensure_path1:',ensure_path1)       # (89,29~31.75)
    print('park_path',park_path,'shape',park_path.shape)
    print('routing to destination ...')
    print("new_end", new_end)
    # path = path_planner.plan_path(int(start[0]), int(start[1]), int(new_end[0]), int(new_end[1]))
    # path = np.vstack([path, ensure_path1])

    path_v ,xy1,xy2= plath_test.park_v()      # 垂直泊车的路径

    print('interpolating ...')
    # interpolated_path = interpolate_path(ensure_path1, sample_rate=5)
    # interpolated_path = interpolate_path(path, sample_rate=5)
    interpolated_park_path = interpolate_path(park_path, sample_rate=2)
    interpolated_park_path = np.vstack([ensure_path1[::-1], interpolated_park_path, ensure_path2[::-1]])

    path_v = interpolate_path(path_v, sample_rate=2)

    # env.draw_path(interpolated_path)
    # env.draw_path(interpolated_park_path)
    env.draw_car(xy1,xy2)                         # 画停车位
    # print(interpolated_park_path.shape)     # 泊车路径的shape:(60,2)
    print(path_v.shape)
    env.draw_path(path_v)                   # 画垂直泊车路径 (27,2)

    final_path = np.vstack([
        # interpolated_path,
        interpolated_park_path, ensure_path2])
    #############################################################################################

    ################################## control ##################################################
    print('driving to destination ...')
    
    back = 0
    
    # 对于final_path中的每一个点（以及它的索引i），进行以下操作
    for i, point in enumerate(path_v):
        T1 = time.perf_counter()

        # 使用控制器（controller）的optimize方法，基于当前车辆状态（my_car）和接下来MPC_HORIZON个路径点
        acc, delta = controller.optimize(my_car, path_v[i:i + MPC_HORIZON])

        my_car.update_state(my_car.move(acc, delta))
        print("acc:", acc, "delta:", np.rad2deg(delta), "v:", my_car.v)

        deg = -np.rad2deg(delta) + 90
        servo.motor_servo(deg)
        v = my_car.v * 10
	
        if v == 0:
            pwm_forward.Motor_Stop()
            print("v == 0")
        elif v > 0:
            if v < 3:
            	pwm_forward.Motor_Forward(6,20)
            elif v < 8:
                pwm_forward.Motor_Forward(8,20)
            # elif v < 7:
                # pwm_forward.Motor_Forward(9,20)
            else:
                pwm_forward.Motor_Forward(10.5,20)
            print("v > 0")
        else:
            back = back + 1
            if back < 3:
            	 pwm_forward.Motor_back(11.5,20)
            	# pass
            else:
            	if abs(v) < 7:
                	pwm_forward.Motor_back(7,20)
            # pwm_forward.Motor_back(10)
            	# elif abs(v) < 7:
                	#pwm_forward.Motor_back(8,20)
            	elif abs(v) < 10:
            		pwm_forward.Motor_back(9,20)
            	else:
            		pwm_forward.Motor_back(10.5,20)
            print("v < 0")
            

        # 渲染
        # res = env.render(my_car.x, my_car.y, my_car.psi, delta)
        # 使用日志记录器（logger）记录当前路径点、车辆状态、加速度和方向盘转角
        logger.log(point, my_car, acc, delta)
        # 使用OpenCV显示渲染结果（即当前车辆状态和环境）
        # cv2.imshow('environment', res)
        T2 =time.perf_counter()
        print('程序运行时间:%s毫秒' % ((T2 - T1)*1000))
        # # 等待1毫秒，检查是否有按键被按下
        # key = cv2.waitKey(1)
        # if key == ord('s'):  # 如果按下了's'键，则将当前渲染结果保存为图片文件'res.png'
        #     cv2.imwrite('res.png', res * 255)

    # #stop
    pwm_forward.Motor_Stop()
    # servo.motor_servo(90)
    # servo.stop()
    # p.stop()
    # GPIO.cleanup()  # ����GPIO����

    # zeroing car steer
    res = env.render(my_car.x, my_car.y, my_car.psi, 0)
    logger.save_data()
    #cv2.imshow('environment', res)
    #key = cv2.waitKey()
    #############################################################################################

    cv2.destroyAllWindows()

