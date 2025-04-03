from node import Node

class Segment:
   def __init__(self, name, origin, destination):
       self.name = name                  # Nombre del segmento
       self.origin = origin              # Nodo de origen (instancia de Node)
       self.destination = destination    # Nodo de destino (instancia de Node)
       self.cost = self.origin.distance(self.destination)  # Calculamos la distancia entre los nodos


   def __str__(self):
       """Representación en forma de cadena para facilitar la impresión del segmento."""
       return f"Segment(name={self.name}, origin={self.origin.name}, destination={self.destination.name}, cost={self.cost})"
