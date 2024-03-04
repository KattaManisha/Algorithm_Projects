from GenerateGraph import GenerateGraph
from TSPAlgorithms import TSPAlgorithms
from PlotGraph import PlotGraph

# Experiment settings
num_cities_list = [5, 10, 15]  # Varying number of cities for experimentation

for num_cities in num_cities_list:
    print(f"Experimenting with {num_cities} cities:")
    
    graph_generator = GenerateGraph(num_cities)
    graph_generator.generate_random_graph()
    graph_generator.assign_random_weights()

    tsp_solver = TSPAlgorithms(num_cities)
    tsp_solver.graph = graph_generator.graph
    tsp_solver.coordinates = graph_generator.coordinates

    nn_tour = tsp_solver.nearest_neighbor_tour()
    nn_tour_length = tsp_solver.calculate_tour_length(nn_tour)

    print("Nearest Neighbor Tour:", nn_tour)
    print("Nearest Neighbor Tour Length:", nn_tour_length)

    christofides_tour = tsp_solver.christofides_tour()
    christofides_tour_length = tsp_solver.calculate_tour_length(christofides_tour)

    print("Christofides Tour:", christofides_tour)
    print("Christofides Tour Length:", christofides_tour_length)

    plot_graph = PlotGraph(graph_generator.graph, graph_generator.coordinates)
    plot_graph.plot_with_tours(nn_tour, christofides_tour, nn_tour_length, christofides_tour_length, num_cities)
