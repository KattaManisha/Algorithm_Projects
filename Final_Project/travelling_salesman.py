import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_random_graph(num_cities):
    np.random.seed(42)
    coordinates = np.random.rand(num_cities, 2)
    distances = np.linalg.norm(coordinates[:, np.newaxis] - coordinates[np.newaxis, :], axis=-1)
    graph = nx.from_numpy_array(distances)
    return graph, coordinates

def assign_random_weights(graph):
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.randint(1, 100)

def nearest_neighbor_tour(graph):
    start_city = random.choice(list(graph.nodes()))
    current_city = start_city
    tour = [current_city]
    unvisited_cities = set(graph.nodes())
    unvisited_cities.remove(current_city)
    
    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: graph[current_city][city]['weight'])
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city
    
    tour.append(start_city)
    return tour

def christofides_solution(graph):
    mst = nx.minimum_spanning_tree(graph)
    odd_degree_vertices = [v for v in mst.nodes() if mst.degree(v) % 2 != 0]
    perfect_matching = nx.max_weight_matching(mst, maxcardinality=True)
    multigraph = mst.copy()
    for u, v in perfect_matching:
        multigraph.add_edge(u, v, weight=graph[u][v]['weight'])
    
    eulerian_multigraph = nx.eulerize(multigraph)
    eulerian_circuit = list(nx.eulerian_circuit(eulerian_multigraph))
    
    tour = [eulerian_circuit[0][0]]
    for u, v in eulerian_circuit:
        if v not in tour:
            tour.append(v)
    
    tour.append(tour[0])
    return tour

def calculate_tour_length(tour, graph):
    tour_length = sum(graph[tour[i]][tour[i+1]]['weight'] for i in range(len(tour) - 1))
    return tour_length

def plot_graph_with_tours(graph, coordinates, nn_tour, christofides_tour, nn_tour_length, christofides_tour_length, num_cities):
    plt.figure(figsize=(8, 6))
    pos = {i: coordinates[i] for i in range(len(coordinates))}
    nx.draw(graph, pos, with_labels=True, node_size=300)
    nx.draw_networkx_edges(graph, pos, edgelist=[(nn_tour[i], nn_tour[i+1]) for i in range(len(nn_tour) - 1)], edge_color='r', width=2, label=f'Nearest Neighbor Tour (Length: {nn_tour_length})')
    nx.draw_networkx_edges(graph, pos, edgelist=[(christofides_tour[i], christofides_tour[i+1]) for i in range(len(christofides_tour) - 1)], edge_color='b', width=2, label=f'Christofides Tour (Length: {christofides_tour_length})')
    plt.title(f"Traveling Salesman Problem - Experiment for {num_cities} cities")
    plt.legend(loc='upper right')
    plt.show()

# Experiment settings
num_cities_list = [5, 10, 15]  # Varying number of cities for experimentation

for num_cities in num_cities_list:
    print(f"Experimenting with {num_cities} cities:")
    graph, coordinates = generate_random_graph(num_cities)
    assign_random_weights(graph)
    
    nn_tour = nearest_neighbor_tour(graph)
    nn_tour_length = calculate_tour_length(nn_tour, graph)
    
    print("Nearest Neighbor Tour:", nn_tour)
    print("Nearest Neighbor Tour Length:", nn_tour_length)
    
    christofides_tour = christofides_solution(graph)
    christofides_tour_length = calculate_tour_length(christofides_tour, graph)
    print("Christofides Tour:", christofides_tour)
    print("Christofides Tour Length:", christofides_tour_length)
    
    plot_graph_with_tours(graph, coordinates, nn_tour, christofides_tour, nn_tour_length, christofides_tour_length, num_cities)
