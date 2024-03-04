import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def nearest_neighbor_tour(graph):
    # Start at a random city
    start_city = random.choice(list(graph.nodes()))
    current_city = start_city
    tour = [current_city]
    unvisited_cities = set(graph.nodes())
    unvisited_cities.remove(current_city)
    
    # Repeat until all cities are visited
    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: graph[current_city][city]['weight'])
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city
    
    # Return to the starting city to complete the tour
    tour.append(start_city)
    
    return tour

def christofides_tour(graph):
    # Step 1: Construct Minimum Spanning Tree (MST)
    mst = nx.minimum_spanning_tree(graph)
    
    # Step 2: Find Minimum Weight Perfect Matching of odd-degree vertices in MST
    odd_degree_vertices = [v for v in mst.nodes() if mst.degree(v) % 2 != 0]
    perfect_matching = nx.max_weight_matching(mst, maxcardinality=True)
    
    # Step 3: Combine MST and Matching to form a Multigraph
    multigraph = mst.copy()
    for u, v in perfect_matching:
        multigraph.add_edge(u, v, weight=graph[u][v]['weight'])
    
    # Ensure the multigraph has an Eulerian circuit
    eulerian_multigraph = nx.eulerize(multigraph)
    
    # Step 4: Find Eulerian Circuit in Multigraph
    eulerian_circuit = list(nx.eulerian_circuit(eulerian_multigraph))
    
    # Step 5: Convert Eulerian Circuit to Hamiltonian Circuit (Tour) by Shortcutting
    tour = [eulerian_circuit[0][0]]
    for u, v in eulerian_circuit:
        if v not in tour:
            tour.append(v)
    
    # Return to the starting city to complete the tour
    tour.append(tour[0])
    
    return tour

# Example usage
if __name__ == "__main__":
    # Generate a random graph with 10 cities
    num_cities = 10
    np.random.seed(42)
    coordinates = np.random.rand(num_cities, 2)
    distances = np.linalg.norm(coordinates[:, np.newaxis] - coordinates[np.newaxis, :], axis=-1)
    graph = nx.from_numpy_array(distances)
    
    # Assign random weights to edges
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.randint(1, 100)
    
    # Solve TSP using Nearest Neighbor Algorithm
    nn_tour = nearest_neighbor_tour(graph)
    nn_tour_length = sum(graph[nn_tour[i]][nn_tour[i+1]]['weight'] for i in range(len(nn_tour) - 1))
    print("Nearest Neighbor Tour:", nn_tour)
    print("Nearest Neighbor Tour Length:", nn_tour_length)
    
    # Solve TSP using Christofides Algorithm
    christofides_tour = christofides_tour(graph)
    christofides_tour_length = sum(graph[christofides_tour[i]][christofides_tour[i+1]]['weight'] for i in range(len(christofides_tour) - 1))
    print("Christofides Tour:", christofides_tour)
    print("Christofides Tour Length:", christofides_tour_length)
    
    # Plot the graph and tours
    plt.figure(figsize=(8, 6))
    pos = {i: coordinates[i] for i in range(num_cities)}
    nx.draw(graph, pos, with_labels=True, node_size=300)
    nx.draw_networkx_edges(graph, pos, edgelist=[(nn_tour[i], nn_tour[i+1]) for i in range(len(nn_tour) - 1)], edge_color='r', width=2, label='Nearest Neighbor Tour')
    nx.draw_networkx_edges(graph, pos, edgelist=[(christofides_tour[i], christofides_tour[i+1]) for i in range(len(christofides_tour) - 1)], edge_color='b', width=2, label='Christofides Tour')
    plt.title("Traveling Salesman Problem")
    plt.legend()
    plt.show()
