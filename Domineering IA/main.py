"""
Gestiona la interacción con los jugadores, solicita la configuración inicial 
del tablero y controla el flujo de los turnos hasta determinar un ganador.
"""
from domineering import DomineeringTablero
from ia import minimax_alfa_beta

# Cambiar R y C, ESTAN AL REVES


def calcular_profundidad(n: int) -> int:
    """Calcula una profundidad de búsqueda razonable según el tamaño del tablero.

    Los tableros grandes tienen muchas más jugadas posibles por turno, por lo
    que se reduce la profundidad para mantener el tiempo de cómputo de la IA
    dentro de límites aceptables. Los umbrales fueron ajustados a partir de
    pruebas de tiempo con el algoritmo Minimax + poda Alfa-Beta.

    Args:
        n (int): Tamaño del tablero (n x n).

    Returns:
        int: Profundidad (cantidad de jugadas a simular) recomendada.
    """
    if n <= 5:
        return 6
    elif n <= 9:
        return 4
    else:
        return 3


def calcular_limite_movimientos(n: int) -> int | None:
    """Calcula cuántas jugadas candidatas evaluar como máximo en cada nodo.

    En tableros muy pequeños se evalúan todas las jugadas disponibles (sin
    restricción), ya que su cantidad ya es manejable. En el resto de los
    casos se limita la cantidad de opciones consideradas en cada nodo (una
    vez ordenadas de mejor a peor con `ordenar_movimientos`) para evitar que
    el árbol de búsqueda crezca de forma incontrolable.

    Args:
        n (int): Tamaño del tablero (n x n).

    Returns:
        int | None: Cantidad máxima de movimientos a evaluar por nodo, o None
            si no se desea aplicar restricción.
    """
    if n <= 5:
        return None
    return max(8, 60 // n)


def solicitar_modo_entrada() -> str:
    """Solicita al jugador humano el formato en que ingresará sus jugadas.

    Esta elección se realiza una sola vez, al inicio de la partida, y se
    mantiene durante todos los turnos del jugador humano.

    Returns:
        str: "numeros" si el jugador ingresará la fila y la columna por
            separado, o "tupla" si las ingresará juntas en una sola línea.
    """
    print("\n¿Cómo prefieres ingresar tus jugadas?")
    print("  1. Números por separado (primero la fila, luego la columna)")
    print("  2. Como tupla en una sola línea, por ejemplo: 3,4 o (3, 4)")

    while True:
        opcion = input("Ingresa 1 o 2: \n")

        if opcion == "1":
            return "numeros"
        elif opcion == "2":
            return "tupla"
        else:
            print("Opción inválida. Por favor, ingresa 1 o 2.\n")


def leer_movimiento_humano(n: int, modo_entrada: str) -> tuple[int, int] | None:
    """Solicita al jugador humano las coordenadas de su jugada.

    El formato de la solicitud depende de `modo_entrada`, definido al inicio
    de la partida mediante `solicitar_modo_entrada`. Toda la validación se
    hace con condicionales `if` explícitos (sin try/except), de modo que
    cada caso inválido imprime un mensaje que indica específicamente cuál
    fue el problema.

    Args:
        n (int): Tamaño del tablero, usado para armar los mensajes al usuario.
        modo_entrada (str): "numeros" o "tupla".

    Returns:
        tuple[int, int] | None: Las coordenadas (fila, columna) ingresadas
            como enteros, o None si la entrada no pudo interpretarse (en
            cuyo caso ya se informó el error específico al usuario).
    """
    if modo_entrada == "numeros":
        entrada_fila = input(f"Ingrese la fila (1 a {n}): \n").strip()
        entrada_columna = input(f"Ingrese la columna (1 a {n}): \n").strip()

        if not entrada_fila.isdigit():
            print(f"Entrada inválida: la fila '{entrada_fila}' debe ser un número entero positivo.\n")
            return None

        if not entrada_columna.isdigit():
            print(f"Entrada inválida: la columna '{entrada_columna}' debe ser un número entero positivo.\n")
            return None

        return int(entrada_fila), int(entrada_columna)

    else:  # modo_entrada == "tupla"
        entrada = input(f"Ingrese la jugada como fila,columna (1 a {n}), ej: 3,4: \n")

        # Quita paréntesis y espacios sobrantes, pero conserva la coma.
        limpio = entrada.strip().replace("(", "").replace(")", "").replace(" ", "")

        if "," not in limpio:
            print(f"Entrada inválida: '{entrada.strip()}' no tiene una coma que separe fila y columna. Ejemplo: 3,4\n")
            return None

        partes = limpio.split(",")

        if len(partes) != 2:
            print(f"Entrada inválida: debes ingresar exactamente dos valores separados por una coma (fila,columna). Ejemplo: 3,4\n")
            return None

        texto_fila, texto_columna = partes

        if not texto_fila.isdigit():
            print(f"Entrada inválida: la fila '{texto_fila}' debe ser un número entero positivo.\n")
            return None

        if not texto_columna.isdigit():
            print(f"Entrada inválida: la columna '{texto_columna}' debe ser un número entero positivo.\n")
            return None

        return int(texto_fila), int(texto_columna)


def diagnosticar_movimiento_b(tablero, n: int, r: int, c: int) -> str | None:
    """Explica por qué un movimiento vertical del jugador B no es válido.

    Reproduce, con condicionales `if`, las mismas condiciones que revisa
    `movimiento_b_valido`, pero describiendo específicamente cuál de ellas
    falló, en vez de solo indicar que el movimiento es inválido.

    Args:
        tablero: Instancia del tablero de juego.
        n (int): Tamaño del tablero.
        r (int): Fila de la casilla superior del dominó.
        c (int): Columna de la casilla superior del dominó.

    Returns:
        str | None: Un mensaje describiendo el problema encontrado, o None
            si el movimiento en realidad sí es válido.
    """
    if r + 1 > n:
        return f"la ficha ocuparía la fila {r + 1}, fuera del tablero (filas 1 a {n})."

    if tablero[r, c] != tablero.EMPTY_SPACE:
        return f"la casilla ({r}, {c}) ya está ocupada."

    if tablero[r + 1, c] != tablero.EMPTY_SPACE:
        return f"la casilla ({r + 1}, {c}) ya está ocupada."

    return None


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

    # Calcula los parámetros de búsqueda de la IA en función del tamaño del tablero.
    profundidad_ia = calcular_profundidad(n)
    limite_movimientos = calcular_limite_movimientos(n)

    # Solicita una sola vez el formato de entrada que usará el jugador humano
    # durante toda la partida.
    modo_entrada = solicitar_modo_entrada()

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
            _, mejor_jugada = minimax_alfa_beta(
                tablero,
                profundidad_ia,
                -float("inf"),
                float("inf"),
                True,
                limite_movimientos,
            )

            if mejor_jugada:
                tablero.realizar_movimiento_a(mejor_jugada[0], mejor_jugada[1])
                print(f"IA juega en fila {mejor_jugada[0]}, columna {mejor_jugada[1]}.\n")
                jugador = "B"
                print(tablero)
        else:
            # Solicita las coordenadas de la jugada según el modo elegido al inicio.
            resultado = leer_movimiento_humano(n, modo_entrada)
            if resultado is None:
                continue

            r, c = resultado

            if r < 1 or r > n or c < 1 or c > n:
                print(f"Movimiento invalido. Las coordenadas deben estar entre 1 y {n}.\n")
                continue

            # Diagnostica específicamente por qué la jugada no sería válida,
            # antes de intentar realizarla.
            razon_invalida = diagnosticar_movimiento_b(tablero, n, r, c)

            if razon_invalida is not None:
                print(f"Movimiento inválido para el jugador B: {razon_invalida}\n")
                continue

            # La jugada es válida: la ejecuta y cambia el turno al jugador A.
            tablero.realizar_movimiento_b(r, c)
            print("Movimiento realizado por el jugador B.\n")
            jugador = "A"
            print(tablero)


# Punto de entrada estándar de los scripts de Python.
if __name__ == "__main__":
    main()