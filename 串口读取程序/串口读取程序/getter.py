import serial
import trans as t
def read_serial_data(port, baudrate, output_file):
    # 打开串口
    ser = serial.Serial(port, baudrate, timeout=1)

    try:
        with open(output_file, 'w') as f:
            while True:
                # 读取串口数据
                data = ser.read(11)  # 读取16字节的数据，可以根据需要调整
                if data:
                    # 将数据转换为十六进制格式
                    hex_data = data.hex()
                    # print(f"Received Hex Data: {hex_data}")
                    # 将数据写入文件
                    
                    f.write(hex_data + '\n')
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        # 关闭串口
        ser.close()


if __name__ == "__main__":
    # 指定串口和波特率
    port = 'COM9'  # 根据实际情况修改
    baudrate = 9600  # 根据实际情况修改
    output_file = 'data.txt'  # 输出文件

    read_serial_data(port, baudrate, output_file)
    t.convert('data.txt')





