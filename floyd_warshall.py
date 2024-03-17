import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ShortestPathFinder:
    def __init__(self, master):
        self.master = master
        self.master.title("Shortest Path Finder")

        # Bind the closing event to stop the code
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the input widgets
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        # Create labels and entry widgets for the source and destination cities
        tk.Label(input_frame, text="Source City:").grid(row=0, column=0, padx=5)
        self.source_entry = tk.Entry(input_frame)
        self.source_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Destination City:").grid(row=1, column=0, padx=5)
        self.destination_entry = tk.Entry(input_frame)
        self.destination_entry.grid(row=1, column=1, padx=5)

        # Button to find the shortest path
        tk.Button(input_frame, text="Find Shortest Path", command=self.find_shortest_path).grid(row=2, columnspan=2, pady=10)

        # Create a frame for displaying the map
        map_frame = tk.Frame(self.master)
        map_frame.pack()

        # Create a matplotlib figure and canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=map_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def find_shortest_path(self):
        # Get the source and destination cities from the entry widgets
        source_city = self.source_entry.get()
        destination_city = self.destination_entry.get()

        # Create a simple road network (graph) using networkx
        G = nx.Graph()
        G.add_edge("KARACHI", "HYDERABAD", weight=164) #A= KARACHI 
        G.add_edge("KARACHI", "QUETTA", weight=686)  #B= HYDERABAD 
        G.add_edge("HYDERABAD", "QUETTA", weight=707) 
        G.add_edge("HYDERABAD", "MULTAN", weight=745)  #C= QUETTA
        G.add_edge("QUETTA", "MULTAN", weight=633)  #D= MULTAN
        G.add_edge("MULTAN", "LAHORE", weight=339) #E= LAHORE

        # Call the Dijkstra's algorithm
        try:
            shortest_path = self.floyd_warshall(G, source_city, destination_city)

            # Display the shortest path on the matplotlib figure with edge labels
            self.plot_shortest_path(G, shortest_path)

            # Show the result in a message box
            messagebox.showinfo("Shortest Path", f"Shortest path: {shortest_path}")

        except nx.NetworkXNoPath:
            messagebox.showerror("Error", "No path found between the specified cities.")

    def floyd_warshall(self, G, source, destination):
        nodes = list(G.nodes)

        # Initialize distances and predecessors matrices
        num_nodes = len(nodes)
        distances = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        predecessors = [[None] * num_nodes for _ in range(num_nodes)]

        for i in range(num_nodes):
            distances[i][i] = 0

        for edge in G.edges(data=True):
            u, v, data = edge
            distances[nodes.index(u)][nodes.index(v)] = data.get('weight', 1)
            distances[nodes.index(v)][nodes.index(u)] = data.get('weight', 1)
            predecessors[nodes.index(u)][nodes.index(v)] = nodes.index(u)
            predecessors[nodes.index(v)][nodes.index(u)] = nodes.index(v)
        
        # Floyd-Warshall algorithm
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
                        predecessors[i][j] = predecessors[k][j]

        # Reconstruct the path from source to destination
        source_index = nodes.index(source)
        destination_index = nodes.index(destination)

        path = [destination]
        while predecessors[source_index][destination_index] is not None:
            destination_index = predecessors[source_index][destination_index]
            path.append(nodes[destination_index])
        path.reverse()

        return path

    def plot_shortest_path(self, G, path):
        # Clear the previous plot
        self.ax.clear()

        # Draw the road network
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, ax=self.ax)

        # Highlight the shortest path
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="r", width=2)

        # Display edge weights as labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)

        # Refresh the canvas
        self.canvas.draw()

    def on_closing(self):
        # Function to stop the code when the window is closed
        self.master.destroy()
        self.master.quit()


def main():
    root = tk.Tk()
    app = ShortestPathFinder(root)
    root.mainloop()


if __name__ == "__main__":
    main()