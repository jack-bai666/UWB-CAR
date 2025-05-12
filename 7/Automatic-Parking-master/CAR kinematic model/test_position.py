import socket
import ast

# 创建一个udp套件字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定本地相关信息，如果不绑定，则系统会随机分配，必须绑定本电脑的ip和port
local_addr = ('', 8080)  # 元组的第一个参数为本机IP，可以为空字符串，会自动生成本机IP
udp_socket.bind(local_addr)

def main_true():
    # 等待接收方发送数据
    # rs中存储的是一个元组（接收到的数据，（发送方的ip，port））
    while True:
        rs_data = udp_socket.recvfrom(1024)
        rs_masg = rs_data[0]
        rs_addr = rs_data[1]
        # print(rs_data)
        # 接收到的数据解码展示
        print(rs_masg.decode('utf-8'))
        # print(rs_addr)
        # 关闭套件字
        # udp_socket.close()

def getxy():            # 每28ms 输出一个标签的测距数据
    # 等待接收方发送数据
    # rs中存储的是一个元组（接收到的数据，（发送方的ip，port））

    rs_data = udp_socket.recvfrom(1024)
    rs_masg = rs_data[0]
    # rs_addr = rs_data[1]
    # print(rs_data)
    # 接收到的数据解码展示
    msg = rs_masg.decode('utf-8')
    print(msg)
    # print(type(msg))
    print("数据长度:",len(msg))

    x = ''
    y = ''
    j = 0

    for i in msg:           # 第40位：标签ID

        j = j+1
        if i == 'X':        # 第49位：X
            n = j + 3
            while msg[n] != ',':
                x = x + msg[n]
                n = n + 1

        if i == 'Y':        # 第49位：X
            n = j + 3
            while msg[n] != ',':
                y = y + msg[n]
                n = n + 1

    # print(rs_addr)
    # 关闭套件字
    id = int(msg[40])
    x = ast.literal_eval(x)
    y = ast.literal_eval(y)
    print(f'标签ID为{id}')
    print(f'X在消息的第{j}位,该位显示数据{i},X的坐标值位为{x}')
    print(f'Y在消息的第{j}位,该位显示数据{i},Y的坐标值位为{y}')

    return id, x, y

def socketclose():
    udp_socket.close()

if __name__ == '__main__':
    main_true()
    # getxy()
