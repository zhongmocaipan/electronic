import tkinter as tk
from tkinter import scrolledtext
import serial
import threading
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# 全局变量用于保存数据
data_buffer = []
text_data_buffer = []
ser = None  # 全局串口对象

def read_serial_data(port, baudrate):
    global data_buffer, text_data_buffer, ser
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud.")
    except serial.SerialException as e:
        print(f"Could not open port {port}: {e}")
        return
    
    try:
        while True:
            data = ser.read(128)  # 假设每次读取128字节
            if data:
                process_data(data)

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        ser.close()

def process_data(data):
    global data_buffer, text_data_buffer
    int_data = []
    hex_data = []
    for i in range(0, len(data), 4):  # 每4个字节为一个整数
        if i + 4 <= len(data):
            value = int.from_bytes(data[i:i+4], byteorder='big', signed=True)
            int_value = value / 100  # 转换为实际值
            int_data.append(int_value)
            hex_data.append(f"{value:08X}")  # 转换为十六进制字符串
            
    # 将数据追加到缓冲区
    data_buffer.extend(int_data)
    text_data_buffer.extend(hex_data)
    
    if len(data_buffer) > 100:  # 限制缓冲区长度
        data_buffer = data_buffer[-100:]
    if len(text_data_buffer) > 100:
        text_data_buffer = text_data_buffer[-100:]

def update_plot(canvas, ax):
    global data_buffer
    ax.clear()
    ax.plot(data_buffer, label='Serial Data')
    ax.set_xlabel('Samples')
    ax.set_ylabel('Value')
    ax.set_title('Real-time Data')
    ax.set_ylim(-180, 180)  # 设置 y 轴范围
    ax.legend()
    canvas.draw()

def update_text(text_area):
    global text_data_buffer
    text_area.delete(1.0, tk.END)
    for line in text_data_buffer:
        # 计算十进制数
        int_value = int(line, 16)  # 将十六进制字符串转换为整数
        text_area.insert(tk.END, f"{line} ({int_value/100})\n")

def send_data(data_str):
    global ser
    if ser and ser.is_open:
        try:
            # 将输入的二进制字符串转换为二进制数据
            if len(data_str) % 8 == 0 and all(c in '01' for c in data_str):
                binary_data = int(data_str, 2).to_bytes(len(data_str) // 8, byteorder='big')
                ser.write(binary_data)  # 发送二进制数据
                print(f"Sent binary data: {data_str}")
            else:
                print("Invalid binary data length or characters. Ensure data length is a multiple of 8 bits and contains only '0' and '1'.")
        except Exception as e:
            print(f"Error sending data: {e}")
    else:
        print("Serial port not open.")

def send_go():
    send_data('00000001')

def send_stop():
    send_data('00000000')

def start_reading(port, baudrate):
    thread = threading.Thread(target=read_serial_data, args=(port, baudrate))
    thread.daemon = True
    thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Serial Data Reader with Plot")

    # 创建一个 matplotlib 图形
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=10, padx=10)
    
    # 创建一个滚动文本区域用于显示数据
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
    text_area.pack(pady=10, padx=10)

    # 创建一个文本框用于输入要发送的数据（十六进制）
    data_entry = tk.Entry(root, width=50, font=("Arial", 12))
    data_entry.pack(pady=10, padx=10)

    # 创建发送数据按钮
    send_hex_button = tk.Button(root, text="Send Hex Data", command=lambda: send_data(data_entry.get().strip()))
    send_hex_button.pack(pady=10, padx=10)

    # 创建发送十进制数据按钮
    send_decimal_button = tk.Button(root, text="Send Decimal Data", command=lambda: send_data(format(int(data_entry.get().strip()), '08b')))
    send_decimal_button.pack(pady=10, padx=10)

    # 创建发送二进制数据按钮
    send_binary_button = tk.Button(root, text="Send Binary Data", command=lambda: send_data(data_entry.get().strip()))
    send_binary_button.pack(pady=10, padx=10)

    # 创建 Go 按钮，设置为红色
    go_button = tk.Button(root, text="Go", command=send_go, bg='red', fg='white')
    go_button.pack(pady=10, padx=10)

    # 创建 Stop 按钮，设置为绿色
    stop_button = tk.Button(root, text="Stop", command=send_stop, bg='green', fg='white')
    stop_button.pack(pady=10, padx=10)

    def update_plot_periodically():
        update_plot(canvas, ax)
        update_text(text_area)
        root.after(100, update_plot_periodically)  # 每100毫秒更新一次图表和文本区域

    # 启动串口读取线程
    start_reading('COM17', 9600)
    
    # 启动定时更新图表和文本区域
    update_plot_periodically()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
