from GenerateGraph import GenerateGraph
from TSPAlgorithms import TSPAlgorithms
from PlotGraph import PlotGraph

# Experiment settings
num_cities_list = [5, 10, 15]  # Varying number of cities for experimentation

for num_cities in num_cities_list:
    print(f"Experimenting with {num_cities} cities:")
    
    # Generate the graph
    graph_gen = GenerateGraph(num_cities)
    graph_gen.generate_random_graph()
    graph_gen.assign_random_weights()
    
    # Solve with nearest neighbor algorithm
    tsp_algo = TSPAlgorithms(num_cities)
    tsp_algo.graph = graph_gen.graph
    nn_tour = tsp_algo.nearest_neighbor_tour()
    nn_tour_length = tsp_algo.calculate_tour_length(nn_tour)
    
    print("Nearest Neighbor Tour:", nn_tour)
    print("Nearest Neighbor Tour Length:", nn_tour_length)
    
    # Solve with Christofides algorithm
    christofides_tour = tsp_algo.christofides_tour()
    christofides_tour_length = tsp_algo.calculate_tour_length(christofides_tour)
    print("Christofides Tour:", christofides_tour)
    print("Christofides Tour Length:", christofides_tour_length)
    
 # Plot the graph with tours
    plot_graph = PlotGraph(graph_gen.graph, graph_gen.coordinates)
    plot_graph.plot_with_tours(nn_tour, christofides_tour, nn_tour_length, christofides_tour_length, num_cities)