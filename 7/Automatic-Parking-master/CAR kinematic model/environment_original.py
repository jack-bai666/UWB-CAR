import cv2
import numpy as np


class Environment:
    def __init__(self, obstacles):
        self.margin = 5
        # coordinates are in [x,y] format
        self.car_length = 80
        self.car_width = 40
        self.wheel_length = 15
        self.wheel_width = 7
        self.wheel_positions = np.array([[25, 15], [25, -15], [-25, 15], [-25, -15]])

        # /255 颜色归一化
        self.color = np.array([0, 0, 255]) / 255
        self.wheel_color = np.array([20, 20, 20]) / 255

        self.car_struct = np.array([[+self.car_length / 2, +self.car_width / 2],
                                    [+self.car_length / 2, -self.car_width / 2],
                                    [-self.car_length / 2, -self.car_width / 2],
                                    [-self.car_length / 2, +self.car_width / 2]],
                                   np.int32)

        self.wheel_struct = np.array([[+self.wheel_length / 2, +self.wheel_width / 2],
                                      [+self.wheel_length / 2, -self.wheel_width / 2],
                                      [-self.wheel_length / 2, -self.wheel_width / 2],
                                      [-self.wheel_length / 2, +self.wheel_width / 2]],
                                     np.int32)

        # height and width   1100*1100
        self.background = np.ones((1000 + 20 * self.margin, 1000 + 20 * self.margin, 3))
        self.background[10:1000 + 20 * self.margin:10, :] = np.array([200, 200, 200]) / 255
        self.background[:, 10:1000 + 20 * self.margin:10] = np.array([200, 200, 200]) / 255
        self.place_obstacles(obstacles)

    def place_obstacles(self, obs):
        """
        所有的障碍物坐标上赋 0
        :param obs: 传入的障碍物坐标，未放大十倍
        :return:
        """
        obstacles = np.concatenate([np.array([[0, i] for i in range(100 + 2 * self.margin)]),  # 四周的边界线
                                    np.array([[100 + 2 * self.margin - 1, i] for i in range(100 + 2 * self.margin)]),
                                    np.array([[i, 0] for i in range(100 + 2 * self.margin)]),
                                    np.array([[i, 100 + 2 * self.margin - 1] for i in range(100 + 2 * self.margin)]),
                                    obs + np.array([self.margin, self.margin])]) * 10  # 坐标值扩大十倍
        for ob in obstacles:  # 填充
            self.background[ob[1]:ob[1] + 10, ob[0]:ob[0] + 10] = 0

    def draw_path(self, path):
        path = np.array(path) * 10
        # color = np.random.randint(0,150,3)/255
        color = np.random.randint(0, 255, 3) / 255

        path = path.astype(int)
        for p in path:
            self.background[p[1] + 10 * self.margin:p[1] + 10 * self.margin + 3,
            p[0] + 10 * self.margin:p[0] + 10 * self.margin + 3] = color

    def rotate_car(self, pts, angle=0):
        R = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]])
        return ((R @ pts.T).T).astype(int)

    def render(self, x, y, psi, delta):
        # x,y in 100 coordinates
        x = int(10 * x)
        y = int(10 * y)
        # x,y in 1000 coordinates
        # adding car body
        rotated_struct = self.rotate_car(self.car_struct, angle=psi)
        rotated_struct += np.array([x, y]) + np.array([10 * self.margin, 10 * self.margin])
        rendered = cv2.fillPoly(self.background.copy(), [rotated_struct], self.color)

        # adding wheel
        rotated_wheel_center = self.rotate_car(self.wheel_positions, angle=psi)
        for i, wheel in enumerate(rotated_wheel_center):

            if i < 2:
                rotated_wheel = self.rotate_car(self.wheel_struct, angle=delta + psi)
            else:
                rotated_wheel = self.rotate_car(self.wheel_struct, angle=psi)
            rotated_wheel += np.array([x, y]) + wheel + np.array([10 * self.margin, 10 * self.margin])
            rendered = cv2.fillPoly(rendered, [rotated_wheel], self.wheel_color)

        # gel
        gel = np.vstack([np.random.randint(-50, -30, 16),
                         np.hstack([np.random.randint(-20, -10, 8), np.random.randint(10, 20, 8)])]).T
        gel = self.rotate_car(gel, angle=psi)
        gel += np.array([x, y]) + np.array([10 * self.margin, 10 * self.margin])
        gel = np.vstack([gel, gel + [1, 0], gel + [0, 1], gel + [1, 1]])
        rendered[gel[:, 1], gel[:, 0]] = np.array([60, 60, 135]) / 255

        new_center = np.array([x, y]) + np.array([10 * self.margin, 10 * self.margin])
        self.background = cv2.circle(self.background, (new_center[0], new_center[1]), 2,
                                     [255 / 255, 150 / 255, 100 / 255], -1)

        rendered = cv2.resize(np.flip(rendered, axis=0), (700, 700))
        return rendered


class Parking1:
    def __init__(self, car_pos):
        # [[-2 -4], [-1 -4], [ 0 -4], [ 1 -4], [-2 -3], [-1 -3], [ 0 -3], [ 1 -3], [-2 -2], [-1 -2], [ 0 -2], [ 1 -2], [-2 -1], [-1 -1], [ 0 -1], [ 1 -1], [-2  0], [-1  0], [ 0  0], [ 1  0], [-2  1], [-1  1], [ 0  1], [ 1  1], [-2  2], [-1  2], [ 0  2], [ 1  2], [-2  3], [-1  3], [ 0  3], [ 1  3]]
        self.car_obstacle = self.make_car()
        # 添加墙的障碍物坐标
        self.walls = [[70, i] for i in range(-5, 90)] + \
                     [[30, i] for i in range(10, 105)] + \
                     [[i, 10] for i in range(30, 36)] + \
                     [[i, 90] for i in range(70, 76)] \
            # + [[i,80] for i in range(-5,20)]
        # self.walls = [0,100]
        self.obs = np.array(self.walls)

        # 停车位的中心点
        self.cars = {1: [[35, 20]], 2: [[65, 20]], 3: [[75, 20]], 4: [[95, 20]],
                     5: [[35, 32]], 6: [[65, 32]], 7: [[75, 32]], 8: [[95, 32]],
                     9: [[35, 44]], 10: [[65, 44]], 11: [[75, 44]], 12: [[95, 44]],
                     13: [[35, 56]], 14: [[65, 56]], 15: [[75, 56]], 16: [[95, 56]],
                     17: [[35, 68]], 18: [[65, 68]], 19: [[75, 68]], 20: [[95, 68]],
                     21: [[35, 80]], 22: [[65, 80]], 23: [[75, 80]], 24: [[95, 80]]}
        self.end = self.cars[car_pos][0]  # 目标停车位置[x,y]

        self.cars.pop(car_pos)  # 取出目标停车位置[[x,y]]

    def generate_obstacles(self):
        """
        产生23个障碍物车辆
        :return:终点坐标[],1674个障碍物坐标
        """
        for i in self.cars.keys():  # 循环剩余23个车位
            for j in range(len(self.cars[i])):
                obstacle = self.car_obstacle + self.cars[i]
                self.obs = np.append(self.obs, obstacle)
        return self.end, np.array(self.obs).reshape(-1, 2)

    def make_car(self):
        """
        产生4*8个点
        :return: shape=(32,2)
        """
        car_obstacle_x, car_obstacle_y = np.meshgrid(np.arange(-2, 2), np.arange(-4, 4))
        car_obstacle = np.dstack([car_obstacle_x, car_obstacle_y]).reshape(-1, 2)
        return car_obstacle