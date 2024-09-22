#个体分布图
import matplotlib.pyplot as plt
import numpy as np

def plot_population_distribution():
    generations = 100
    population_size = 50
    fitness_values = np.random.uniform(0, 1, (generations, population_size))
    
    plt.figure(figsize=(12, 8))
    plt.imshow(fitness_values.T, aspect='auto', cmap='viridis', origin='lower')
    plt.colorbar(label='Fitness Value')
    plt.xlabel('Generation')
    plt.ylabel('Individual')
    plt.title('个体分布图')
    plt.savefig('D://population_distribution.png')
    plt.show()

if __name__ == "__main__":
    plot_population_distribution()
