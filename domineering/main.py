from domineering import DomineeringTablero


def main():
    print("=== Domineering ===")
    while True:
        try:
            n = int(input("Ingrese el tamaño del tablero (n >= 4): ")) 
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero positivo.")
            continue

        try:
            tablero = DomineeringTablero(n)
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero mayor a 4.")
            continue
        break

    jugador = "A"
    print("\nJugador A coloca fichas horizontalmente.")
    print("Jugador B coloca fichas verticalmente.\n")
    print(tablero)

    while True:
        if not tablero.movimiento_valido(jugador):
            print(f"No hay más movimientos válidos para el jugador {jugador}.")
            ganador = "B" if jugador == "A" else "A"
            print(f"El jugador {ganador} gana!")
            break

        print(f"\nTurno del jugador {jugador}.")
        try:
            r = int(input("Ingrese la fila (1 a {}): \n".format(n)))
            c = int(input("Ingrese la columna (1 a {}): \n".format(n)))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese números enteros.")
            continue

        if jugador == "A":
            if tablero.realizar_movimiento_A(r, c):
                print("Movimiento realizado por el jugador A.\n")
                jugador = "B"
                print(tablero)
            else:
                print("Movimiento inválido para el jugador A.\n")
        else:
            if tablero.realizar_movimiento_B(r, c):
                print("Movimiento realizado por el jugador B.\n")
                jugador = "A"
                print(tablero)
            else:
                print("Movimiento inválido para el jugador B.\n")

if __name__ == "__main__":
    main()