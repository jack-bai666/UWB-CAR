import math
import numpy as np
import matplotlib.pyplot as plt
from pathplanning import PathPlanning, ParkPathPlanning, interpolate_path

# print(math.atan2(-1,0),math.atan2(0,1))
# 起始点(89，32)   终点(95,44)
y0 = 32
y1 = 44
x0 = 89
x1 = 95
curve_x = np.array([])
curve_y = np.array([])

y = np.arange(y0,y1+1)          # y0 到 y1 共 y 个点
print(y)
circle_fun = (6.9**2 - (y-y0)**2)       # (x-xo)^2 = ...
print(circle_fun)

# print(np.sqrt(circle_fun[circle_fun>=0]))

x = (np.sqrt(circle_fun[circle_fun>=0]) + x0+6.9)       # xo = x0 + 6.9
y = y[circle_fun>=0]                                    # 取上半圆
x = (x - 2*(x-(x0+6.9)))                                # 取左边1/4圆

x11 = (-np.sqrt(circle_fun[circle_fun>=0]) + x0+6.9)

print(x)
print(x11)

choices = x<x0+6.9/2
print(choices)                  # 再取1/8圆
x=x[choices]
# print(x)
y=y[choices]

curve_x = np.append(curve_x, x)
curve_y = np.append(curve_y, y)

plt.plot(curve_x, curve_y,'o')
plt.show()

y = np.arange(y0, y1 + 1)
circle_fun = (6.9 ** 2 - (y - y1) ** 2)
x = (np.sqrt(circle_fun[circle_fun >= 0]) + x1 - 6.9)
y = y[circle_fun >= 0]
choices = x > x1 - 6.9 / 2
x = x[choices]
y = y[choices]
curve_x = np.append(curve_x, x)
curve_y = np.append(curve_y, y)

park_path = np.vstack([curve_x, curve_y]).T
print(park_path.shape)

interpolated_park_path = interpolate_path(park_path, sample_rate=2)

# a = np.size(interpolated_park_path,0)
# print(a)

pt_x = []
pt_y = []

for i in  park_path:
    print(i[0])
    pt_x.append(i[0])

    pt_y.append(i[1])

print('pt_x',pt_x)

plt.plot(pt_x, pt_y,'o')
plt.show()