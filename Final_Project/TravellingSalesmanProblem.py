import networkx as nx
import random
import pandas as pd
from geopy.distance import geodesic
import folium
import branca
import time

# Function to calculate distance between two cities
def calculate_distance(city1, city2):
    return geodesic(city1, city2).kilometers

# Nearest Neighbor algorithm for TSP
def nearest_neighbor_tsp(graph, start_city):
    tour = [start_city]
    current_city = start_city
    visited_cities = set([start_city])  # Keep track of visited cities
    iterations = 0  # Initialize iteration counter
    
    while len(tour) < len(graph.nodes):
        next_city = min((city for city in graph[current_city] if city not in visited_cities),
                        key=lambda x: graph[current_city][x]['weight'])
        tour.append(next_city)
        visited_cities.add(next_city)  # Mark the next city as visited
        current_city = next_city
        iterations += 1  # Increment iteration counter
    
    return tour, iterations

# Christofides algorithm for TSP
def christofides_tsp(graph):
    mst = nx.minimum_spanning_tree(graph)
    odd_degree_vertices = [v for v in mst.nodes() if mst.degree(v) % 2 != 0]
    perfect_matching = nx.max_weight_matching(mst, maxcardinality=True)
    multigraph = mst.copy()
    for u, v in perfect_matching:
        multigraph.add_edge(u, v, weight=graph[u][v]['weight'])
    
    eulerian_multigraph = nx.eulerize(multigraph)
    eulerian_circuit = list(nx.eulerian_circuit(eulerian_multigraph))
    
    tour = [eulerian_circuit[0][0]]
    iterations = 0  # Initialize iteration counter
    
    for u, v in eulerian_circuit:
        if v not in tour:
            tour.append(v)
            iterations += 1  # Increment iteration counter
    
    return tour, iterations

# Read the CSV file with US cities data
df = pd.read_csv('E:/PSU/Algorithm/Algorithm_Projects/Final_Project/uscities.csv')  

# Function to randomly select cities from the DataFrame
def select_random_cities(df, num_cities):
    return random.sample(df['city'].tolist(), num_cities)

# Create graph with distances between cities
def create_graph_with_distances(df, cities):
    graph = nx.Graph()
    for city1 in cities:
        for city2 in cities:
            if city1 != city2:
                distance = calculate_distance((df.loc[df['city'] == city1, 'lat'].iloc[0], df.loc[df['city'] == city1, 'lng'].iloc[0]),
                                              (df.loc[df['city'] == city2, 'lat'].iloc[0], df.loc[df['city'] == city2, 'lng'].iloc[0]))
                graph.add_edge(city1, city2, weight=distance)
    return graph

# Function to plot selected cities on the map
def plot_selected_cities_on_map(cities, df):
    map = folium.Map(location=[37.0902, -95.7129], zoom_start=5)  # Centered around US

    # Add cities to the map
    for city in cities:
        try:
            city_info = df[df['city'] == city].iloc[0]
            label = f"{city_info['city']}"
            folium.Marker([city_info['lat'], city_info['lng']], popup=label).add_to(map)
        except IndexError:
            print(f"City '{city}' not found in DataFrame. Skipping...")
            continue

    return map
# Function to plot tour on the map
def plot_tour_on_map(tour, df, num_cities, tour_length, algorithm_name):
    map = folium.Map(location=[37.0902, -95.7129], zoom_start=5)  # Centered around US
    
    # Add title
    title_html = f'<h3 align="center">Traveling Salesman Problem - Experiment for {num_cities} cities</h3>'
    map.get_root().html.add_child(folium.Element(title_html))
    
    # Add cities to the map
    for city in tour:
        try:
            city_info = df[df['city'] == city].iloc[0]
            label = f"{city_info['city']} ({algorithm_name} - Tour Length: {tour_length:.6f} km)"
            folium.Marker([city_info['lat'], city_info['lng']], popup=label).add_to(map)
        except IndexError:
            print(f"City '{city}' not found in DataFrame. Skipping...")
            continue
    
    # Add tour route to the map
    tour_points = [(df[df['city'] == city]['lat'].iloc[0], df[df['city'] == city]['lng'].iloc[0]) for city in tour]
    folium.PolyLine(tour_points, color="blue", weight=2.5).add_to(map)
    
    return map

# Function to measure the runtime of an algorithm
def measure_runtime(algorithm, *args):
    start_time = time.time()
    result = algorithm(*args)
    end_time = time.time()
    runtime = end_time - start_time
    return result, runtime

# Function for comparative analysis of algorithms

def comparative_analysis(nn_tour, nn_tour_length, nn_start_city, nn_iterations, nn_runtime, christofides_tour, christofides_tour_length, christofides_start_city, christofides_iterations, christofides_runtime):
    
    print("Nearest Neighbor Tour:", nn_tour)
    print("Nearest Neighbor Tour Length:", nn_tour_length)
    print("Nearest Neighbor Start City:", nn_start_city)
    print("Nearest Neighbor Runtime:", nn_runtime)
    print("Nearest Neighbor Iterations:", nn_iterations) 

    print("Christofides Tour:", christofides_tour)
    print("Christofides Tour Length:", christofides_tour_length)
    print("Christofides Start City:", christofides_start_city)
    print("Christofides Runtime:", christofides_runtime)
    print("Christofides Iterations:", christofides_iterations)

# Experiment settings
num_cities_list = [20, 100, 500, 1000]  # Varying number of cities for experimentation

# Perform experiments
for num_cities in num_cities_list:
    print(f"Experimenting with {num_cities} cities:")
    selected_cities = select_random_cities(df, num_cities)
    
    # Plot the selected cities on the map
    map_with_selected_cities = plot_selected_cities_on_map(selected_cities, df)
    map_with_selected_cities.save(f"selected_cities_{num_cities}.html")
    
    graph = create_graph_with_distances(df, selected_cities)

    # Solve TSP using Nearest Neighbor algorithm
    start_city = random.choice(selected_cities)

    nn_runtime = measure_runtime(nearest_neighbor_tsp, graph, start_city)
    nn_tour, nn_iterations = nearest_neighbor_tsp(graph, start_city)
    nn_tour_length = sum(graph[nn_tour[i]][nn_tour[i+1]]['weight'] for i in range(len(nn_tour) - 1))
    nn_start_city = nn_tour[0]
    
    # Plot the Nearest Neighbor tour on the map
    map_with_nn_tour = plot_tour_on_map(nn_tour, df, num_cities, nn_tour_length, "Nearest Neighbor")
    map_with_nn_tour.save(f"nearest_neighbor_tour_{num_cities}.html")
    
    # Solve TSP using Christofides algorithm
    christofides_runtime = measure_runtime(christofides_tsp, graph)
    christofides_tour, christofides_iterations = christofides_tsp(graph)
    christofides_tour_length = sum(graph[christofides_tour[i]][christofides_tour[i+1]]['weight'] for i in range(len(christofides_tour) - 1))
    christofides_start_city = christofides_tour[0]
    
    # Print comparative analysis
    comparative_analysis(nn_tour, nn_tour_length, nn_start_city, nn_iterations, nn_runtime[1], christofides_tour, christofides_tour_length, christofides_start_city, christofides_iterations, christofides_runtime[1])
    
    # Plot the Christofides tour on the map
    map_with_christofides_tour = plot_tour_on_map(christofides_tour, df, num_cities, christofides_tour_length, "Christofides")
    map_with_christofides_tour.save(f"christofides_tour_{num_cities}.html")