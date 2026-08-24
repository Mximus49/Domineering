from board import Board


class DomineeringTablero(Board):
    __playerA: str  # Jugador A
    __playerB: str  # Jugador B

    def __init__(self, tamano: int):
        if tamano < 4:
            raise ValueError("El tamaño del tablero debe ser mayor o igual a 4.")
        
        super().__init__(tamano)
        self.__playerA = "A"
        self.__playerB = "B"

    def movimiento_A_valido(self, r: int, c: int) -> bool:
        """Valida si el movimiento del jugador A es válido
        
        El jugador A coloca su ficha de manera horizontal
        """
        if not self.valid_move(r, c):
            return False
        if c + 1 > len(self):
            return False
        return self.valid_move(r, c + 1)

    def movimiento_B_valido(self, r: int, c: int) -> bool:
        """Valida si el movimiento del jugador B es válido
        
        El jugador B coloca su ficha de manera vertical
        """
        if not self.valid_move(r, c):
            return False
        if r + 1 > len(self):
            return False
        return self.valid_move(r + 1, c)

    def realizar_movimiento_A(self, r: int, c: int) -> bool:
        if not self.movimiento_A_valido(r, c):
            return False
        self[r, c] = self.__playerA
        self[r, c + 1] = self.__playerA
        return True

    def realizar_movimiento_B(self, r: int, c: int) -> bool:
        if not self.movimiento_B_valido(r, c):
            return False
        self[r, c] = self.__playerB
        self[r + 1, c] = self.__playerB
        return True

    def movimiento_valido(self, jugador: str) -> bool:
        if jugador == "A":
            for r in range(1, len(self) + 1):
                for c in range(1, len(self) + 1):
                    if self.movimiento_A_valido(r, c):
                        return True
        elif jugador == "B":
            for r in range(1, len(self) + 1):
                for c in range(1, len(self) + 1):
                    if self.movimiento_B_valido(r, c):
                        return True
        return False