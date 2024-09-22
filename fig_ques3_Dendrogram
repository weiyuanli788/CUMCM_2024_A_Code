#遗传算法迭代过程的树状图

import matplotlib.pyplot as plt
import networkx as nx

def generate_genetic_tree(generations=4):
    G = nx.DiGraph()
    
    for generation in range(generations):
        num_individuals = 2 ** generation
        for i in range(num_individuals):
            node = f'{generation}_{i}'
            G.add_node(node, generation=generation)
            
            if generation > 0:
                parent = f'{generation-1}_{i//2}'
                G.add_edge(parent, node)
                
    return G

def draw_genetic_tree(G):
    pos = nx.spring_layout(G, seed=42)
    labels = {node: node for node in G.nodes()}
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray', arrows=True)
    plt.title('Genetic Algorithm Iterations Tree')
    plt.grid(True)
    plt.savefig('D://genetic_algorithm_tree1.png')
    plt.show()

if __name__ == "__main__":
    G = generate_genetic_tree(generations=4)
    draw_genetic_tree(G)
