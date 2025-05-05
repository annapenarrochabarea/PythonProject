import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseEvent
from Graph import *
from segment import *
from node import *


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Gráficos de Vuelo")

        # Crear un objeto Graph vacío
        self.graph = Graph()
        self.selected_node = None

        # Crear botones
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.btn_create_graph_1 = tk.Button(self.frame, text="Mostrar Gráfico 1", command=self.load_graph_1)
        self.btn_create_graph_1.pack(pady=10)

        self.btn_create_graph_2 = tk.Button(self.frame, text="Mostrar Gráfico 2", command=self.load_graph_2)
        self.btn_create_graph_2.pack(pady=10)

        self.btn_load_file = tk.Button(self.frame, text="Cargar Gráfico desde archivo",command=self.load_graph_from_file)
        self.btn_load_file.pack(pady=10)

        self.btn_add_node = tk.Button(self.frame, text="Añadir Nodo", command=self.add_node)
        self.btn_add_node.pack(pady=10)

        # Etiqueta para la coordenada X
        self.label_x = tk.Label(self.frame, text="Coordenada X:")  # Esto crea una etiqueta con el texto
        self.label_x.pack(pady=2)

        # Caja de texto para la coordenada X
        self.entry_x = tk.Entry(self.frame)
        self.entry_x.pack(pady=2)

        # Etiqueta para la coordenada Y
        self.label_y = tk.Label(self.frame, text="Coordenada Y:")  # Esto crea una etiqueta con el texto
        self.label_y.pack(pady=2)

        # Caja de texto para la coordenada Y
        self.entry_y = tk.Entry(self.frame)
        self.entry_y.pack(pady=2)

        self.btn_add_segment = tk.Button(self.frame, text="Añadir Segmento", command=self.add_segment)
        self.btn_add_segment.pack(pady=10)

        self.btn_delete_node = tk.Button(self.frame, text="Eliminar Node", command=self.delete_node)
        self.btn_delete_node.pack(pady=10)

        self.btn_new_graph = tk.Button(self.frame, text="New Graph", command=self.new_graph)
        self.btn_new_graph.pack(pady=10)

        self.btn_save = tk.Button(self.frame, text="Save Graph", command=self.save_graph)
        self.btn_save.pack(pady=10)

        # Canvas para dibujar los gráficos de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("pick_event", self.on_canvas_click)


    def display_graph(self):
        if self.graph is None:
            messagebox.showerror("Error", "No hay ningún gráfico para mostrar")
            return

        # Mostrar el gráfico general utilizando la función PlotGraph definida en Graph
        PlotGraph(self.graph, self.ax)
        self.canvas.draw()

    def load_graph_1(self):
        self.graph = CreateGraph_1()  # Cargar el gráfico 1
        self.display_graph()

    def load_graph_2(self):
        self.graph = CreateGraph_2()  # Cargar el gráfico 2
        self.display_graph()

    def load_graph_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
        if filename:
            self.graph = LoadFromFile(filename)  # Utilizar la función LoadFromFile de Graph
            self.display_graph()

    def on_canvas_click(self, event):
        artist = event.artist
        if not isinstance(artist, matplotlib.collections.PathCollection):
            return  # Ignorar clics que no sean sobre nodos

        mouse_event = event.mouseevent
        x_click, y_click = mouse_event.xdata, mouse_event.ydata
        closest_node = self.get_closest_node(x_click, y_click)
        if closest_node:
            self.selected_node = closest_node
            PlotNode(self.graph, closest_node.name, self.ax)
            self.canvas.draw()

    def add_node(self):
        x = self.entry_x.get()
        y = self.entry_y.get()

        try:
            x = float(x)
            y = float(y)
        except ValueError:
            messagebox.showerror("Error", "Debes escribir números válidos.")
            return

        nombre = f"N{len(self.graph.nodes) + 1}"  # Nombre automático como N1, N2...
        nuevo_nodo = Node(nombre, x, y)

        if AddNode(self.graph, nuevo_nodo):  # Usamos tu función de Graph.py
            self.display_graph()
        else:
            messagebox.showwarning("Repetido", "Ese nodo ya existe.")

    def add_segment(self):
        # Pedir los datos del segmento a añadir
        name = simpledialog.askstring("Add Segment", "Nombre del Segmento:")
        origin_name = simpledialog.askstring("Add Segment", "Nodo de Origen:")
        dest_name = simpledialog.askstring("Add Segment", "Nodo Final:")

        # Verificar que los nodos de origen y destino existen
        origin = next((node for node in self.graph.nodes if node.name == origin_name), None)
        dest = next((node for node in self.graph.nodes if node.name == dest_name), None)

        if origin is None or dest is None:
            # Si no se encuentran los nodos, mostrar un error
            messagebox.showerror("Error", "Uno o ambos nodos no existen en el gráfico.")
            return

        # Si los nodos existen, añadir el segmento
        if self.graph.AddSegment(name, origin, dest):
            self.draw_graph()  # Redibujar el gráfico con el nuevo segmento
        else:
            messagebox.showerror("Error", "El segmento no se ha añadido. Revisa los nombres de los nodos.")

    def get_closest_node(self, x, y):
        """Devuelve el nodo más cercano al punto (x, y)."""
        return min(self.graph.nodes, key=lambda node: Distance(node, Node("temp", x, y)))

    def plot_node_neighbors(self, origin_node):
        # Dibujar los vecinos del nodo utilizando la función PlotNode definida en Graph
        PlotNode(self.graph, origin_node.name, self.ax)
        self.canvas.draw()

    def delete_node(self):
        if self.selected_node:
            from Graph import RemoveNode  # Importar aquí si no lo tienes ya arriba
            success = RemoveNode(self.graph, self.selected_node)
            if success:
                self.selected_node = None
                self.display_graph()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el nodo.")
        else:
            messagebox.showwarning("Atención", "No hay ningún nodo seleccionado.")

    def new_graph(self):
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres crear un nuevo gráfico? Se perderán los datos actuales.")
        if confirm:
            self.graph = Graph()  # Crear un nuevo objeto Graph vacío
            self.selected_node = None
            self.display_graph()

    def save_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if filename:
            try:
                SaveToFile(self.graph, filename)
                messagebox.showinfo("Éxito", f"Grafo guardado en {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el grafo: {str(e)}")


# Función principal para ejecutar la aplicación
def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()