import math

class Node:
   def __init__(self, name, x, y):
       self.name = name      # Nombre del nodo
       self.x = x            # Coordenada X del nodo
       self.y = y            # Coordenada Y del nodo
       self.neighbors = []   # Lista de nodos vecinos


   def add_neighbor(self, neighbor):
       if neighbor not in self.neighbors:
           self.neighbors.append(neighbor)
           return True
       return False


   def distance(self, other_node):  #Calcula la distancia euclidiana entre dos nodos.
       dx = other_node.x - self.x
       dy = other_node.y - self.y
       return math.sqrt(dx**2 + dy**2)


   def __str__(self):  #Representación en forma de cadena para facilitar la impresión del nodo.
       return f"Node(name={self.name}, x={self.x}, y={self.y}, neighbors={[neighbor.name for neighbor in self.neighbors]})"

# Funciones adicionales que estarán fuera de la clase Node pero como está relacionado, las colocamos en el mismo archivo.

def AddNeighbor(n1, n2):  # Añade el nodo n2 a la lista de vecinos de n1 si no está presente.
    return n1.add_neighbor(n2)  # Si ya es un vecino, devuelve False; si no, lo añade y devuelve True.

def Distance(n1, n2):
    return n1.distance(n2)
