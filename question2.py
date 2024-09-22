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
acceleration_time = 200  # 完全加速所需时间 (s)！重要参数，请根据身体素质数据修改！

# 每节板凳的启动时间
start_times = np.linspace(0, acceleration_time, num_sections)

# 初始化位置和速度
positions = np.zeros((num_sections, 2, len(time_points)))  # (x, y) positions
speeds = np.zeros((num_sections, len(time_points)))  # speeds

def calculate_speed(t, start_time):
    if t < start_time:
        return 0  # 在启动时间之前，速度为0
    return min(max_speed, (t - start_time) / acceleration_time * max_speed)

def calculate_position(x, y, speed, t):
    # 计算螺旋线位置
    angle = 2 * np.pi * (t / pitch)
    return x + speed * np.cos(angle) * t, y + speed * np.sin(angle) * t

def check_collision(positions, length):
    for i in range(1, num_sections):
        prev_end = positions[i-1, :, -1] + np.array([body_tail_length * np.cos(2 * np.pi * (300 / pitch)), body_tail_length * np.sin(2 * np.pi * (300 / pitch))])
        curr_start = positions[i, :, -1]
        distance = np.linalg.norm(prev_end - curr_start)
        if distance < length:
            return True
    return False

# 计算每秒的位置和速度
positions_list = []
speeds_list = []
termination_time = None

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

    # 计算龙尾后把手的位置和速度
    positions[num_sections - 1, :, i] = positions[num_sections - 2, :, i]
    speeds[num_sections - 1, i] = speeds[num_sections - 2, i]

    # 检查是否发生碰撞
    if check_collision(positions, body_tail_length):
        termination_time = t - 1
        break

    # 构建行数据
    position_row = {'Time': t}
    speed_row = {'Time': t}
    for j in range(num_sections):
        position_row[f'Section_{j}_x'] = positions[j, 0, i]
        position_row[f'Section_{j}_y'] = positions[j, 1, i]
        speed_row[f'Section_{j}_Speed'] = speeds[j, i]
    positions_list.append(position_row)
    speeds_list.append(speed_row)

# 处理终止时刻
if termination_time is not None:
    # 最后一秒的数据
    termination_index = np.where(time_points == termination_time)[0][0]
    termination_positions = positions[:, :, termination_index]
    termination_speeds = speeds[:, termination_index]
    
    # 创建终止时刻的数据帧
    termination_data = {'Time': termination_time}
    for j in range(num_sections):
        termination_data[f'Section_{j}_x'] = termination_positions[j, 0]
        termination_data[f'Section_{j}_y'] = termination_positions[j, 1]
        termination_data[f'Section_{j}_Speed'] = termination_speeds[j]
    
    termination_position_df = pd.DataFrame([termination_data])
    termination_speed_df = pd.DataFrame([termination_data])
    
    # 保存终止时刻的数据到Excel
    random_int = np.random.randint(0, 10000)
    termination_position_file = f'D:/dragon_termination_position_{random_int}.xlsx'
    termination_speed_file = f'D:/dragon_termination_speed_{random_int}.xlsx'
    
    termination_position_df.to_excel(termination_position_file, index=False)
    termination_speed_df.to_excel(termination_speed_file, index=False)
    
    print(f"Termination position data has been saved to {termination_position_file}.")
    print(f"Termination speed data has been saved to {termination_speed_file}.")
else:
    print("No collision detected within the specified time.")

# 保存所有时间的数据到Excel
random_int = np.random.randint(0, 10000)
position_file = f'D:/dragon_position_{random_int}.xlsx'
speed_file = f'D:/dragon_speed_{random_int}.xlsx'

position_df = pd.DataFrame(positions_list)
speed_df = pd.DataFrame(speeds_list)

position_df.to_excel(position_file, index=False)
speed_df.to_excel(speed_file, index=False)

print(f"Position data has been saved to {position_file}.")
print(f"Speed data has been saved to {speed_file}.")
