import matplotlib.pyplot as plt
import math
from segment import *
from node import *


class Graph:
    def __init__(self):
        self.nodes = []  # Lista para almacenar los nodos
        self.segments = []  # Lista para almacenar los segmentos (conexiones entre nodos)


 #Añadir un nodo al grafo
def AddNode(G, node):
    if node not in G.nodes:
        G.nodes.append(node) #Si no esta el nodo, lo añadimos
        return True
    return False

# Añadir un segmento entre dos nodos
def AddSegment(G, name, nameOrigin, nameDestination, color='blue'):
    origin_node = None
    destination_node = None
    for node in G.nodes:
        if node.name == nameOrigin:
            origin_node = node
        if node.name == nameDestination:
            destination_node = node

    if origin_node and destination_node:
        segment = Segment(name, origin_node, destination_node)
        G.segments.append(segment)
        AddNeighbor(origin_node, destination_node)
        return True
    return False

#Obtener el nodo más cercano
def GetClosest(G, x, y):
    return min(G.nodes, key=lambda node: Distance(node, Node("temp", x, y)))

# Definimos las características del grafico
def PlotGraph(G, ax):
    ax.clear()
    ax.grid(True, color='red', linestyle='--', linewidth=0.5)  # Mostrar la cuadrícula

    # Dibujar nodos
    for node in G.nodes:
        ax.scatter(node.x, node.y, color='red', s=50, picker=True)
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=10, color='green', fontweight='bold')

    # Dibujar segmentos
    for segment in G.segments:
        x_vals = [segment.origin.x, segment.destination.x]
        y_vals = [segment.origin.y, segment.destination.y]
        ax.plot(x_vals, y_vals, color='blue', linewidth=2)

        #Escribimos cuanto mide cada uno en la mitad de cada segmento
        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        ax.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=8, color='black')


    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title("Grafico con nodos y segmentos")
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 25)

# Definimos las características del grafico de nodos
def PlotNode(G, nameOrigin, ax):
    ax.clear()
    origin = next((node for node in G.nodes if node.name == nameOrigin), None)
    if origin is None: #Si no existe el origen, returns False
        print(f"Nodo '{nameOrigin}' no encontrado.")
        return False

    ax.grid(True, color='red', linestyle='--', linewidth=0.5)  # Mostrar la cuadrícula

    for node in G.nodes: #Dibujamos los nodos
        if node == origin:
            color = 'blue'
        elif node in origin.neighbors:
            color = 'green'
        else:
            color = 'gray'

        ax.scatter(node.x, node.y, color=color, s=50, zorder=3, picker=True)
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=10, fontweight='bold',color='green')  # Texto verde cerca del punto

    # Dibujar líneas a los vecinos
    for neighbor in origin.neighbors:
        plt.plot([origin.x, neighbor.x], [origin.y, neighbor.y], 'r-', linewidth=2)

    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title("Grafico con nodos y segmentos")
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 25)

    return True

# Definimos las características del grafico de las files
def LoadGraphFromFile(filename):
    G = Graph()  # Creamos un nuevo objeto Graph
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Primero, procesamos los nodos
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:  # Formato del nodo: Nombre,X,Y
                    try:
                        node_name = parts[0]
                        x = float(parts[1])
                        y = float(parts[2])
                        AddNode(G, Node(node_name, x, y))
                    except ValueError:
                        # Si no se puede convertir x o y a float, se ignora la línea
                        continue
                elif len(parts) == 3 and parts[0] != '':  # Formato de los segmentos: NombreSegmento,NodoOrigen,NodoDestino
                    segment_name = parts[0]
                    origin = parts[1]
                    destination = parts[2]
                    AddSegment(G,segment_name, origin, destination)

    except FileNotFoundError:
        print(f"Error: El archivo {filename} no se encuentra.")
    return G


def RemoveNode(G, node):
    if node in G.nodes:
        G.nodes.remove(node)
        # Quitar también los segmentos asociados
        G.segments = [seg for seg in G.segments if seg.origin != node and seg.destination != node]
        return True
    return False


def SaveToFile(G, filename):
    with open(filename, 'w') as f:
        for node in G.nodes:
            f.write(f"{node.name} {node.x} {node.y}\n")
        f.write("SEGMENTS\n")
        for seg in G.segments:
            f.write(f"{seg.name} {seg.origin.name} {seg.destination.name} {seg.cost}\n")


@staticmethod
def LoadFromFile(filename):
    G = Graph()
    with open(filename, 'r') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines) and lines[i].strip() != "SEGMENTS":
        name, x, y = lines[i].split()
        AddNode(G,Node(name, float(x), float(y)))
        i += 1
    i += 1
    while i < len(lines):
        name, origin, dest, *rest = lines[i].split()
        AddSegment(G,name, origin, dest)
        i += 1
    return G

#Datos del Grafico 1
def CreateGraph_1():
    G = Graph()

    #Nodos Grafico 1
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))

    #Segmentos Grafico 1
    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")
    return G

#Datos del Grafico 2
def CreateGraph_2():
    G = Graph()

    #Nodos Grafico 2 (inventados)
    AddNode(G, Node("M", 2, 3))
    AddNode(G, Node("N", 5, 8))
    AddNode(G, Node("O", 23, 2))
    AddNode(G, Node("P", 20, 20))
    AddNode(G, Node("Q", 14, 6))
    AddNode(G, Node("R", 18, 10))

    #Segmentos Grafico 2 (inventados)
    AddSegment(G, "MN", "M", "N")
    AddSegment(G, "MO", "M", "O")
    AddSegment(G, "NP", "N", "P")
    AddSegment(G, "NQ", "N", "Q")
    AddSegment(G, "RQ", "R", "Q")
    AddSegment(G, "OR", "O", "R")
    AddSegment(G, "OP", "O", "P")
    return G
