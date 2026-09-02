"""
Gestiona la interacción con los jugadores, solicita la configuración inicial 
del tablero y controla el flujo de los turnos hasta determinar un ganador.
"""
from domineering import DomineeringTablero
from ia import minimax_alfa_beta

# Cambiar R y C, ESTAN AL REVES

def main():
    print("=== Domineering ===")
    # Bucle para solicitar y validar la configuración inicial del tablero.
    while True:
        try:
            # Solicita al usuario el tamaño de la matriz (n x n).
            n = int(input("Ingrese el tamaño del tablero (n >= 4): ")) 
        except ValueError:
            # Maneja el error si el usuario ingresa texto u otros caracteres no numéricos.
            print("Entrada inválida. Por favor, ingrese un número entero positivo.")
            continue

        try:
            # Intenta crear el tablero con el tamaño proporcionado.
            tablero = DomineeringTablero(n)
        except ValueError:
            # Captura la excepción si el tamaño es menor a 4.
            print("Entrada inválida. Por favor, ingrese un número entero mayor a 4.")
            continue
        break

    # Crea las reglas visuales y al jugador que comienza la partida.
    jugador = "A"
    print("\nJugador A coloca fichas horizontalmente.")
    print("Jugador B coloca fichas verticalmente.\n")
    # Muestra el estado inicial del tablero vacío.
    print(tablero)

    # Bucle principal del juego que se ejecuta hasta que haya un ganador.
    while True:
        # Verifica antes de cada turno si el jugador actual tiene movimientos disponibles.
        if not tablero.movimiento_valido(jugador):
            print(f"No hay más movimientos válidos para el jugador {jugador}.")
            # Si el jugador actual no puede moverse, el oponente es el ganador.
            ganador = "B" if jugador == "A" else "A"
            print(f"El jugador {ganador} gana!")
            break

        print(f"\nTurno del jugador {jugador}.")
        
        
        # Lógica para procesar el movimiento dependiendo del jugador activo.
        if jugador == "A":
            print("La IA esta pensando su jugada...")
            _, mejor_jugada = minimax_alfa_beta(tablero, 4, -float("inf"), float("inf"), True)

            if mejor_jugada:
                tablero.realizar_movimiento_a(mejor_jugada[0], mejor_jugada[1])
                print(f"IA juega en fila {mejor_jugada[0]}, columna {mejor_jugada[1]}.\n")
                jugador = "B"
                print(tablero)
        else:
            # Bloque para capturar las coordenadas de la jugada deseada.
            r = input(f"Ingrese la fila (1 a {n}): \n")
            c = input(f"Ingrese la columna (1 a {n}): \n")
            
            if not (r.isdigit() and c.isdigit()):
                print("Entrada inválida. Por favor, ingrese números enteros.\n")
                continue
            
            r = int(r)
            c = int(c)
            
            if r < 1 or r > n or c < 1 or c > n:
                print(f"Movimiento invalido. Las coordenadas deben estar entre 1 y {n}.\n")
                continue
            
            # Intenta ejecutar el movimiento vertical para el jugador B.
            if tablero.realizar_movimiento_b(r, c):
                print("Movimiento realizado por el jugador B.\n")
                # Cambia el turno al jugador A si el movimiento fue exitoso.
                jugador = "A"
                print(tablero)
            else:
                # Avisa si la posición estaba ocupada o dejaba la pieza fuera de los límites.
                print("Movimiento inválido para el jugador B.\n")


# Punto de entrada estándar de los scripts de Python.
if __name__ == "__main__":
    main()