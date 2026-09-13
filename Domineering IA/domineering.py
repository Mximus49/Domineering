"""Módulo que contiene la lógica del tablero y las reglas del juego."""
from board import Board


class DomineeringTablero(Board):
    """Representa el tablero del juego.

    Hereda de la clase Board y maneja la lógica de movimientos
    para los jugadores A (fichas verticales, humano, juega primero)
    y B (fichas horizontales, IA).
    """

    __player_a: str  # Identificador para el jugador A.
    __player_b: str  # Identificador para el jugador B.

    def __init__(self, tamano: int):
        """Inicializa el tablero del juego."""
        if tamano < 4:
            raise ValueError("El tamaño del tablero debe ser mayor o igual a 4.")

        super().__init__(tamano)
        self.__player_a = "A"
        self.__player_b = "B"

    def movimiento_a_valido(self, r: int, c: int) -> bool:
        """Valida si el movimiento del jugador A es válido.

        El jugador A coloca su ficha de manera vertical ocupando
        las casillas consecutivas (r, c) y (r + 1, c).
        """
        if not self.valid_move(r, c):
            return False

        # Verifica que la ficha no exceda los límites del tablero.
        if r + 1 > len(self):
            return False

        return self.valid_move(r + 1, c)

    def movimiento_b_valido(self, r: int, c: int) -> bool:
        """Valida si el movimiento del jugador B es válido.

        El jugador B coloca su ficha de manera horizontal ocupando
        las casillas consecutivas (r, c) y (r, c + 1).
        """
        if not self.valid_move(r, c):
            return False

        # Verifica que la ficha no exceda los límites del tablero.
        if c + 1 > len(self):
            return False

        return self.valid_move(r, c + 1)

    def realizar_movimiento_a(self, r: int, c: int) -> bool:
        """Ejecuta el movimiento del jugador A en el tablero."""
        if not self.movimiento_a_valido(r, c):
            return False

        # Asigna el jugador A a la posición vertical.
        self[r, c] = self.__player_a
        self[r + 1, c] = self.__player_a
        return True

    def realizar_movimiento_b(self, r: int, c: int) -> bool:
        """Ejecuta el movimiento del jugador B en el tablero."""
        if not self.movimiento_b_valido(r, c):
            return False

        # Asigna el jugador B a la posición horizontal.
        self[r, c] = self.__player_b
        self[r, c + 1] = self.__player_b
        return True

    def deshacer_movimiento_a(self, r: int, c: int) -> None:
        """Deshace un movimiento vertical previamente realizado por A.

        Limpia las dos casillas (r, c) y (r + 1, c) que el jugador A
        ocupó al jugar en esa posición.
        """
        self[r, c] = self.EMPTY_SPACE
        self[r + 1, c] = self.EMPTY_SPACE

    def deshacer_movimiento_b(self, r: int, c: int) -> None:
        """Deshace un movimiento horizontal previamente realizado por B.

        Limpia las dos casillas (r, c) y (r, c + 1) que el jugador B
        ocupó al jugar en esa posición.
        """
        self[r, c] = self.EMPTY_SPACE
        self[r, c + 1] = self.EMPTY_SPACE

    def movimiento_valido(self, jugador: str) -> bool:
        """Comprueba si un jugador tiene algún movimiento válido disponible.

        Itera sobre todo el tablero para verificar si el jugador indicado
        aún puede colocar una ficha.
        """
        if jugador == "A":
            for r in range(1, len(self) + 1):
                for c in range(1, len(self) + 1):
                    if self.movimiento_a_valido(r, c):
                        return True

        elif jugador == "B":
            for r in range(1, len(self) + 1):
                for c in range(1, len(self) + 1):
                    if self.movimiento_b_valido(r, c):
                        return True

        return False

    def obtener_movimientos(self, jugador: str) -> list[tuple[int, int]]:
        movimientos = []
        for r in range(1, len(self) + 1):
            for c in range(1, len(self) + 1):
                if jugador == "A" and self.movimiento_a_valido(r, c):
                    movimientos.append((r, c))
                elif jugador == "B" and self.movimiento_b_valido(r, c):
                    movimientos.append((r, c))
        return movimientos

    def evaluar_tablero(self) -> int:
        """Evalúa el tablero desde la perspectiva del jugador A.

        Retorna un valor positivo si el jugador A tiene ventaja,
        un valor negativo si el jugador B (IA) tiene ventaja, y 0 si es
        empate.
        """
        movimientos_a = len(self.obtener_movimientos("A"))
        movimientos_b = len(self.obtener_movimientos("B"))
        return movimientos_a - movimientos_b