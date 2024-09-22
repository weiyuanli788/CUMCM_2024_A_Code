import numpy as np
from scipy.optimize import minimize

# 计算在给定半径处的把手速度
def speed_at_radius(v_head, radius, r0):
    return v_head * np.sqrt(radius / r0)

# 计算所有把手的最大速度
def max_handle_speed(v_head, spiral_radius, arc1_radius, arc2_radius, spiral_params):
    # 计算在螺旋路径上的最大速度
    max_speed_in_spiral = v_head * (spiral_radius / spiral_params['initial_radius'])
    
    # 计算在圆弧上的最大速度
    max_speed_in_arc1 = speed_at_radius(v_head, arc1_radius, arc1_radius)
    max_speed_in_arc2 = speed_at_radius(v_head, arc2_radius, arc2_radius / 2)
    
    return max(max_speed_in_spiral, max_speed_in_arc1, max_speed_in_arc2)

# 目标函数，确保把手的速度不超过2 m/s
def objective_function(v_head, spiral_params, arc1_radius, arc2_radius, v_max):
    max_speed = max_handle_speed(v_head, spiral_params['radius'], arc1_radius, arc2_radius, spiral_params)
    return (max_speed - v_max)**2

# ABC算法实现
def abc_algorithm(spiral_params, arc1_radius, arc2_radius, v_max, num_bees=20, num_iterations=100):
    np.random.seed(0)
    colony = np.random.uniform(0, v_max, num_bees)  # 初始化蜜蜂位置（速度）
    best_v_head = colony[0]
    best_score = objective_function(best_v_head, spiral_params, arc1_radius, arc2_radius, v_max)

    for _ in range(num_iterations):
        for i in range(num_bees):
            food_source = colony[i]
            
            phi = np.random.uniform(-1, 1)
            k = np.random.randint(num_bees)
            new_solution = colony[i] + phi * (colony[i] - colony[k])
            new_solution = np.clip(new_solution, 0, v_max)
            
            new_score = objective_function(new_solution, spiral_params, arc1_radius, arc2_radius, v_max)
            if new_score < best_score:
                best_v_head = new_solution
                best_score = new_score
                
            if new_score < objective_function(food_source, spiral_params, arc1_radius, arc2_radius, v_max):
                colony[i] = new_solution

    return best_v_head

# 初始化螺旋参数和圆弧半径
spiral_params = {
    'radius': 7.0,  # 螺旋半径的初始值，需要在实际应用中计算或优化
    'initial_radius': 7.0
}

arc1_radius = 6.879451574886364  # 从优化结果中得到的半径
arc2_radius = 3.439725787443182  # 从优化结果中得到的半径

v_max = 2.0  # m/s 最大把手速度

# 运行ABC算法求解最大龙头行进速度
max_v_head = abc_algorithm(spiral_params, arc1_radius, arc2_radius, v_max)

print(f"最大龙头行进速度: {max_v_head:.6f} m/s")
