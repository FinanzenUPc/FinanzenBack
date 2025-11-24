"""
Knapsack Problem (Problema de la Mochila) - Programación Dinámica
Complejidad: O(n * W)
"""
from typing import List, Tuple, Dict


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> Dict[str, any]:
    """
    Problema de la mochila 0/1 usando programación dinámica.

    Args:
        weights: Lista de pesos de los items
        values: Lista de valores de los items
        capacity: Capacidad de la mochila

    Returns:
        Dict con valor máximo e items seleccionados
    """
    n = len(weights)

    # Tabla DP: dp[i][w] = máximo valor con i items y capacidad w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Llenar tabla DP
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # No incluir item i-1
            dp[i][w] = dp[i-1][w]

            # Incluir item i-1 si es posible
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])

    # Reconstruir solución
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)  # Item en índice i-1
            w -= weights[i-1]

    selected_items.reverse()

    return {
        "max_value": dp[n][capacity],
        "selected_items": selected_items,
        "selected_weights": [weights[i] for i in selected_items],
        "selected_values": [values[i] for i in selected_items],
        "total_weight": sum(weights[i] for i in selected_items)
    }


def knapsack_unbounded(weights: List[int], values: List[int], capacity: int) -> Dict[str, any]:
    """
    Problema de la mochila sin límite (unbounded knapsack).

    Args:
        weights: Lista de pesos de los items
        values: Lista de valores de los items
        capacity: Capacidad de la mochila

    Returns:
        Dict con valor máximo
    """
    dp = [0] * (capacity + 1)

    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return {
        "max_value": dp[capacity]
    }


def knapsack_fractional(weights: List[float], values: List[float], capacity: float) -> Dict[str, any]:
    """
    Problema de la mochila fraccionaria (Greedy).

    Args:
        weights: Lista de pesos
        values: Lista de valores
        capacity: Capacidad de la mochila

    Returns:
        Dict con valor máximo y fracciones
    """
    n = len(weights)

    # Calcular valor/peso y ordenar
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    items.sort(reverse=True, key=lambda x: x[0])

    total_value = 0.0
    fractions = [0.0] * n
    remaining_capacity = capacity

    for ratio, weight, value, idx in items:
        if remaining_capacity >= weight:
            # Tomar todo el item
            fractions[idx] = 1.0
            total_value += value
            remaining_capacity -= weight
        else:
            # Tomar fracción
            fraction = remaining_capacity / weight
            fractions[idx] = fraction
            total_value += value * fraction
            remaining_capacity = 0
            break

    return {
        "max_value": total_value,
        "fractions": fractions
    }


def subset_sum(numbers: List[int], target: int) -> Dict[str, any]:
    """
    Problema de suma de subconjunto (Subset Sum).

    Args:
        numbers: Lista de números
        target: Suma objetivo

    Returns:
        Dict indicando si es posible y el subconjunto
    """
    n = len(numbers)
    dp = [[False for _ in range(target + 1)] for _ in range(n + 1)]

    # Suma 0 siempre es posible
    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for s in range(target + 1):
            dp[i][s] = dp[i-1][s]

            if numbers[i-1] <= s:
                dp[i][s] = dp[i][s] or dp[i-1][s - numbers[i-1]]

    # Reconstruir subconjunto
    if not dp[n][target]:
        return {
            "is_possible": False,
            "subset": []
        }

    subset = []
    s = target
    for i in range(n, 0, -1):
        if s >= numbers[i-1] and dp[i-1][s - numbers[i-1]]:
            subset.append(numbers[i-1])
            s -= numbers[i-1]

    return {
        "is_possible": True,
        "subset": subset,
        "sum": sum(subset)
    }
