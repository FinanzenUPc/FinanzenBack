"""
Union-Find (Disjoint Set Union) Data Structure
Complejidad: O(α(n)) ≈ O(1) amortizado con compresión de caminos y unión por rango
"""
from typing import Dict, List


class UnionFind:
    """Estructura de datos Union-Find con compresión de caminos y unión por rango."""

    def __init__(self, n: int):
        """
        Inicializa Union-Find.

        Args:
            n: Número de elementos
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Número de componentes

    def find(self, x: int) -> int:
        """
        Encuentra el representante del conjunto con compresión de caminos.

        Args:
            x: Elemento

        Returns:
            Representante del conjunto
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Compresión de caminos
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Une dos conjuntos por rango.

        Args:
            x: Primer elemento
            y: Segundo elemento

        Returns:
            True si se unieron, False si ya estaban en el mismo conjunto
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Unión por rango
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """
        Verifica si dos elementos están en el mismo conjunto.

        Args:
            x: Primer elemento
            y: Segundo elemento

        Returns:
            True si están conectados
        """
        return self.find(x) == self.find(y)

    def get_components(self) -> Dict[int, List[int]]:
        """
        Obtiene todos los componentes.

        Returns:
            Dict con representante como clave y lista de elementos como valor
        """
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        return components

    def num_components(self) -> int:
        """
        Número de componentes conectados.

        Returns:
            Número de componentes
        """
        return self.count
