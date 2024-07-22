import struct

def convert_to_signed_short(high_byte, low_byte):
    # 组合高低字节
    combined = (high_byte << 8) | low_byte
    # 使用 struct 模块将其转换为有符号的 short 类型
    signed_short = struct.unpack('h', struct.pack('H', combined))[0]
    return signed_short

def convert(file_path):

    # 初始化一个列表来存储转换后的结果
    converted_data = []

    # 打开并逐行读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 遍历每一条数据
    # 遍历每一条数据
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()  # 去除每行末尾的换行符和空格
        TL = int(line[16:18], 16)  # TL：低温度
        TH = int(line[18:20], 16)  # TH：高温度
        if len(line) < 22:
            converted_line = f"Invalid Data Format"
        else:
            prefix = line[0:4]  # 前四位为前缀
            # 根据第三到四位判断输出类型
            if line[2:4] == '50':
                # 时间转换输出
                YY = line[4:6]  # YY：年
                MM_str = line[6:8]  # MM：月（字符串形式）
                DD = line[8:10]  # DD：日
                HH = int(line[10:12], 16)  # HH：时（转换为整数）
                MM = int(line[12:14], 16)  # MM：分（转换为整数）
                SS = int(line[14:16], 16)  # SS：秒（转换为整数）
                MSL = int(line[16:18], 16)  # TL：低温度
                MSH = int(line[18:20], 16)  # TH：高温度
                MS=((MSH<<8)|MSL)
                YY=int(YY,16)+24
                # 计算和校验
                SUM = 0x55 + int(prefix, 16) + YY + int(MM_str, 16) + int(DD, 16) + HH + MM + SS + TL + TH
                
                # 格式化输出
                converted_line = f"日期: 20{YY}年 {int(MM_str, 16)}月 {DD}日 {HH}时 {MM}分 {SS}秒 {MS}毫秒"


            elif line[2:4] == '51':
                # 加速度转换输出
                AxL = int(line[4:6], 16)  # AxL：加速度 X 低字节
                AxH = int(line[6:8], 16)  # AxH：加速度 X 高字节
                AyL = int(line[8:10], 16)  # AyL：加速度 Y 低字节
                AyH = int(line[10:12], 16)  # AyH：加速度 Y 高字节
                AzL = int(line[12:14], 16)  # AzL：加速度 Z 低字节
                AzH = int(line[14:16], 16)  # AzH：加速度 Z 高字节

                # 计算加速度
                g = 9.8  # 重力加速度
                Ax = float(convert_to_signed_short(AxH, AxL)) / 32768.0 * 16 * g  # 加速度 X
                Ay = float(convert_to_signed_short(AyH, AyL)) / 32768.0 * 16 * g  # 加速度 Y
                Az = float(convert_to_signed_short(AzH, AzL)) / 32768.0 * 16 * g  # 加速度 Z
                # 计算和校验
                SUM = 0x55 + 0x51 + AxH + AxL + AyH + AyL + AzH + AzL + TL + TH
                
                # 加速度转换输出
                converted_line = f"加速度: ax:{Ax}m/s^2 ay:{Ay}m/s^2 az:{Az}m/s^2"
                # converted_line = f"0x55 0x51: 0x{SUM:X}"
            elif line[2:4] == '52':
                # 角速度转换输出
                wxL = int(line[4:6], 16)  # wxL：角速度 X 低字节
                wxH = int(line[6:8], 16)  # wxH：角速度 X 高字节
                wyL = int(line[8:10], 16)  # wyL：角速度 Y 低字节
                wyH = int(line[10:12], 16)  # wyH：角速度 Y 高字节
                wzL = int(line[12:14], 16)  # wzL：角速度 Z 低字节
                wzH = int(line[14:16], 16)  # wzH：角速度 Z 高字节
                
                # 计算角速度
                wx = ((wxH << 8) | wxL) / 32768 * 2000  # 角速度 X (°/s)
                wy = ((wyH << 8) | wyL) / 32768 * 2000  # 角速度 Y (°/s)
                wz = ((wzH << 8) | wzL) / 32768 * 2000  # 角速度 Z (°/s)
                T=((TH<<8)|TL) /100
                
                # 计算和校验
                SUM = 0x55 + 0x52 + wxH + wxL + wyH + wyL + wzH + wzL + TL + TH
                
                # 角速度转换输出
                converted_line = f"角速度: wx:{wx}°/s wy:{wy}°/s wz:{wz}°/s T:{T}℃"
                # converted_line = f"0x55 0x52: 0x{SUM:X}"
            elif line[2:4] == '53':
                # 角度转换输出
                RollL = int(line[4:6], 16)  # RollL：滚转角低字节
                RollH = int(line[6:8], 16)  # RollH：滚转角高字节
                PitchL = int(line[8:10], 16)  # PitchL：俯仰角低字节
                PitchH = int(line[10:12], 16)  # PitchH：俯仰角高字节
                YawL = int(line[12:14], 16)  # YawL：偏航角低字节
                YawH = int(line[14:16], 16)  # YawH：偏航角高字节
                # 处理滚转角

                # 计算角度
                Roll = ((RollH << 8) | RollL) / 32768 * 180  # 滚转角 (°)
                Pitch = ((PitchH << 8) | PitchL) / 32768 * 180  # 俯仰角 (°)
                Yaw = ((YawH << 8) | YawL) / 32768 * 180  # 偏航角 (°)
                T=((TH<<8)|TL) /100
                # 计算和校验
                if(Roll>180):
                    Roll=Roll-360
                if(Pitch>180):
                    Pitch=Pitch-360
                if(Yaw>180):
                    Yaw=Yaw-360
                SUM = 0x55 + 0x53 + RollH + RollL + PitchH + PitchL + YawH + YawL + TL + TH
                
                # 角度转换输出
                converted_line = f"角度： roll:{Roll}° Pitch:{Pitch}° Yaw:{Yaw}° T:{T}℃"
                # converted_line = f"0x55 0x53: 0x{SUM:X}"
            elif line[2:4] == '54':
                # 磁场转换输出
                HxL = int(line[4:6], 16)  # HxL：磁场 X 低字节
                HxH = int(line[6:8], 16)  # HxH：磁场 X 高字节
                HyL = int(line[8:10], 16)  # HyL：磁场 Y 低字节
                HyH = int(line[10:12], 16)  # HyH：磁场 Y 高字节
                HzL = int(line[12:14], 16)  # HzL：磁场 Z 低字节
                HzH = int(line[14:16], 16)  # HzH：磁场 Z 高字节
                
                # 计算磁场
                Hx = ((HxH << 8) | HxL)   # 磁场 X (uT)
                Hy = ((HyH << 8) | HyL)  # 磁场 Y (uT)
                Hz = ((HzH << 8) | HzL)   # 磁场 Z (uT)
                if Hz & 0x8000:
                    Hz = -((~Hz & 0xFFFF) + 1)
                if Hx & 0x8000:
                    Hx = -((~Hz & 0xFFFF) + 1)
                if Hy & 0x8000:
                    Hy = -((~Hz & 0xFFFF) + 1)
                T=((TH<<8)|TL) /100
                # 计算和校验
                SUM = 0x55 + 0x54 + HxH + HxL + HyH + HyL + HzH + HzL + TL + TH
                
                # 磁场转换输出
                converted_line = f"磁场: Hx:{Hx}uT Hy:{Hy}uT Hz:{Hz}uT T:{T}"
                # converted_line = f"0x55 0x54: 0x{SUM:X}"
            elif line[2:4]=='55':
                # 数据示例
                D0H = int(line[4:6], 16)
                D0L = int(line[6:8], 16)
                D1H = int(line[8:10], 16)
                D1L = int(line[10:12], 16)
                D2H = int(line[12:14], 16)
                D2L = int(line[14:16], 16)
                D3H = int(line[16:18], 16)
                D3L = int(line[18:20], 16)

                # 计算 Dx
                D0 = (D0H << 8) | D0L
                D1 = (D1H << 8) | D1L
                D2 = (D2H << 8) | D2L
                D3 = (D3H << 8) | D3L

                # 计算校验和
                SUM = 0x55 + 0x55 + D0 + D1 + D2 + D3
                converted_line = f"端口输出状态: D0:{D0} D1:{D1} D2:{D2} D3:{D3}"

            elif line[2:4]=='56':
                # 数据示例
                P0 = int(line[4:6], 16)
                P1 = int(line[6:8], 16)
                P2 = int(line[8:10], 16)
                P3 = int(line[10:12], 16)
                H0 = int(line[12:14], 16)
                H1 = int(line[14:16], 16)
                H2 = int(line[16:18], 16)
                H3 = int(line[18:20], 16)

                # 计算气压 P 和高度 H
                P = (P3 << 24) | (P2 << 16) | (P1 << 8) | P0
                H = (H3 << 24) | (H2 << 16) | (H1 << 8) | H0

                # 计算校验和
                SUM = 0x55 + 0x56 + P0 + P1 + P2 + P3 + H0 + H1 + H2 + H3
                converted_line = f"气压状态: P:{P} H:{H}"
            elif line[2:4]=='57':
                # 数据示例
                Lon0 = int(line[4:6], 16)
                Lon1 = int(line[6:8], 16)
                Lon2 = int(line[8:10], 16)
                Lon3 = int(line[10:12], 16)
                Lat0 = int(line[12:14], 16)
                Lat1 = int(line[14:16], 16)
                Lat2 = int(line[16:18], 16)
                Lat3 = int(line[18:20], 16)


                # 计算经度 Lon 和纬度 Lat
                Lon = (Lon3 << 24) | (Lon2 << 16) | (Lon1 << 8) | Lon0
                Lat = (Lat3 << 24) | (Lat2 << 16) | (Lat1 << 8) | Lat0

                # 计算校验和
                SUM = 0x55 + 0x57 + Lon0 + Lon1 + Lon2 + Lon3 + Lat0 + Lat1 + Lat2 + Lat3
                converted_line = f"经纬度: Lon:{Lon} Lat:{Lat}"

            else:
                converted_line = f"Invalid Type {line[2:4]}"
        
        converted_data.append(converted_line)


    # 将转换后的结果写入新文件
    output_file = 'converted_data.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in converted_data:
            file.write(line + '\n')

    print(f"转换完成，并将结果保存到 {output_file} 文件中。")
if __name__=="__main__":
    convert('data.txt')