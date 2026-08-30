from domineering import DomineeringTablero


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
        
        # Bloque para capturar las coordenadas de la jugada deseada.
        try:
            r = int(input("Ingrese la fila (1 a {}): \n".format(n)))
            c = int(input("Ingrese la columna (1 a {}): \n".format(n)))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese números enteros.")
            continue # Reinicia la petición de coordenadas si hay error en la entrada.

        # Lógica para procesar el movimiento dependiendo del jugador activo.
        if jugador == "A":
            # Intenta ejecutar el movimiento horizontal para el jugador A.
            if tablero.realizar_movimiento_A(r, c):
                print("Movimiento realizado por el jugador A.\n")
                # Cambia el turno al jugador B si el movimiento fue exitoso.
                jugador = "B"
                print(tablero)
            else:
                # Avisa si la posición estaba ocupada o dejaba la pieza fuera de los límites.
                print("Movimiento inválido para el jugador A.\n")
        else:
            # Intenta ejecutar el movimiento vertical para el jugador B.
            if tablero.realizar_movimiento_B(r, c):
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