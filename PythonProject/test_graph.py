from node import Node
from segment import Segment
from Graph import *

print ("Probando el grafo...")
# Crear el grafo
G = CreateGraph_1()

# Graficar todos los nodos y segmentos
PlotGraph(G)

# Guardar el grafo en archivo
SaveToFile(G, 'Prueba_guardar_grafo.txt')

# Graficar un nodo y sus vecinos (por ejemplo, "C")
PlotNode(G, "C")

n = GetClosest(G,15,5)
print (n.name) # La respuesta debe ser J
n = GetClosest(G,8,19)
print (n.name) # La respuesta debe ser B