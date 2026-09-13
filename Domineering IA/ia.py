"""Módulo que implementa el agente inteligente mediante Minimax con poda Alfa-Beta."""


def _contar_vecinos_vacios(tablero, r: int, c: int) -> int:
    """Cuenta cuántas casillas ortogonalmente vecinas a (r, c) están vacías.

    Es una heurística puramente local: solo examina hasta 4 casillas
    vecinas, sin recorrer el tablero completo. Su costo es constante y no
    depende del tamaño del tablero.
    """
    vecinos = ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
    total = 0
    for fila, columna in vecinos:
        if 1 <= fila <= len(tablero) and 1 <= columna <= len(tablero):
            if tablero[fila, columna] == tablero.EMPTY_SPACE:
                total += 1
    return total


def ordenar_movimientos(tablero, movimientos: list[tuple[int, int]], jugador: str) -> list[tuple[int, int]]:
    """Ordena los movimientos candidatos de mejor a peor según una heurística local.

    Se prioriza colocar el dominó en casillas con más vecinos vacíos
    alrededor (más "espacio para maniobrar" cerca de esa jugada).
    """
    def puntaje(movimiento: tuple[int, int]) -> int:
        r, c = movimiento
        if jugador == "A":
            return _contar_vecinos_vacios(tablero, r, c) + _contar_vecinos_vacios(tablero, r + 1, c)
        else:
            return _contar_vecinos_vacios(tablero, r, c) + _contar_vecinos_vacios(tablero, r, c + 1)

    return sorted(movimientos, key=puntaje, reverse=True)


def minimax_alfa_beta(
    tablero,
    profundidad,
    alfa,
    beta,
    es_maximizador,
    max_movimientos: int | None = None,
):
    """Ejecuta Minimax con poda Alfa-Beta para elegir la mejor jugada disponible."""
    movimientos_a = tablero.obtener_movimientos("A")
    movimientos_b = tablero.obtener_movimientos("B")

    # Condición de término: si el jugador en turno no tiene movimientos, pierde.
    if es_maximizador and not movimientos_a:
        return -float('inf'), None
    if not es_maximizador and not movimientos_b:
        return float('inf'), None

    # Si alcanzamos el límite de profundidad, evaluamos el tablero.
    if profundidad == 0:
        return tablero.evaluar_tablero(), None

    if es_maximizador:  # Simulación del Humano (Jugador A)
        movimientos = ordenar_movimientos(tablero, movimientos_a, "A")

        # Restringe la cantidad de opciones evaluadas, si corresponde.
        if max_movimientos is not None:
            movimientos = movimientos[:max_movimientos]

        max_eval = -float('inf')
        # Asignamos el primer movimiento por defecto: si todas las jugadas
        # llevan a perder (-inf), la IA al menos jugará algo.
        mejor_movimiento = movimientos[0]

        for r, c in movimientos:
            tablero.realizar_movimiento_a(r, c)

            evaluacion, _ = minimax_alfa_beta(
                tablero, profundidad - 1, alfa, beta, False, max_movimientos
            )

            # Deshacemos el movimiento.
            tablero[r, c] = tablero.EMPTY_SPACE
            tablero[r + 1, c] = tablero.EMPTY_SPACE

            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = (r, c)

            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break  # Poda
        return max_eval, mejor_movimiento

    else:  # Turno de la IA (Jugador B)
        movimientos = ordenar_movimientos(tablero, movimientos_b, "B")

        if max_movimientos is not None:
            movimientos = movimientos[:max_movimientos]

        min_eval = float('inf')
        mejor_movimiento = movimientos[0]

        for r, c in movimientos:
            tablero.realizar_movimiento_b(r, c)

            evaluacion, _ = minimax_alfa_beta(
                tablero, profundidad - 1, alfa, beta, True, max_movimientos
            )

            # Deshacemos el movimiento horizontal.
            tablero[r, c] = tablero.EMPTY_SPACE
            tablero[r, c + 1] = tablero.EMPTY_SPACE

            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = (r, c)

            beta = min(beta, evaluacion)
            if beta <= alfa:
                break  # Poda
        return min_eval, mejor_movimiento