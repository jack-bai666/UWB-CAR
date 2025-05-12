import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# import time
# from Coordinate_transformation import Coordinate_transformation

# img = np.ones((1500, 1500, 3), np.uint8) * 225
#
# #车位线
# #车位尺寸为250*600
# img=cv2.line(img,(0,900),(1500,900),(255,0,0),2)
# img=cv2.rectangle(img,(800,1500),(1050,900),(255,0,0),2)

# 起始坐标(930,290)
# x_start = 930
x_start = 50
# y_start = 290
y_start = 50

# 车身
car_w = 18  # 车宽
car_h = 32  # 车长
L = 18  # 轴距
# d0=150      #起点处，车身与车位线的平行距离
# R=600       #转弯半径（可由方向盘角度控制）
# r=[500,600,700]
r = [55,55,40]
# R1=R2=R     #R1,R2分别为第一第二个圆弧的转弯半径
dis = 6  # 后轮轴与车尾的距离


def vertical_path(xy1, xy2):
    '''
    :param xy1: 入位点1的坐标(在环视图中的坐标)
    :param xy2: 入位点2的坐标
    :param d0:  后轮轴中心距离车位线的距离
    :return:    返回垂直车位的泊车路径
    '''
    d0 = abs(xy1[0] - x_start)
    # img = np.ones((1500, 1500, 3), np.uint8) * 225

    # xy0,alp0=Coordinate_transformation(xy1,xy2)
    # print(xy0,alp0)

    # 后轮轴中心坐标
    x0 = int(x_start)
    y0 = int(y_start)
    print(f'后轮轴初始坐标{(x0, y0)}')

    # img = cv2.circle(img, (x0+800, y0+800), 3, (0, 0, 255), 2)

    # 车位入口点坐标
    x_1 = xy1[0]
    y_1 = xy1[1]
    x_2 = xy2[0]
    y_2 = xy2[1]

    # 切换点c的坐标计算
    x_c = int((x_1 + x_2) // 2 + L // 2)
    # x_c = int((x_1 + x_2) // 2)
    y_c = int((y_1 + y_2) // 2)
    print(f"c点坐标{(x_c, y_c)}")
    D = L // 2
    # D = 0
    # img = cv2.circle(img, (x_c+800, y_c+800), 3, (0, 0, 255), 2)

    list_all = []  # 用于存放路径离散点
    # for R in range(38,70):
    # for R in r:
    # R1 = R2 = R = r[0]
    R1 = r[0]
    R2 = r[1]
    # 圆心O2的坐标计算
    x_o2 = x_c
    y_o2 = y_c + R2

    # print('x_o2',x_c,'y_o2',y_o2)

    # 切换点b的坐标计算
    alp = math.asin((d0 + R2 + D) / (R1 + R2))  # alp为切换点c到切换点b的转动角度
    x_b = (x_o2 - R2 * (math.sin(alp))) // 1
    y_b = (y_o2 - R2 * (math.cos(alp))) // 1
    x_b = int(x_b)
    y_b = int(y_b)

    print(f'B点坐标{(x_b, y_b)}')
    # img = cv2.circle(img, (x_b+800, y_b+800), 3, (0, 0, 255), 2)

    # 圆心O1的坐标计算
    x_o1 = x_o2 - (R1 + R2) * (math.sin(alp))
    y_o1 = y_o2 - (R1 + R2) * (math.cos(alp))
    x_o1 = int(x_o1)
    y_o1 = int(y_o1)

    # 切换点A的坐标计算
    x_a = int(x_o1 + R1)
    y_a = int(y_o1)
    print(f'A点坐标{(x_a, y_a)}')
    # img = cv2.circle(img, (x_a+800, y_a+800), 3, (0, 0, 255), 2)

    # 结束点后轮轴中心坐标
    x_end = int((x_1 + x_2) // 2 + car_h)
    y_end = int((y_1 + y_2) // 2)
    print(f'后轮轴结束坐标{(x_end, y_end)}')
    # img = cv2.circle(img, (x_end+800, y_end+800), 3, (0, 0, 255), 2)

    # 从初始点到A点
    list0 = []
    for y in range(y0, y_a, 5):             # 步长分别为 2,2,4,2
        list0.append((x0, y))
    # list0.reverse()
    # img = cv2.line(img, (x0+800, y0+800), (x_a+800, y_a+800), (0, 0, 0), 2)
    # list0.append((x_a,y_a))
    # print('list0', list0)

    list1 = []
    # list1.append((x_b, y_b))
    # 从a点到b点
    for x in range(x_b, x_a, 4):
        y = int(math.sqrt(R1 ** 2 - (x - x_o1) ** 2) + y_o1)
        list1.append((x, y))
        # img = cv2.circle(img, (x+800, y+800), 2, (0, 0, 255), 2)
    y = int(math.sqrt(R1 ** 2 - (x_a - 1 - x_o1) ** 2) + y_o1)
    list1.append((x_a - 1, y))
    list1.reverse()
    # print('list1', list1)

    list2 = []
    # list2.append((x_a, y_a))
    # 从b点到c点
    i = 1
    for x in range(x_b, x_c, 8):
        if i % 2 == 0 & i < 8:
            continue
        if i % 3 == 0 & i < 10:
            continue
        y = int(-math.sqrt(R2 ** 2 - (x - x_o2) ** 2) + y_o2)
        # img = cv2.circle(img, (x+800, y+800), 2, (0, 0, 255), 2)

        list2.append((x, y))
        # list2.append(x)
        # list2.append(y)
    # list2.reverse()
    # arr2 = np.array(list2, np.int).reshape(1, x_b - x_c, 2)
    # img = cv2.polylines(img, arr2, False, (255, 0, 0))

    # 从c点到结束点
    list3 = []
    for x in range(x_c, x_end, 5):
        list3.append((x, y_end))
    # list3.reverse()
    # img = cv2.line(img, (x_c+800, y_c+800), (x_end+800, y_end+800), (0, 0, 0), 2)

    list_all.append(list0 + list1 + list2 + list3)  # 不同半径下产生的路径
    list_t = list0 + list1 + list2 + list3
    # print(type(list_all[1][1][0]))

    print("len:",len(list_all))   # 三条路径
    # print('list_all', list_all)
    # print('list3', list3)
    # print('list_t', list_t)
    return list_all, list_t


# 画图函数
def show(xy1, xy2):
    img = np.ones((200, 200, 3), np.uint8) * 225
    img01 = np.ones((200, 200, 3), np.uint8) * 225

    if 20 < abs(xy1[1] - xy2[1]) < 40:  # 垂直车位
        if xy1[1] > xy2[1]:
            xy1, xy2 = xy2, xy1
        cv2.rectangle(img, (int(0 + xy1[0]), int(xy1[1])), (int(10 + xy1[0] + 31), int(xy1[1] + 17.6+10)), (255, 0, 0), 2)
        cv2.rectangle(img01, (int(0 + xy1[0]), int(xy1[1])), (int(0 + xy1[0] + 80), int(xy1[1] + 60)), (255, 0, 0), 2)

        path, list_t = vertical_path(xy1, xy2)

        # 画出所有情况下的路径
        for i in range(len(path)):
            # print("i:", i)
            for j in path[i]:
                # print("j:",j)
                img = cv2.circle(img, (j[0], j[1]), 2, (0, 0, 255), 1)
        cv2.imwrite('vertical_demo.png', img)
        plt.imshow(img[:, :, ::-1])
        plt.title("frame")
        plt.show()


    return list_t


def park_v():
    x_p = x_start + 3/2 * car_w
    y_p = y_start + 15
    # print(x_p)
    xy1 = (x_p, y_p)
    xy2 = (x_p, y_p + car_w + 10)

    _ , list_t = vertical_path(xy1, xy2)

    # list_t = show(xy1, xy2)

    print('list_t', list_t)

    arr = np.array(list_t)
    arr = arr / 10
    # print('arr', arr, 'shape', arr.shape)
    return arr


if __name__ == '__main__':
    # 垂直车位的例子
    x_p = x_start + 3/2 * car_w
    y_p = y_start + 15
    # print(x_p)
    xy1 = (x_p, y_p)
    xy2 = (x_p, y_p + car_w + 10)
    # print(xy1, xy2)
    list_t = show(xy1, xy2)
    # print('list_t', list_t)

    arr = np.array(list_t)
    arr = arr / 10
    # print('arr', arr, 'shape', arr.shape)

