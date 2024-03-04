import networkx as nx
import matplotlib.pyplot as plt

class PlotGraph:
    def __init__(self, graph, coordinates):
        self.graph = graph
        self.coordinates = coordinates
        self.pos = {i: coordinates[i] for i in range(len(coordinates))}

    def plot_with_tours(self, nn_tour, christofides_tour, nn_tour_length, christofides_tour_length, num_cities):
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, self.pos, with_labels=True, node_size=300)
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=[(nn_tour[i], nn_tour[i+1]) for i in range(len(nn_tour) - 1)], edge_color='r', width=2, label=f'Nearest Neighbor Tour (Length: {nn_tour_length})')
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=[(christofides_tour[i], christofides_tour[i+1]) for i in range(len(christofides_tour) - 1)], edge_color='b', width=2, label=f'Christofides Tour (Length: {christofides_tour_length})')
        plt.title(f"Traveling Salesman Problem - Experiment for {num_cities} cities")
        plt.legend(loc='upper right')
        plt.show()
