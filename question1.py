###问题一位置的代码
# 参数设置
        return 0  # 在启动时间之前，速度为0
    return min(max_speed, (t - start_time) / acceleration_time * max_speed)

def calculate_position(x, y, speed, t):
    # 计算螺旋线位置
    angle = 2 * np.pi * (t / pitch)
    return x + speed * np.cos(angle) * t, y + speed * np.sin(angle) * t

# 计算每秒的位置和速度
positions_list = []
speeds_list = []

for i, t in enumerate(time_points):
    # 计算龙头的位置和速度
    head_speed_current = head_speed  # 龙头速度保持不变
    head_position = calculate_position(initial_head_position[0], initial_head_position[1], head_speed_current, t)
    speeds[0, i] = head_speed_current
    positions[0, :, i] = head_position

    for j in range(1, num_sections):
        # 计算每节板凳的速度
        start_time = start_times[j]
        current_speed = calculate_speed(t, start_time)
        speeds[j, i] = current_speed

        # 计算每节板凳的位置
        prev_position = positions[j-1, :, i]
        angle_j = 2 * np.pi * (t / pitch)  # 修正角度计算
        positions[j, :, i] = prev_position + np.array([body_tail_length * np.cos(angle_j), body_tail_length * np.sin(angle_j)])

    # 计算龙尾后把手的速度
    if i > 0:
        # 直接计算第224节板凳作为新的龙尾的数据
        start_time = start_times[num_sections - 1]
        speeds[num_sections, i] = calculate_speed(t, start_time)
        
        # 计算第224节板凳的位置
        prev_position = positions[num_sections - 1, :, i]
        angle_j = 2 * np.pi * (t / pitch)  # 修正角度计算
        positions[num_sections, :, i] = prev_position + np.array([body_tail_length * np.cos(angle_j), body_tail_length * np.sin(angle_j)])

    # 构建行数据
    position_row = {'Time': t}
    speed_row = {'Time': t}
    for j in range(num_sections + 1):
        position_row[f'Section_{j}_x'] = positions[j, 0, i]
        position_row[f'Section_{j}_y'] = positions[j, 1, i]
        speed_row[f'Section_{j}_Speed'] = speeds[j, i]
    positions_list.append(position_row)
    speeds_list.append(speed_row)

# 创建DataFrame
position_df = pd.DataFrame(positions_list)
speed_df = pd.DataFrame(speeds_list)

# 生成随机整数以避免文件名冲突
random_int = np.random.randint(0, 10000)
position_file = f'D:/dragon_position_{random_int}.xlsx'
speed_file = f'D:/dragon_speed_{random_int}.xlsx'

# 保存到Excel文件
position_df.to_excel(position_file, index=False)
speed_df.to_excel(speed_file, index=False)

print(f"Position data has been saved to {position_file}.")
print(f"Speed data has been saved to {speed_file}.")
###问题一速度的代码
import numpy as np
import pandas as pd

# 参数设置
num_sections = 224  # 包括龙头、龙身、龙尾以及龙尾后把手
initial_head_position = np.array([8.8, 0])  # 龙头的初始位置
head_speed = 1.0  # 龙头的速度 (m/s)
pitch = 0.55  # 螺距 (m)
time_points = np.arange(0, 301, 1)  # 从0到300秒的时间点

# 板凳的长度
head_length = 3.41  # 龙头板凳长度 (m)
body_tail_length = 2.2  # 龙身和龙尾板凳长度 (m)

# 速度加速参数
max_speed = 1.0  # 最大速度 (m/s)
acceleration_time = 200  # 修改为基于平均加速时间的加速时间 (s)

# 每节板凳的启动时间
start_times = np.linspace(0, acceleration_time, num_sections)

# 初始化位置和速度
positions = np.zeros((num_sections + 1, 2, len(time_points)))  # (x, y) positions, including Dragon Tail Rear
speeds = np.zeros((num_sections + 1, len(time_points)))  # speeds, including Dragon Tail Rear

# 计算速度函数
def calculate_speed(t, start_time):
    if t < start_time:
        return 0  # 在启动时间之前，速度为0
    return max_speed * (1 - np.exp(-(t - start_time) / acceleration_time))

# 计算螺旋线位置函数
def calculate_spiral_position(initial_radius, t, current_radius):
    angle = 2 * np.pi * (t / pitch)
    radius = max(0, current_radius - head_speed * t)  # 确保半径不为负数
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return x, y

# 计算每秒的位置和速度
positions_list = []
speeds_list = []

for i, t in enumerate(time_points):
    # 计算龙头的位置和速度
    head_position = calculate_spiral_position(np.linalg.norm(initial_head_position), t, np.linalg.norm(initial_head_position))
    head_speed_current = head_speed  # 龙头速度保持不变
    speeds[0, i] = round(head_speed_current, 6)
    positions[0, :, i] = [round(coord, 6) for coord in head_position]

    for j in range(1, num_sections):
        # 计算每节板凳的速度
        start_time = start_times[j]
        current_speed = calculate_speed(t, start_time)
        speeds[j, i] = round(current_speed, 6)

        # 计算每节板凳的位置
        if t < start_time:
            # 在启动时间之前位置保持不变
            positions[j, :, i] = positions[j-1, :, i]
        else:
            prev_position = positions[j-1, :, i]
            distance_from_prev = body_tail_length
            current_radius = np.linalg.norm(prev_position) - distance_from_prev
            if current_radius < 0:
                current_radius = 0  # 确保半径不为负数
            
            # 计算螺旋线的位置
            positions[j, :, i] = [round(coord, 6) for coord in calculate_spiral_position(current_radius, t, current_radius)]

    # 计算龙尾后把手的速度
    if i > 0:
        start_time = start_times[num_sections - 1]
        speeds[num_sections, i] = round(calculate_speed(t, start_time), 6)
        
        # 计算第224节板凳的位置
        prev_position = positions[num_sections - 1, :, i]
        current_radius = np.linalg.norm(prev_position) - body_tail_length
        if current_radius < 0:
            current_radius = 0  # 确保半径不为负数
        positions[num_sections, :, i] = [round(coord, 6) for coord in calculate_spiral_position(current_radius, t, current_radius)]

    # 构建行数据
    position_row = {'Time': round(t, 6)}
    speed_row = {'Time': round(t, 6)}
    for j in range(num_sections + 1):
        position_row[f'Section_{j}_x'] = round(positions[j, 0, i], 6)
        position_row[f'Section_{j}_y'] = round(positions[j, 1, i], 6)
        speed_row[f'Section_{j}_Speed'] = round(speeds[j, i], 6)
    positions_list.append(position_row)
    speeds_list.append(speed_row)

# 创建DataFrame
position_df = pd.DataFrame(positions_list)
speed_df = pd.DataFrame(speeds_list)

# 生成随机整数以避免文件名冲突
random_int = np.random.randint(0, 10000)
position_file = f'D:/dragon_position_{random_int}.xlsx'
speed_file = f'D:/dragon_speed_{random_int}.xlsx'

# 保存到Excel文件
position_df.to_excel(position_file, index=False)
speed_df.to_excel(speed_file, index=False)
