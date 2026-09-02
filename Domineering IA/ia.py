import copy


def minimax_alfa_beta(tablero, profundidad, alfa, beta, es_maximizador):
    movimientos_a = tablero.obtener_movimientos("A")
    movimientos_b = tablero.obtener_movimientos("B")
    
    # Condición de término
    if profundidad == 0 or not movimientos_a or not movimientos_b:
        return tablero.evaluar_tablero(), None

    mejor_movimiento = None

    if es_maximizador: # Turno de la IA (Jugador A)
        max_eval = -float('inf')
        for r, c in movimientos_a:
            tablero_clon = copy.deepcopy(tablero)
            tablero_clon.realizar_movimiento_a(r, c)
            
            evaluacion, _ = minimax_alfa_beta(tablero_clon, profundidad - 1, alfa, beta, False)
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = (r, c)
                
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break # Poda
        return max_eval, mejor_movimiento

    else: # Simulación del Humano (Jugador B)
        min_eval = float('inf')
        for r, c in movimientos_b:
            tablero_clon = copy.deepcopy(tablero)
            tablero_clon.realizar_movimiento_b(r, c)
            
            evaluacion, _ = minimax_alfa_beta(tablero_clon, profundidad - 1, alfa, beta, True)
            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = (r, c)
                
            beta = min(beta, evaluacion)
            if beta <= alfa:
                break # Poda
        return min_eval, mejor_movimiento