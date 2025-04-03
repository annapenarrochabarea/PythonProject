
from node import Node
from segment import Segment
# Crear nodos
n1 = Node('aaa', 0, 0)
n2 = Node('bbb', 3, 4)
n3 = Node('ccc', 6, 8)

# Crear segmentos
seg1 = Segment('Segment1', n1, n2)
seg2 = Segment('Segment2', n2, n3)


# Imprimir los segmentos para verificar los resultados
print(seg1)  # Debería mostrar el segmento entre n1 y n2
print(seg2)  # Debería mostrar el segmento entre n2 y n3

