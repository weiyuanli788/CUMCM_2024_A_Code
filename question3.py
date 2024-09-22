#最终：最小螺距：0.965235 米
def mutate(individual, mutation_rate, pitch_min, pitch_max, mutation_strength=0.05):
    if np.random.rand() < mutation_rate:
        return np.clip(individual + np.random.uniform(-mutation_strength, mutation_strength), pitch_min, pitch_max)
    return individual

# 遗传算法主程序
def genetic_algorithm(pop_size, pitch_min, pitch_max, generations, mutation_rate, mutation_strength=0.05):
    population = initialize_population(pop_size, pitch_min, pitch_max)
    
    for generation in range(generations):
        scores = np.array([objective_function(ind[0]) for ind in population])
        best_score_index = np.argmin(scores)
        best_pitch = population[best_score_index][0]
        
        # 选择最好的个体
        selected_population = tournament_selection(population, scores)
        
        # 生成新种群
        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = selected_population[np.random.choice(len(selected_population), 2, replace=False)]
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, pitch_min, pitch_max, mutation_strength)
            new_population.append(child)
        
        population = np.array(new_population).reshape(-1, 1)
    
    # 最终的最优解
    scores = np.array([objective_function(ind[0]) for ind in population])
    best_score_index = np.argmin(scores)
    best_pitch = population[best_score_index][0]
    
    return best_pitch

# 主程序
if __name__ == "__main__":
    pop_size = 50  # 种群大小
    pitch_min = 0.5  # 最小螺距
    pitch_max = 1.7  # 最大螺距
    generations = 100  # 代数
    mutation_rate = 0.1  # 变异率
    mutation_strength = 0.1  # 变异强度

    optimal_pitch = genetic_algorithm(pop_size, pitch_min, pitch_max, generations, mutation_rate, mutation_strength)
    
    print(f"最小螺距：{optimal_pitch:.6f} 米")
