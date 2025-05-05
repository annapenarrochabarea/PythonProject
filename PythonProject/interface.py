import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Graph import *
from segment import *
from node import *

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Editor")

        self.graph = Graph()
        self.selected_node = None

        # Crear interfaz
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.btn_example1 = tk.Button(self.frame, text="Load Example 1", command=self.load_example1)
        self.btn_example1.pack(pady=10)

        self.btn_example2 = tk.Button(self.frame, text="Load Example 2", command=self.load_example2)
        self.btn_example2.pack(pady=10)

        self.btn_load_file = tk.Button(self.frame, text="Load From File", command=self.load_from_file)
        self.btn_load_file.pack(pady=10)

        self.btn_select_node = tk.Button(self.frame, text="Select Node", command=self.select_node)
        self.btn_select_node.pack(pady=10)

        self.btn_add_node = tk.Button(self.frame, text="Add Node", command=self.add_node)
        self.btn_add_node.pack(pady=10)

        self.btn_add_segment = tk.Button(self.frame, text="Add Segment", command=self.add_segment)
        self.btn_add_segment.pack(pady=10)

        self.btn_delete_node = tk.Button(self.frame, text="Delete Node", command=self.delete_node)
        self.btn_delete_node.pack(pady=10)

        self.btn_new_graph = tk.Button(self.frame, text="New Graph", command=self.new_graph)
        self.btn_new_graph.pack(pady=10)

        self.btn_save = tk.Button(self.frame, text="Save Graph", command=self.save_graph)
        self.btn_save.pack(pady=10)

        # Canvas para matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)

    # Definimos las características del grafico
    def draw_graph(self, highlight_node=None):
        self.ax.clear()
        self.ax.grid(True, color='red', linestyle='--', linewidth=0.5)

        # Determinar nodos visibles y colores
        neighbors = highlight_node.neighbors if highlight_node else []
        visible_nodes = [highlight_node] + neighbors if highlight_node else self.graph.nodes
        visible_segments = []

        if highlight_node:
            # Solo segmentos que conectan el nodo resaltado con sus vecinos
            for seg in self.graph.segments:
                if (seg.origin == highlight_node and seg.destination in neighbors) or \
                        (seg.destination == highlight_node and seg.origin in neighbors):
                    visible_segments.append(seg)

        else:
            visible_segments = self.graph.segments

        # Dibujar segmentos visibles
        for segment in visible_segments:
            x_vals = [segment.origin.x, segment.destination.x]
            y_vals = [segment.origin.y, segment.destination.y]
            self.ax.plot(x_vals, y_vals, 'blue', linewidth=2)
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            self.ax.plot(x_vals, y_vals, color=segment.color, linewidth=2)


        # Dibujar nodos con colores personalizados
        for node in self.graph.nodes:
            if node == highlight_node:
                color = 'green'
            elif node in neighbors:
                color = 'blue'
            else:
                color = 'red'

            self.ax.scatter(node.x, node.y, color=color, s=50, zorder=3)
            self.ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=10, fontweight='bold', color=color)

        self.ax.set_xlim(0, 25)
        self.ax.set_ylim(0, 25)
        self.canvas.draw()

    def load_example1(self):
        self.graph = CreateGraph_1()
        self.draw_graph()

    def load_example2(self):
        self.graph = CreateGraph_2()
        self.draw_graph()

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.graph = LoadGraphFromFile(path)
            self.draw_graph()

    def select_node(self):
        name = simpledialog.askstring("Select Node", "Enter node name:")
        if name:
            node = next((n for n in self.graph.nodes if n.name == name), None)
            if node:
                self.draw_graph(highlight_node=node)
            else:
                messagebox.showerror("Error", "Node not found")

    def add_node(self):
        name = simpledialog.askstring("Add Node", "Enter node name:")
        try:
            x = float(simpledialog.askstring("Add Node", "Enter x position:"))
            y = float(simpledialog.askstring("Add Node", "Enter y position:"))
            self.graph.AddNode(Node(name, x, y))
            self.draw_graph()
        except:
            messagebox.showerror("Error", "Invalid coordinates")

    def add_segment(self):
        name = simpledialog.askstring("Add Segment", "Enter segment name:")
        origin = simpledialog.askstring("Add Segment", "Enter origin node:")
        dest = simpledialog.askstring("Add Segment", "Enter destination node:")
        if self.graph.AddSegment(name, origin, dest):
            self.draw_graph()
        else:
            messagebox.showerror("Error", "Segment not added. Check node names.")

    def delete_node(self):
        name = simpledialog.askstring("Delete Node", "Enter node name to delete:")
        node = next((n for n in self.graph.nodes if n.name == name), None)
        if node:
            self.graph.nodes.remove(node)
            self.graph.segments = [s for s in self.graph.segments if s.origin != node and s.destination != node]
            self.draw_graph()
        else:
            messagebox.showerror("Error", "Node not found")

    def new_graph(self):
        self.graph = Graph()
        self.draw_graph()

    def save_graph(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w') as file:
                for node in self.graph.nodes:
                    file.write(f"{node.name},{node.x},{node.y}\n")
                for segment in self.graph.segments:
                    file.write(f"{segment.name},{segment.origin.name},{segment.destination.name}\n")
            messagebox.showinfo("Saved", "Graph saved successfully!")

    def on_canvas_click(self, event):
        if event.inaxes:
            closest = self.graph.GetClosest(event.xdata, event.ydata)
            self.draw_graph(highlight_node=closest)


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
