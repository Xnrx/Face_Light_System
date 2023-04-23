import serial

# 打开串口
ser = serial.Serial('COM7', 9600) # 根据实际情况修改串口名称和波特率

# 接收并打印串口发送的全部信息
while True:
    if ser.in_waiting:
        data = ser.read_all()
        print(data.decode())

    # 输入循环，让用户输入什么就发送什么
    input_data = input("请输入要发送的数据（按 q 退出）：")
    if input_data == 'q':
        break
    ser.write(input_data.encode())

# 关闭串口
ser.close()
