"""Módulo que contiene la lógica del tablero y las reglas del juego."""
from board import Board


class DomineeringTablero(Board):
    """Representa el tablero del juego.

    Hereda de la clase Board y maneja la lógica de movimientos
    para los jugadores A (fichas horizontales) y B (fichas verticales).
    """

    __player_a: str  # Identificador para el jugador A.
    __player_b: str  # Identificador para el jugador B.

    def __init__(self, tamano: int):
        """Inicializa el tablero del juego.

        Args:
            tamano (int): Representa la dimensión del tablero (n x n),
                el cual debe ser >= 4.

        Raises:
            ValueError: Si el tamaño del tablero es menor a 4.
        """
        if tamano < 4:
            raise ValueError("El tamaño del tablero debe ser mayor o igual a 4.")

        super().__init__(tamano)
        self.__player_a = "A"
        self.__player_b = "B"

    def movimiento_a_valido(self, r: int, c: int) -> bool:
        """Valida si el movimiento del jugador A es válido.

        El jugador A coloca su ficha de manera horizontal ocupando
        las casillas consecutivas (r, c) y (r, c + 1).

        Args:
            r (int): Fila objetivo en el tablero.
            c (int): Columna objetivo en el tablero.

        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        if not self.valid_move(r, c):
            return False

        # Verifica que la ficha no exceda los límites del tablero.
        if c + 1 > len(self):
            return False

        return self.valid_move(r, c + 1)

    def movimiento_b_valido(self, r: int, c: int) -> bool:
        """Valida si el movimiento del jugador B es válido.

        El jugador B coloca su ficha de manera vertical ocupando
        las casillas consecutivas (r, c) y (r + 1, c).

        Args:
            r (int): Fila objetivo en el tablero.
            c (int): Columna objetivo en el tablero.

        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        if not self.valid_move(r, c):
            return False

        # Verifica que la ficha no exceda los límites del tablero.
        if r + 1 > len(self):
            return False

        return self.valid_move(r + 1, c)

    def realizar_movimiento_a(self, r: int, c: int) -> bool:
        """Ejecuta el movimiento del jugador A en el tablero.

        Args:
            r (int): Fila donde se colocará la ficha.
            c (int): Columna inicial para la ficha.

        Returns:
            bool: True si se realizó con éxito, False si el movimiento era inválido.
        """
        if not self.movimiento_a_valido(r, c):
            return False

        # Asigna el jugador A a la posición horizontal.
        self[r, c] = self.__player_a
        self[r, c + 1] = self.__player_a
        return True

    def realizar_movimiento_b(self, r: int, c: int) -> bool:
        """Ejecuta el movimiento del jugador B en el tablero.

        Args:
            r (int): Fila donde se colocará la ficha.
            c (int): Columna inicial para la ficha.

        Returns:
            bool: True si se realizó con éxito, False si el movimiento era inválido.
        """
        if not self.movimiento_b_valido(r, c):
            return False

        # Asigna el jugador B a la posición vertical.
        self[r, c] = self.__player_b
        self[r + 1, c] = self.__player_b
        return True

    def movimiento_valido(self, jugador: str) -> bool:
        """Comprueba si un jugador tiene algún movimiento válido disponible.

        Itera sobre todo el tablero para verificar si el jugador indicado
        aún puede colocar una ficha.

        Args:
            jugador (str): Identificador del jugador ("A" o "B").

        Returns:
            bool: True si existe un movimiento válido, False en caso contrario.
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