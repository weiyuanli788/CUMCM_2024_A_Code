#变异与交叉示意图

import matplotlib.pyplot as plt
import numpy as np

def plot_mutation_crossover():
    generations = 100
    num_individuals = 50
    mutations = np.random.uniform(0, 1, (generations, num_individuals))
    crossovers = np.random.uniform(0, 1, (generations, num_individuals))
    
    plt.figure(figsize=(12, 8))
    plt.plot(np.mean(mutations, axis=1), label='Average Mutation Strength', color='r')
    plt.plot(np.mean(crossovers, axis=1), label='Average Crossover Rate', color='b')
    plt.xlabel('Generation')
    plt.ylabel('Value')
    plt.title('变异与交叉示意图')
    plt.legend()
    plt.grid(True)
    plt.savefig('mutation_crossover.png')
    plt.show()

if __name__ == "__main__":
    plot_mutation_crossover()
