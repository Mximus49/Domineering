def minimax_alfa_beta(tablero, profundidad, alfa, beta, es_maximizador):
    movimientos_a = tablero.obtener_movimientos("A")
    movimientos_b = tablero.obtener_movimientos("B")
    
    # 1. Condición de término corregida:
    # Si es el turno de A y no tiene movimientos, pierde (-inf)
    if es_maximizador and not movimientos_a:
        return -float('inf'), None
    # Si es el turno de B y no tiene movimientos, B pierde (A gana, +inf)
    if not es_maximizador and not movimientos_b:
        return float('inf'), None
        
    # Si alcanzamos el límite de profundidad, evaluamos el tablero
    if profundidad == 0:
        return tablero.evaluar_tablero(), None

    if es_maximizador: # Turno del jugador A (maximiza la ventaja A - B)
        max_eval = -float('inf')
        
        # 2. Asignamos el primer movimiento válido por defecto. 
        # Así, si todas las jugadas llevan a perder (-inf), la IA al menos jugará algo.
        mejor_movimiento = movimientos_a[0] 
        
        for r, c in movimientos_a:
            tablero.realizar_movimiento_a(r, c)
            
            evaluacion, _ = minimax_alfa_beta(tablero, profundidad - 1, alfa, beta, False)
            
            # Deshacemos el movimiento vertical (delegado al tablero para
            # no depender de offsets hardcodeados aquí).
            tablero.deshacer_movimiento_a(r, c)
            
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = (r, c)
                
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break # Poda
        return max_eval, mejor_movimiento

    else: # Turno de la IA (Jugador B, minimiza la ventaja A - B)
        min_eval = float('inf')
        
        # Asignamos el primer movimiento válido por defecto
        mejor_movimiento = movimientos_b[0]
        
        for r, c in movimientos_b:
            tablero.realizar_movimiento_b(r, c)
            
            evaluacion, _ = minimax_alfa_beta(tablero, profundidad - 1, alfa, beta, True)
            
            # Deshacemos el movimiento horizontal (delegado al tablero).
            tablero.deshacer_movimiento_b(r, c)
            
            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = (r, c)
                
            beta = min(beta, evaluacion)
            if beta <= alfa:
                break # Poda
        return min_eval, mejor_movimiento