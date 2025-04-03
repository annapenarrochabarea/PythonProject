import math
import matplotlib.pyplot as plt

from node import *

class Graph:
    def __init__(self):
        self.nodes = []  # Lista para almacenar los nodos
        self.segments = []  # Lista para almacenar los segmentos (conexiones entre nodos)

    # Añadir un nodo al grafo
    def AddNode(self, n):
        if n in self.nodes:  # Si el nodo ya está en la lista, no lo añadimos
            return False
        self.nodes.append(n)  # Si no está, lo añadimos
        return True

    # Añadir un segmento (conexión) entre dos nodos
    def AddSegment(self, nameOriginNode, nameDestinationNode):
        origin = None
        destination = None
        # Buscar los nodos por su nombre
        for node in self.nodes:
            if node.name == nameOriginNode:
                origin = node
            if node.name == nameDestinationNode:
                destination = node
        if origin is None or destination is None:  # Si algún nodo no se encuentra
            return False
        # Si ambos nodos existen, lo añadimos como segmento
        else:
            self.segments.append((origin, destination))
            origin.add_neighbor(destination)  # Añadir el vecino al nodo origen
            return True

    # Obtener el nodo más cercano a un punto (x, y)
    def GetClosest(self, x, y):
        closest_node = None
        min_distance = float("inf")  # Iniciar con una distancia muy grande
        for node in self.nodes:
            # Calcular la distancia de cada nodo al punto (x, y)
            distance = math.sqrt((node.x - x)**2 + (node.y - y)**2)
            if distance < min_distance:
                closest_node = node
                min_distance = distance
        return closest_node

    # Mostrar el grafo en una gráfica
    def Plot(self):
        plt.figure(figsize=(6, 5))  # Tamaño similar al de la imagen del documento

        # Dibuja los segmentos (líneas entre nodos)
        for segment in self.segments:
            x_values = [segment[0].x, segment[1].x]
            y_values = [segment[0].y, segment[1].y]
            plt.plot(x_values, y_values, 'b-')  # Líneas azules

        # Dibuja los nodos
        for node in self.nodes:
            plt.scatter(node.x, node.y, color='red', s=50, zorder=3)  # Puntos rojos
            plt.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=10, fontweight='bold',
                     color='green')  # Texto verde cerca del punto

        # Configurar cuadrícula
        plt.grid(True, linestyle='--', linewidth=0.5, color='red')  # Cuadrícula en rojo con líneas punteadas

        # Ajustar límites del gráfico
        plt.xlim(0, 25)
        plt.ylim(0, 25)

        # Título del gráfico
        plt.title("Grafico con nodos y segmentos", fontsize=12)

        # Mostrar el gráfico
        plt.show()

