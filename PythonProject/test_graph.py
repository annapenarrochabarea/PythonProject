from graph import *

#Defino y creo el grafico

def CreateGraph_1():
    G1 = Graph()  # Crear una instancia del grafo
    G1.AddNode(Node("A", 1, 20))
    G1.AddNode(Node("B", 8, 17))
    G1.AddNode(Node("C", 15, 20))
    G1.AddNode(Node("D", 18, 15))
    G1.AddNode(Node("E", 2, 4))
    G1.AddNode(Node("F", 6, 5))
    G1.AddNode(Node("G", 12, 12))
    G1.AddNode(Node("H", 10, 3))
    G1.AddNode(Node("I", 19, 1))
    G1.AddNode(Node("J", 13, 5))
    G1.AddNode(Node("K", 3, 15))
    G1.AddNode(Node("L", 4, 10))

    G1.AddSegment("A", "B")
    G1.AddSegment("A", "E")
    G1.AddSegment("A", "K")
    G1.AddSegment("B", "A")
    G1.AddSegment("B", "C")
    G1.AddSegment("B", "F")
    G1.AddSegment("B", "K")
    G1.AddSegment("B", "G")
    G1.AddSegment("C", "D")
    G1.AddSegment("C", "G")
    G1.AddSegment("D", "G")
    G1.AddSegment("D", "H")
    G1.AddSegment("D", "I")
    G1.AddSegment("E", "F")
    G1.AddSegment("F", "L")
    G1.AddSegment("G", "B")
    G1.AddSegment("G", "F")
    G1.AddSegment("G", "H")
    G1.AddSegment("I", "D")
    G1.AddSegment("I", "J")
    G1.AddSegment("J", "I")
    G1.AddSegment("K", "A")
    G1.AddSegment("K", "L")
    G1.AddSegment("L", "K")
    G1.AddSegment("L", "F")

    return G1

print("Probando el grafo...")

G1 = CreateGraph_1()
G1.Plot() #De momento me imprime un grafico con todos los nodos, seguiremos avanzando 
