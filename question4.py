import numpy as np
import random
from scipy.optimize import minimize

# 目标函数
def objective_function(params):
    R1, x1, y1, x2, y2 = params
    arc1_length = np.pi * R1
    arc2_length = np.pi * (R1 / 2)
    total_length = arc1_length + arc2_length
    if not check_arc_tangent(x1, y1, R1, x2, y2, R1 / 2):
        return np.inf
    spiral_params = {}  # 使用实际螺旋线参数
    if not (check_arc_spiral_tangent(x1, y1, R1, spiral_params) and
            check_arc_spiral_tangent(x2, y2, R1 / 2, spiral_params)):
        return np.inf
    return total_length

def check_arc_tangent(x1, y1, R1, x2, y2, R2):
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return np.isclose(distance, R1 + R2, atol=1e-2)

def check_arc_spiral_tangent(x, y, R, spiral_params):
    # 这里应实现具体的检查逻辑
    return True

# 模拟退火算法
def simulated_annealing(particle, temp, cooling_rate):
    new_particle = particle + np.random.uniform(-1, 1, size=particle.shape)
    new_particle = np.clip(new_particle, bounds[:, 0], bounds[:, 1])
    delta = objective_function(new_particle)
    delta_old = objective_function(particle)
    if delta < delta_old or np.random.rand() < np.exp((delta_old - delta) / temp):
        return new_particle
    return particle

# 粒子群优化算法
def pso_algorithm(num_particles, num_iterations):
    global best_particle
    particles = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(num_particles, len(bounds)))
    velocities = np.random.uniform(-1, 1, size=(num_particles, len(bounds)))
    personal_best_particles = np.copy(particles)
    personal_best_scores = np.array([objective_function(p) for p in personal_best_particles])
    global_best_particle = personal_best_particles[np.argmin(personal_best_scores)]
    global_best_score = min(personal_best_scores)

    for iteration in range(num_iterations):
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = (0.5 * velocities[i] +
                             2 * r1 * (personal_best_particles[i] - particles[i]) +
                             2 * r2 * (global_best_particle - particles[i]))
            particles[i] = particles[i] + velocities[i]
            particles[i] = np.clip(particles[i], bounds[:, 0], bounds[:, 1])
            temp = 1.0 / (iteration + 1)  # 模拟退火温度逐渐降低
            particles[i] = simulated_annealing(particles[i], temp, 0.99)
            score = objective_function(particles[i])
            if score < personal_best_scores[i]:
                personal_best_particles[i] = particles[i]
                personal_best_scores[i] = score
            if score < global_best_score:
                global_best_particle = particles[i]
                global_best_score = score

    return global_best_particle, global_best_score

# 初始化和优化
def optimize_path():
    global bounds
    bounds = np.array([
        [4.5, 15],  # R1
        [-15, 15],  # x1
        [-15, 15],  # y1
        [-15, 15],  # x2
        [-15, 15]   # y2
    ])

    num_particles = 30
    num_iterations = 100

    best_particle, best_score = pso_algorithm(num_particles, num_iterations)
    
    R1, x1, y1, x2, y2 = best_particle
    print(f"Optimized Radius 1: {R1}")
    print(f"Optimized Center 1: ({x1}, {y1})")
    print(f"Optimized Radius 2: {R1 / 2}")
    print(f"Optimized Center 2: ({x2}, {y2})")
    print(f"Arc 1 Equation: (x - {x1})^2 + (y - {y1})^2 = {R1**2}")
    print(f"Arc 2 Equation: (x - {x2})^2 + (y - {y2})^2 = {(R1 / 2)**2}")
    print(f"Optimized Path Length: {best_score}")

    # 打印龙头的初始位置
    initial_position_x = x1 - R1
    initial_position_y = y1
    print(f"Dragon Head Initial Position: ({initial_position_x}, {initial_position_y})")

if __name__ == "__main__":
    optimize_path()
