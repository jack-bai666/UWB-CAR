import platform
print('系统:',platform.system())

import time
T1 = time.perf_counter()

#______假设下面是程序部分______
for i in range(100*100):
    pass

T2 =time.perf_counter()
print('程序运行时间:%s毫秒' % ((T2 - T1)*1000))