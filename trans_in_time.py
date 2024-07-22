import serial
import struct
import time

def convert_to_signed_short(high_byte, low_byte):
    combined = (high_byte << 8) | low_byte
    signed_short = struct.unpack('h', struct.pack('H', combined))[0]
    return signed_short

def process_line(line):
    line = line.strip()  # 去除每行末尾的换行符和空格
    TL = int(line[16:18], 16)  # TL：低温度
    TH = int(line[18:20], 16)  # TH：高温度
    
    if len(line) < 22:
        return "Invalid Data Format"
    
    prefix = line[0:4]  # 前四位为前缀
    result = ""

    if line[2:4] == '50':
        YY = line[4:6]
        MM_str = line[6:8]
        DD = line[8:10]
        HH = int(line[10:12], 16)
        MM = int(line[12:14], 16)
        SS = int(line[14:16], 16)
        MSL = int(line[16:18], 16)
        MSH = int(line[18:20], 16)
        MS = ((MSH << 8) | MSL)
        YY = int(YY, 16) + 24
        result = f"日期: 20{YY}年 {int(MM_str, 16)}月 {DD}日 {HH}时 {MM}分 {SS}秒 {MS}毫秒"
        
    elif line[2:4] == '51':
        AxL = int(line[4:6], 16)
        AxH = int(line[6:8], 16)
        AyL = int(line[8:10], 16)
        AyH = int(line[10:12], 16)
        AzL = int(line[12:14], 16)
        AzH = int(line[14:16], 16)
        g = 9.8
        Ax = float(convert_to_signed_short(AxH, AxL)) / 32768.0 * 16 * g
        Ay = float(convert_to_signed_short(AyH, AyL)) / 32768.0 * 16 * g
        Az = float(convert_to_signed_short(AzH, AzL)) / 32768.0 * 16 * g
        result = f"加速度: ax:{Ax}m/s^2 ay:{Ay}m/s^2 az:{Az}m/s^2"
        
    elif line[2:4] == '52':
        wxL = int(line[4:6], 16)
        wxH = int(line[6:8], 16)
        wyL = int(line[8:10], 16)
        wyH = int(line[10:12], 16)
        wzL = int(line[12:14], 16)
        wzH = int(line[14:16], 16)
        wx = ((wxH << 8) | wxL) / 32768 * 2000
        wy = ((wyH << 8) | wyL) / 32768 * 2000
        wz = ((wzH << 8) | wzL) / 32768 * 2000
        T = ((TH << 8) | TL) / 100
        result = f"角速度: wx:{wx}°/s wy:{wy}°/s wz:{wz}°/s T:{T}℃"
        
    elif line[2:4] == '53':
        RollL = int(line[4:6], 16)
        RollH = int(line[6:8], 16)
        PitchL = int(line[8:10], 16)
        PitchH = int(line[10:12], 16)
        YawL = int(line[12:14], 16)
        YawH = int(line[14:16], 16)
        Roll = ((RollH << 8) | RollL) / 32768 * 180
        Pitch = ((PitchH << 8) | PitchL) / 32768 * 180
        Yaw = ((YawH << 8) | YawL) / 32768 * 180
        T = ((TH << 8) | TL) / 100
        if Roll > 180:
            Roll -= 360
        if Pitch > 180:
            Pitch -= 360
        if Yaw > 180:
            Yaw -= 360
        result = f"角度： roll:{Roll}° Pitch:{Pitch}° Yaw:{Yaw}° T:{T}℃"
        
    elif line[2:4] == '54':
        HxL = int(line[4:6], 16)
        HxH = int(line[6:8], 16)
        HyL = int(line[8:10], 16)
        HyH = int(line[10:12], 16)
        HzL = int(line[12:14], 16)
        HzH = int(line[14:16], 16)
        Hx = ((HxH << 8) | HxL)
        Hy = ((HyH << 8) | HyL)
        Hz = ((HzH << 8) | HzL)
        if Hz & 0x8000:
            Hz = -((~Hz & 0xFFFF) + 1)
        if Hx & 0x8000:
            Hx = -((~Hx & 0xFFFF) + 1)
        if Hy & 0x8000:
            Hy = -((~Hy & 0xFFFF) + 1)
        T = ((TH << 8) | TL) / 100
        result = f"磁场: Hx:{Hx}uT Hy:{Hy}uT Hz:{Hz}uT T:{T}"
        
    elif line[2:4] == '55':
        D0H = int(line[4:6], 16)
        D0L = int(line[6:8], 16)
        D1H = int(line[8:10], 16)
        D1L = int(line[10:12], 16)
        D2H = int(line[12:14], 16)
        D2L = int(line[14:16], 16)
        D3H = int(line[16:18], 16)
        D3L = int(line[18:20], 16)
        D0 = (D0H << 8) | D0L
        D1 = (D1H << 8) | D1L
        D2 = (D2H << 8) | D2L
        D3 = (D3H << 8) | D3L
        result = f"端口输出状态: D0:{D0} D1:{D1} D2:{D2} D3:{D3}"
        
    elif line[2:4] == '56':
        P0 = int(line[4:6], 16)
        P1 = int(line[6:8], 16)
        P2 = int(line[8:10], 16)
        P3 = int(line[10:12], 16)
        H0 = int(line[12:14], 16)
        H1 = int(line[14:16], 16)
        H2 = int(line[16:18], 16)
        H3 = int(line[18:20], 16)
        P = (P3 << 24) | (P2 << 16) | (P1 << 8) | P0
        H = (H3 << 24) | (H2 << 16) | (H1 << 8) | H0
        result = f"气压状态: P:{P} H:{H}"
        
    elif line[2:4] == '57':
        Lon0 = int(line[4:6], 16)
        Lon1 = int(line[6:8], 16)
        Lon2 = int(line[8:10], 16)
        Lon3 = int(line[10:12], 16)
        Lat0 = int(line[12:14], 16)
        Lat1 = int(line[14:16], 16)
        Lat2 = int(line[16:18], 16)
        Lat3 = int(line[18:20], 16)
        Lon = (Lon3 << 24) | (Lon2 << 16) | (Lon1 << 8) | Lon0
        Lat = (Lat3 << 24) | (Lat2 << 16) | (Lat1 << 8) | Lat0
        result = f"位置: Lon:{Lon} Lat:{Lat}"
        
    elif line[2:4] == '58':
        VEL0 = int(line[4:6], 16)
        VEL1 = int(line[6:8], 16)
        VEL2 = int(line[8:10], 16)
        VEL3 = int(line[10:12], 16)
        YAW0 = int(line[12:14], 16)
        YAW1 = int(line[14:16], 16)
        VEL = (VEL3 << 24) | (VEL2 << 16) | (VEL1 << 8) | VEL0
        YAW = (YAW1 << 8) | YAW0
        result = f"速度状态: VEL:{VEL} YAW:{YAW}"
        
    else:
        result = "Invalid Data"

    return result

def read_from_serial(serial_port):
    with serial.Serial(serial_port, 9600, timeout=1) as ser:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    processed_data = process_line(line)
                    print(processed_data)
                    # 这里可以根据需要将processed_data写回串口
                    # ser.write(processed_data.encode('utf-8'))

if __name__ == "__main__":
    serial_port = 'COM3'  # 更改为实际的串口端口号
    read_from_serial(serial_port)
